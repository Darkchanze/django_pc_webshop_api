from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json

class PCRecommendationView(APIView):
    def post(self, request):
        try:
            # Parameter aus der Anfrage extrahieren
            budget = request.data.get('budget')
            requirements = request.data.get('requirements')

            if not budget or not requirements:
                return Response(
                    {"error": "Budget und Anforderungen sind erforderlich"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Prompt für LM Studio erstellen
            prompt = f"""Als PC-Experte, empfehle mir bitte eine PC-Konfiguration mit folgenden Kriterien:
            Budget: {budget}€
            Anforderungen: {requirements}
            
            Bitte gib eine detaillierte Empfehlung mit:
            1. Liste der Komponenten mit Preisen
            2. Gesamtkosten
            3. Begründung für die Auswahl
            4. Falls das Budget zu niedrig ist, Vorschläge zur Anpassung
            5. Alternative Optionen falls verfügbar
            
            Formatiere die Antwort übersichtlich. Die Bauteile zusammen sollen einen kompletten funktionsfähigen PC darstellen, es darf kein Teil fehlen."""

            # Anfrage an LM Studio senden
            lm_studio_url = "http://localhost:1234/v1/chat/completions"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "messages": [
                    {"role": "system", "content": "Du bist ein erfahrener PC-Experte, der detaillierte und präzise PC-Konfigurationsempfehlungen gibt."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(lm_studio_url, headers=headers, json=data)
            
            if response.status_code == 200:
                ai_response = response.json()
                recommendation = ai_response['choices'][0]['message']['content']
                return Response({"recommendation": recommendation})
            else:
                return Response(
                    {"error": "Fehler bei der Kommunikation mit LM Studio"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 