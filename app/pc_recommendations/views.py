from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.utils import timezone
from datetime import timedelta

class PCRecommendationView(APIView):
    def post(self, request):
        try:
            # Parameter aus der Anfrage extrahieren
            budget = request.data.get('budget')
            requirements = request.data.get('requirements')
            
            # Session-Management
            session = request.session
            current_time = timezone.now()
            
            # Prüfe, ob die Session abgelaufen ist (30 Minuten Timeout)
            if 'last_activity' in session:
                last_activity = timezone.datetime.fromisoformat(session['last_activity'])
                if current_time - last_activity > timedelta(minutes=15):
                    # Session zurücksetzen, wenn sie abgelaufen ist
                    session.flush()
            
            # Aktualisiere den Zeitstempel der letzten Aktivität
            session['last_activity'] = current_time.isoformat()
            
            # Hole den Kontext der vorherigen Konversation, falls vorhanden
            conversation_history = session.get('conversation_history', [])
            
            if not budget or not requirements:
                return Response(
                    {"error": "Budget und Anforderungen sind erforderlich"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Erstelle den Prompt basierend auf dem Kontext
            if conversation_history:
                # Wenn es eine Rückfrage ist, füge den Kontext hinzu
                context_prompt = "Basierend auf unserer vorherigen Konversation:\n"
                for conversation_entry in conversation_history[-3:]:  # Nur die letzten 3 Einträge verwenden
                    context_prompt += f"Budget: {conversation_entry['budget']}€\n"
                    context_prompt += f"Anforderungen: {conversation_entry['requirements']}\n"
                    context_prompt += f"Meine Antwort war: {conversation_entry['recommendation']}\n\n"


                
                prompt = f"""{context_prompt}
                Neue Anfrage:
                Budget: {budget}€
                Anforderungen: {requirements}
                
                Bitte berücksichtige die vorherige Konversation und gib eine aktualisierte Empfehlung mit:
                1. Liste der Komponenten mit Preisen
                2. Gesamtkosten auflisten direkt nach der liste der Komponenten!
                3. Begründung für die Auswahl
                4. Falls das Budget zu niedrig ist, Vorschläge zur Anpassung
                5. Alternative Optionen falls verfügbar
                6. Benutze das Budget der neuen Anfrage und auch die Anforderungen!
                
                Formatiere die Antwort übersichtlich. Die Bauteile zusammen sollen einen kompletten funktionsfähigen PC darstellen, es darf kein Teil fehlen. """
            else:
                # Erste Anfrage
                prompt = f"""Als PC-Experte, empfehle mir bitte eine PC-Konfiguration mit folgenden Kriterien:
                Budget: {budget}€
                Anforderungen: {requirements}
                
                Bitte gib eine detaillierte Empfehlung mit:
                1. Liste der Komponenten mit Preisen
                2. Gesamtkosten auflisten direkt nach der liste der Komponenten!
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
                "max_tokens": 1000,
                "n": 1 # Nur eine Antwort anfordern
            }

            response = requests.post(lm_studio_url, headers=headers, json=data)
            
            if response.status_code == 200:
                ai_response = response.json()
                recommendation = ai_response['choices'][0]['message']['content']
                
                # Speichere die Konversation in der Session
                conversation_entry = {
                    'budget': budget,
                    'requirements': requirements,
                    'recommendation': recommendation,
                    'timestamp': current_time.isoformat()
                }
                conversation_history.append(conversation_entry)
                session['conversation_history'] = conversation_history
                
                return Response({
                    "recommendation": recommendation,
                    "is_follow_up": bool(conversation_history)  # Flag, ob es eine Rückfrage ist
                })
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