from django.core.management.base import BaseCommand
from pc_components.models import Component, Pc, Pc_Components

class Command(BaseCommand):
    help = 'Löscht alle Daten aus der Datenbank'

    def handle(self, *args, **options):
        # Lösche alle PC-Komponenten-Beziehungen
        Pc_Components.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Alle PC-Komponenten-Beziehungen gelöscht'))

        # Lösche alle PCs
        Pc.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Alle PCs gelöscht'))

        # Lösche alle Komponenten
        Component.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Alle Komponenten gelöscht'))

        self.stdout.write(self.style.SUCCESS('Datenbank erfolgreich geleert')) 