from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.utils import timezone
from datetime import timedelta
from pc_components.models import Component


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
                if current_time - last_activity > timedelta(minutes=30):
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
            
            # Komponenten aus der Datenbank abrufen
            components_data = self._get_components_from_database()
            
            # Erstelle den Prompt basierend auf dem Kontext und den verfügbaren Komponenten
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
                
                Hier sind die verfügbaren Komponenten, die du für die PC-Zusammenstellung verwenden sollst:
                {components_data}
                
                WICHTIG: Verwende nur die oben aufgelisteten Komponenten für deine Empfehlung!
                
                Bitte berücksichtige die vorherige Konversation und gib eine aktualisierte Empfehlung mit:
                1. Liste der Komponenten mit Preisen (nur aus der obigen Liste!)
                2. Gesamtkosten auflisten direkt nach der liste der Komponenten!
                3. Begründung für die Auswahl
                4. Falls das Budget zu niedrig ist, Vorschläge zur Anpassung
                5. Alternative Optionen falls verfügbar
                6. Benutze das Budget der neuen Anfrage und auch die Anforderungen!
                
                Formatiere die Antwort übersichtlich. Die Bauteile zusammen sollen einen kompletten funktionsfähigen PC darstellen, es darf kein Teil fehlen. 
                Vergewissere dich, dass deine Empfehlung folgende Komponententypen enthält: CPU, GPU, Motherboard, RAM, Storage, Power Supply und Case."""
            else:
                # Erste Anfrage
                prompt = f"""Als PC-Experte, empfehle mir bitte eine PC-Konfiguration mit folgenden Kriterien:
                Budget: {budget}€
                Anforderungen: {requirements}
                
                Hier sind die verfügbaren Komponenten, die du für die PC-Zusammenstellung verwenden sollst:
                {components_data}
                
                WICHTIG: Verwende nur die oben aufgelisteten Komponenten für deine Empfehlung!
                
                Bitte gib eine detaillierte Empfehlung mit:
                1. Liste der Komponenten mit Preisen (nur aus der obigen Liste!)
                2. Gesamtkosten auflisten direkt nach der liste der Komponenten!
                3. Begründung für die Auswahl
                4. Falls das Budget zu niedrig ist, Vorschläge zur Anpassung
                5. Alternative Optionen falls verfügbar
                
                Formatiere die Antwort übersichtlich. Die Bauteile zusammen sollen einen kompletten funktionsfähigen PC darstellen, es darf kein Teil fehlen.
                Vergewissere dich, dass deine Empfehlung folgende Komponententypen enthält: CPU, GPU, Motherboard, RAM, Storage, Power Supply und Case."""

            # Anfrage an LM Studio senden
            lm_studio_url = "http://localhost:1234/v1/chat/completions"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "messages": [
                    {"role": "system", "content": "Du bist ein erfahrener PC-Experte, der detaillierte und präzise PC-Konfigurationsempfehlungen gibt. Verwende nur die bereitgestellten Komponenten und deren Preise."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1500,  # Erhöht für längere Antworten mit Komponenten
                "n": 1
            }

            try:
                response = requests.post(lm_studio_url, headers=headers, json=data, timeout=60)  # Erhöhtes Timeout
                response.raise_for_status()  # Wirft eine Exception bei HTTP-Fehlern
                
                ai_response = response.json()
                
                # Validiere die Antwort von LM Studio
                if not ai_response.get('choices') or not ai_response['choices'][0].get('message', {}).get('content'):
                    raise ValueError("Ungültige Antwort von LM Studio")
                
                recommendation = ai_response['choices'][0]['message']['content']
                
                # Speichere die Konversation in der Session
                conversation_entry = {
                    'budget': budget,
                    'requirements': requirements,
                    'recommendation': recommendation,
                    'timestamp': current_time.isoformat()
                }
                if not conversation_history:
                    conversation_history = []
                conversation_history.append(conversation_entry)
                session['conversation_history'] = conversation_history
                
                return Response({
                    "recommendation": recommendation,
                    "is_follow_up": len(conversation_history) > 1
                })
                
            except requests.exceptions.RequestException as e:
                print(f'Fehler bei der Kommunikation mit LM Studio: {str(e)}')
                return Response(
                    {"error": f"Fehler bei der Kommunikation mit LM Studio: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except (KeyError, ValueError) as e:
                print(f'Ungültige Antwort von LM Studio: {str(e)}')
                return Response(
                    {"error": f"Ungültige Antwort von LM Studio: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            print(f'Unerwarteter Fehler: {str(e)}')
            return Response(
                {"error": f"Unerwarteter Fehler: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_components_from_database(self):
        """
        Holt die Komponenten aus der Datenbank und formatiert sie für den Prompt
        """
        # Komponententypen, die wir benötigen
        component_types = ['CPU', 'GPU', 'Motherboard', 'RAM', 'Storage', 'Power Supply', 'Case']
        
        # Formatierte String für den Prompt
        components_str = ""
        
        for component_type in component_types:
            # Hole die Komponenten dieses Typs
            components = Component.objects.filter(type=component_type)
            
            # Stichprobe für jede Kategorie (maximal 15 Komponenten pro Typ)
            sample = list(components.order_by('?')[:15])
            
            components_str += f"\n{component_type.upper()} Komponenten:\n"
            
            for comp in sample:
                # Formatiere Preis mit 2 Dezimalstellen
                price = "{:.2f}".format(comp.price)
                components_str += f"- {comp.name} ({comp.manufacturer}) - {price}€\n"
            
            components_str += "\n"
        
        return components_str