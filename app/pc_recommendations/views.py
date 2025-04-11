from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from pc_components.models import Component
import re
import json


class PCRecommendationView(APIView):
    def post(self, request):
        try:
            budget = request.data.get('budget')
            requirements = request.data.get('requirements')

            if not budget or not requirements:
                return Response(
                    {"error": "Budget und Anforderungen sind erforderlich"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            weight_prompt = f"""Erstelle eine Preisverteilung für einen PC mit:
            Budget: {budget}€
            Anforderungen: {requirements}

            WICHTIG:
            - Gib NUR das JSON-Objekt zurück
            - Keine zusätzlichen Erklärungen
            - Summe muss genau 100% ergeben nicht mehr nicht weniger!
            - Case muss mindestens 5% sein, mit Case dürfen wir aber nicht  über 100% kommen sondern genau auf 100%

            Beispiel-Antwort:
            {{
                "cpu": 30,
                "gpu": 30,
                "ram": 15,
                "ssd": 10,
                "psu": 10,
                "case": 5
            }}"""

            try:
                weight_response = self._send_to_lm_studio(weight_prompt, is_weight_distribution=True)
                print("after first _send_to_lm_studio")
                weight_data = extract_json_from_ai(weight_response)
                print(f"Daten von der AI: {weight_data}")

                if not self._validate_weight_distribution(weight_data):
                    raise ValueError("Ungültige Preisverteilung von der AI")

                filtered_components = self._get_filtered_components(budget, weight_data)
                final_prompt = self._create_final_prompt(budget, requirements, filtered_components)
                final_recommendation = self._send_to_lm_studio(final_prompt, is_weight_distribution=False)

                return Response({
                    "recommendation": final_recommendation
                })

            except (requests.exceptions.RequestException, json.JSONDecodeError, ValueError) as e:
                print(f'Fehler bei der Verarbeitung: {str(e)}')
                return Response(
                    {"error": f"Fehler bei der Verarbeitung: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            print(f'Unerwarteter Fehler: {str(e)}')
            return Response(
                {"error": f"Unerwarteter Fehler: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _send_to_lm_studio(self, prompt, is_weight_distribution=True):
        lm_studio_url = "http://localhost:1234/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        if is_weight_distribution:
            system_prompt = "Du bist ein erfahrener PC-Experte. Du gibst nur die geforderte Antwort zurück, ohne zusätzliche Erklärungen oder Text. Wenn du eine Preisverteilung zurückgibst, achte darauf, dass die Summe genau 100% ergibt und der Case mindestens 5% beträgt."
        else:
            system_prompt = "Du bist ein erfahrener PC-Experte. Analysiere die gegebenen Komponenten und erstelle eine optimale PC-Konfiguration. Gib eine detaillierte, aber präzise Empfehlung zurück, die alle geforderten Punkte abdeckt."

        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "model": "openhermes-2.5-mistral-7b",
            "temperature": 0.3,
            "max_tokens": 500,
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
            print(f"LM Studio Antwort: {ai_response}")
            if not ai_response.get('choices'):
                raise ValueError("Keine Antwort von LM Studio erhalten")

            message = ai_response['choices'][0].get('message', {})
            if not message or not message.get('content'):
                raise ValueError("Leere Antwort von LM Studio erhalten")

            print(f"Verarbeiteter Message aus der Gefiltet wird: {message}")
            content = message['content'].strip()
            print(f"Verarbeiteter Content: {content}")

            content = content.replace('```json', '').replace('```', '').strip()
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                json.loads(json_str)
                return json_str
            else:
                raise ValueError("Kein JSON in der Antwort gefunden")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Fehler bei der Kommunikation mit LM Studio: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ungültiges JSON-Format in der Antwort: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unerwarteter Fehler bei der Verarbeitung der Antwort: {str(e)}")

    def _validate_weight_distribution(self, weight_data):
        try:
            weight_data = {k: float(v) for k, v in weight_data.items()}
            required_keys = ['cpu', 'gpu', 'ram', 'ssd', 'psu', 'case']
            if not all(key in weight_data for key in required_keys):
                return False
            total = sum(weight_data.values())
            if not (90 <= total <= 110):
                return False
            if weight_data['case'] < 5:
                return False
            if not all(v > 0 for v in weight_data.values()):
                return False
            print("_validate_weight_distribution was True")
            return True
        except (ValueError, TypeError):
            return False

    def _get_filtered_components(self, budget, weight_data):
        filtered_components = {}
        for component_type, percentage in weight_data.items():
            target_price = (budget * percentage) / 100
            min_price = target_price * 0.9
            max_price = target_price * 1.1
            db_type = self._convert_component_type(component_type)
            components = Component.objects.filter(
                type=db_type,
                price__gte=min_price,
                price__lte=max_price
            ).order_by('price')[:15]
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
        components_str = ""
        for comp_type, components in filtered_components.items():
            components_str += f"\n{comp_type.upper()} Komponenten:\n"
            for comp in components:
                components_str += f"- {comp['name']} ({comp['manufacturer']}) - {comp['price']:.2f}€\n"
            components_str += "\n"

        prompt = f"""Empfehle eine PC-Konfiguration für folgendes:

- Budget: {budget}€
- Anforderungen: {requirements}
- Komponenten (zur Auswahl): {components_str}

⚠️ WICHTIG:
- Verwende nur diese Komponenten
- Gib nur ein valides JSON-Objekt zurück. Keine weiteren Erklärungen.
- Nur ein einziges 'components'-Feld im JSON!
- Felder:
  - \"components\": Liste der gewählten Komponenten mit name + price
  - \"total_cost\": Gesamtkosten
  - \"justification\": Begründung
  - \"adjustments\": Was tun, wenn Budget zu niedrig ist?
  - \"alternatives\": Optionale Alternativen

📌 Beispiel:

{{
  \"components\": [
    {{ \"name\": \"Intel i5\", \"price\": 200 }},
    {{ \"name\": \"GTX 1660\", \"price\": 300 }}
  ],
  \"total_cost\": 500,
  \"justification\": \"Stabile Performance für Programmieren.\",
  \"adjustments\": \"RAM oder SSD verkleinern.\",
  \"alternatives\": \"Ryzen 5 statt Intel i5\"
}}
"""
        return prompt


def extract_json_from_ai(content: str):
    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError("Kein JSON-Objekt gefunden")
        json_str = json_match.group()
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Fehler beim Extrahieren des JSONs: {e}")
