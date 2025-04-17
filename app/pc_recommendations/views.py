from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from pc_components.models import Component
import re
import json
import openai
import os


class PCRecommendationView(APIView):
    """
        API view that generates a PC recommendation based on a user's budget and use-case requirements.

        It communicates with a local language model (LM Studio) to calculate a budget allocation and
        assemble a suitable PC configuration using filtered components from the database.
    """
    def post(self, request):
        """
            Handles the POST request to generate a PC configuration recommendation.

            Retrieves the user-defined budget and requirements from the request,
            calculates a component weight distribution using the language model,
            filters components from the database based on that distribution,
            and sends a final prompt to the model to generate a full build recommendation.

            Returns:
                Response: A JSON response containing the recommended PC or an error.
        """
        try:
            budget = request.data.get('budget')
            requirements = request.data.get('requirements')

            if not budget or not requirements:
                return Response(
                    {"error": "Budget and requirements are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            base_prompt = f"""You are an experienced PC expert. Create a percentage-based budget distribution for a custom PC build based on the following:

            - Total budget: {budget} Euros
            - Requirements: {requirements}

            ⚠️ STRICT INSTRUCTIONS:
            - Return only a valid JSON object – absolutely no comments, explanation, or extra formatting
            - Use exactly these 8 component types as keys:
              "cpu", "gpu", "ram", "ssd", "psu", "case", "motherboard", "cooler"
            - The sum of all values must be **exactly 100** (as percentages) – no rounding errors
            - All values must be positive numbers
            - The share for "case" must be at least 5%
            - Do not include extra keys like "monitor", "keyboard", "others", etc.

            📦 Example format (structure must match exactly):

            {{
              "cpu": 25,
              "gpu": 30,
              "ram": 15,
              "ssd": 10,
              "psu": 7,
              "case": 5,
              "motherboard": 5,
              "cooler": 3
            }}
            """

            MAX_RETRIES = 6
            for attempt in range(MAX_RETRIES):
                try:
                    prompt = base_prompt
                    if attempt == 1:
                        prompt += "\n\n// Please repeat the calculation with a completely new approach. The previous result did not sum up to exactly 100 – this time, make absolutely sure that the percentage values add up to exactly 100, with no rounding errors."
                    weight_response = self._send_to_lm_studio(prompt, is_weight_distribution=True)
                    weight_data = extract_json_from_ai(weight_response)


                    if not self._validate_weight_distribution(weight_data):
                        raise ValueError("Invalid price distribution from the AI")

                    filtered_components = self._get_filtered_components(budget, weight_data)
                    final_prompt = self._create_final_prompt(budget, requirements, filtered_components)
                    final_recommendation = self._send_to_lm_studio(final_prompt, is_weight_distribution=False)

                    return Response({
                        "recommendation": final_recommendation
                    })
                except (requests.exceptions.RequestException, json.JSONDecodeError, ValueError) as e:
                    print(f"Error during processing: {str(e)}")
                    if attempt == MAX_RETRIES - 1:
                        return Response(
                            {"error": f"Error during processing: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

        except Exception as e:
            print(f'Unexpected error: {str(e)}')
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _send_to_lm_studio(self, prompt, is_weight_distribution=True):
        """
        Sends a prompt to OpenAI ChatGPT 3.5 API and retrieves the response.
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")

        system_prompt = (
            "You are an experienced PC expert. Only return the required JSON answer, "
            "without any additional explanations or text. When providing a budget distribution, "
            "make sure the sum is exactly 100% and the case share is at least 5%."
            if is_weight_distribution else
            "You are an experienced PC expert. Analyze the given components and create an optimal PC build. "
            "Provide a detailed but concise recommendation that covers all required aspects."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )

            content = response['choices'][0]['message']['content']
            content = content.replace('```json', '').replace('```', '').strip()
            start = content.find('{')
            end = content.rfind('}') + 1

            if start != -1 and end != 0:
                json_str = content[start:end]
                json.loads(json_str)  # Test for valid JSON
                return json_str
            else:
                raise ValueError("No JSON found in the response")
        except Exception as e:
            raise ValueError(f"OpenAI API Error: {e}")

    def _validate_weight_distribution(self, weight_data):
        """
            Validates the structure and values of the AI-generated budget weight distribution.

            Checks if all required component types are present, all values are positive,
            and that the total sum is reasonably close to 100%. Also enforces a minimum of 5% for the case.

            Args:
                weight_data (dict): Dictionary with component types as keys and percentage values.

            Returns:
                bool: True if valid, otherwise False.
        """
        try:
            weight_data = {k: float(v) for k, v in weight_data.items()}
            required_keys = ['cpu', 'gpu', 'ram', 'ssd', 'psu', 'case']
            if not all(key in weight_data for key in required_keys):
                return False
            total = sum(weight_data.values())
            if not (85 <= total <= 115):
                return False
            if weight_data['case'] < 5:
                print("Note: Case share too low, setting it to 5%")
                weight_data['case'] = 5.0
            if not all(v > 0 for v in weight_data.values()):
                return False
            return True
        except (ValueError, TypeError):
            return False

    def _get_filtered_components(self, budget, weight_data):
        """
        Filters components from the database based on their type and the target price derived
        from the AI-generated budget allocation.

        Uses dynamic price ranges to find a minimum number of matching components.

        Args:
            budget (float): Total budget defined by the user.
            weight_data (dict): Budget distribution per component type (in percentages).

        Returns:
            dict: A dictionary of component types mapped to lists of filtered components.
        """
        filtered_components = {}

        for component_type, percentage in weight_data.items():
            target_price = (budget * percentage) / 100
            db_type = self._convert_component_type(component_type)


            min_count = 8
            current_range = 0.1
            max_range = 0.4
            step = 0.05

            while current_range <= max_range:
                min_price = target_price * (1 - current_range)
                max_price = target_price * (1 + current_range)
                components = Component.objects.filter(
                    type=db_type,
                    price__gte=min_price,
                    price__lte=max_price
                ).order_by('price')[:min_count]

                if components.count() >= min_count:
                    break
                current_range += step

            filtered_components[component_type] = [
                {
                    'name': comp.name,
                    'manufacturer': comp.manufacturer,
                    'price': float(comp.price)
                }
                for comp in components
            ]
        return filtered_components

    def _convert_component_type(self, type_str):
        type_map = {
            'cpu': 'CPU',
            'gpu': 'GPU',
            'ram': 'RAM',
            'ssd': 'Storage',
            'psu': 'Power Supply',
            'case': 'Case',
            'motherboard': 'Motherboard',
            'cooler': 'Cooler'
        }
        return type_map.get(type_str.lower())

    def _create_final_prompt(self, budget, requirements, filtered_components):
        """
            Builds the final prompt for the language model to recommend a full PC configuration
            using only the filtered components.

            Args:
                budget (float): Total budget for the PC build.
                requirements (str): User-defined usage goals and preferences.
                filtered_components (dict): Pre-filtered components grouped by type.

            Returns:
                str: A formatted prompt ready to be sent to the language model.
        """
        components_str = ""
        for comp_type, components in filtered_components.items():
            components_str += f"\n{comp_type.upper()} Components:\n"
            for comp in components:
                components_str += f"- {comp['name']} ({comp['manufacturer']}) - {comp['price']:.2f}€\n"
            components_str += "\n"

        prompt = f"""You are a professional PC builder.

        Your task is to recommend a **complete PC build** using **exactly one component from each category**:
        - CPU
        - GPU
        - RAM
        - SSD
        - PSU
        - Case
        - Motherboard
        - Cooler

        🛑 Constraints:
        - Total budget: {budget}€
        - Use case: {requirements}
        - Components must be chosen **only from the list below**
        - All components must be **fully compatible**
        - Total cost must **not exceed** the budget
        - You must return a **valid JSON object only** – no extra text or explanation

        📦 JSON format (must match exactly):

        {{
          "components": [
            {{ "name": "Intel Core i5-12400F", "price": 180.00 }},
            {{ "name": "ZOTAC RTX 3060 Twin Edge OC 12GB", "price": 330.00 }},
            {{ "name": "Corsair Vengeance LPX 16GB DDR4", "price": 65.00 }},
            {{ "name": "Samsung 980 1TB NVMe SSD", "price": 100.00 }},
            {{ "name": "Corsair CV650 650W PSU", "price": 65.00 }},
            {{ "name": "NZXT H510 Mid Tower Case", "price": 70.00 }},
            {{ "name": "MSI B660M Mortar Motherboard", "price": 110.00 }},
            {{ "name": "Cooler Master Hyper 212 Black Edition", "price": 40.00 }}
          ],
          "total_cost": 960.00,
          "justification": "Balanced 1080p gaming setup with strong CPU/GPU combo, fast storage, and reliable components."
        }}

        Available components to choose from:

        {components_str}
        """
        return prompt


def extract_json_from_ai(content: str):
    """
    Extracts the first JSON object found in a raw AI response string.

    Args:
        content (str): Raw string returned by the language model.

    Returns:
        dict: Parsed JSON data.

    Raises:
        ValueError: If no JSON object is found or parsing fails.
    """
    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found")
        json_str = json_match.group()
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Error while extracting JSON: {e}")
