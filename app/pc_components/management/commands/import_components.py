from django.core.management.base import BaseCommand
from pc_components.models import Component
import csv
import os
import re
from decimal import Decimal

class Command(BaseCommand):
    help = 'Importiert PC-Komponenten aus CSV-Dateien'

    def handle(self, *args, **options):
        # Währungswechselkurs von INR zu EUR (Beispielkurs, sollte aktualisiert werden)
        INR_TO_EUR = 0.011  # 1 INR = 0.011 EUR

        # Mapping der Dateinamen zu Komponententypen
        component_types = {
            'CPU.csv': 'CPU',
            'GPU.csv': 'GPU',
            'MotherBoard.csv': 'Motherboard',
            'RAM.csv': 'RAM',
            'StorageSSD.csv': 'Storage',
            'PowerSupply.csv': 'Power Supply',
            'cabinates.csv': 'Case'
        }

        # Basisverzeichnis für die CSV-Dateien
        base_dir = os.path.join('app', 'data', 'pc_data')

        for filename, component_type in component_types.items():
            file_path = os.path.join(base_dir, filename)
            
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'Datei nicht gefunden: {file_path}'))
                continue

            self.stdout.write(f'Importiere {component_type} aus {filename}...')

            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Überspringe Header

                for row in reader:
                    try:
                        # Extrahiere Name und Hersteller basierend auf dem Dateityp
                        if filename in ['cabinates.csv', 'PowerSupply.csv']:
                            full_name = row[0].strip()
                            price_str = row[1].strip()
                        else:
                            full_name = row[1].strip()
                            price_str = row[2].strip()
                        
                        # Versuche Hersteller zu extrahieren
                        manufacturer = 'Unknown'
                        full_name_lower = full_name.lower()
                        
                        # Erweiterte Hersteller-Erkennung
                        manufacturer_mappings = {
                            'amd': 'AMD',
                            'intel': 'Intel',
                            'nvidia': 'NVIDIA',
                            'gigabyte': 'Gigabyte',
                            'msi': 'MSI',
                            'asus': 'ASUS',
                            'corsair': 'Corsair',
                            'samsung': 'Samsung',
                            'crucial': 'Crucial',
                            'seagate': 'Seagate',
                            'western digital': 'Western Digital',
                            'zebronics': 'ZEBRONICS',
                            'ant esports': 'Ant Esports',
                            'cooler master': 'Cooler Master',
                            'deepcool': 'Deepcool',
                            'frontech': 'Frontech',
                            'artis': 'Artis',
                            'ars infotech': 'ARS Infotech',
                            'matrix': 'Matrix',
                            'rubaintech': 'Rubaintech',
                            'wefly': 'WEFLY',
                            'techon': 'TECHON',
                            'betaohm': 'Betaohm',
                            'gigastar': 'GIGASTAR',
                            'asrock': 'ASRock'
                        }

                        for key, value in manufacturer_mappings.items():
                            if key in full_name_lower:
                                manufacturer = value
                                break

                        # Extrahiere Preis und konvertiere von INR zu EUR
                        price_str = price_str.replace('₹', '').replace(',', '')
                        price_inr = Decimal(price_str)
                        price_eur = price_inr * Decimal(str(INR_TO_EUR))

                        # Erstelle die Komponente
                        Component.objects.create(
                            name=full_name,
                            type=component_type,
                            manufacturer=manufacturer,
                            price=price_eur,
                            currency='EUR',
                            description='',
                            technical_details=''
                        )

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Fehler beim Importieren von {row}: {str(e)}'))

            self.stdout.write(self.style.SUCCESS(f'Import von {component_type} abgeschlossen'))

        self.stdout.write(self.style.SUCCESS('Import aller Komponenten abgeschlossen')) 