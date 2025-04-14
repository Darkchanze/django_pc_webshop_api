from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from pc_components.models import Component
import re
import json


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

            base_prompt = f"""You are an experienced PC expert. Create a percentage-based budget distribution for the following requirements:

            - Total budget: {budget} Euros
            - Requirements: {requirements}

            ⚠️ Important:
            - Return **only a valid JSON object**
            - **Do not include any explanations or comments!**
            - All values must be **percentages**, **not Euro amounts**
            - The **sum of ALL values must be exactly 100** – no rounding errors, no deviations.
            - The share for the case (\"case\") must be **at least 5%**

            Example:

            {{
              "cpu": 30,
              "gpu": 30,
              "ram": 15,
              "ssd": 10,
              "psu": 10,
              "case": 5
            }}
            """

            MAX_RETRIES = 6
            for attempt in range(MAX_RETRIES):
                try:
                    prompt = base_prompt
                    if attempt == 1:
                        prompt += "\n\n// Please repeat the calculation with a completely new approach. The previous result did not sum up to exactly 100 – this time, make absolutely sure that the percentage values add up to exactly 100, with no rounding errors."

                    weight_response = self._send_to_lm_studio(prompt, is_weight_distribution=True)
                    print("after first _send_to_lm_studio")
                    weight_data = extract_json_from_ai(weight_response)
                    print(f"Data from the AI: {weight_data}")

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
            Sends a prompt to the local LM Studio model and retrieves the response.

            Args:
                prompt (str): The prompt to send to the language model.
                is_weight_distribution (bool): Flag indicating whether the prompt is for budget allocation
                                                or final component recommendation.

            Returns:
                str: JSON string extracted from the model's response.

            Raises:
                ValueError: If the model's response is missing, empty, malformed, or contains no JSON.
        """
        lm_studio_url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        if is_weight_distribution:
            system_prompt = "You are an experienced PC expert. Only return the required JSON answer, without any additional explanations or text. When providing a budget distribution, make sure the sum is exactly 100% and the case share is at least 5%."
        else:
            system_prompt = "You are an experienced PC expert. Analyze the given components and create an optimal PC build. Provide a detailed but concise recommendation that covers all required aspects."

        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "model": "openhermes-2.5-mistral-7b",
            "temperature": 0.3,
            "max_tokens": 1200,
            "stop": ["\n\n", "```"],
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0
        }

        try:
            print(f"This is your prompt from the user : {prompt}")
            print(f"this is your system prompt : {system_prompt}")
            print(f"this is your data : {data}")

            response = requests.post(lm_studio_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            ai_response = response.json()
            print(f"LM Studio answer: {ai_response}")
            if not ai_response.get('choices'):
                raise ValueError("No response received from LM Studio")

            message = ai_response['choices'][0].get('message', {})
            if not message or not message.get('content'):
                raise ValueError("Empty response received from LM Studio")

            print(f"Processed message to be filtered: {message}")
            content = message['content'].strip()
            print(f"Processed content: {content}")

            content = content.replace('```json', '').replace('```', '').strip()
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                json.loads(json_str)
                return json_str
            else:
                raise ValueError("No JSON found in the response")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error communicating with LM Studio: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in the response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error while processing the response: {str(e)}")

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
            print("_validate_weight_distribution was True")
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
        print(filtered_components)
        return filtered_components

    def _convert_component_type(self, type_str):
        """
        Converts internal lowercase component type keys to the corresponding
        database model type names used for filtering.

        Args:
            type_str (str): Lowercase identifier (e.g., 'cpu', 'gpu').

        Returns:
            str: Properly capitalized type name matching the database schema.
        """
        type_map = {
            'cpu': 'CPU',
            'gpu': 'GPU',
            'ram': 'RAM',
            'ssd': 'Storage',
            'psu': 'Power Supply',
            'case': 'Case'
        }
        return type_map.get(type_str.lower(), type_str)

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

        prompt = f"""Recommend a PC configuration based on the following:

    - Budget: {budget}€
    - Requirements: {requirements}
    - Components to choose from: {components_str}

    ⚠️ IMPORTANT:
    - Use only the provided components
    - Return only a valid JSON object. No additional explanations.
    - Only one 'components' field in the JSON!
    - Fields:
      - \"components\": List of selected components with name + price
      - \"total_cost\": Total cost
      - \"justification\": Reasoning
      - \"adjustments\": What to change if the budget is too low?
      - \"alternatives\": Optional alternatives

    📌 Example:

    {{
      \"components\": [
        {{ \"name\": \"Intel i5\", \"price\": 200 }},
        {{ \"name\": \"GTX 1660\", \"price\": 300 }}
      ],
      \"total_cost\": 500,
      \"justification\": \"Solid performance for programming.\",
      \"adjustments\": \"Reduce RAM or SSD size.\",
      \"alternatives\": \"Ryzen 5 instead of Intel i5\"
    }}
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
