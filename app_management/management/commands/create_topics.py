import json
import os
from django.core.management.base import BaseCommand
from app_management.models import Topic

class Command(BaseCommand):
    help = 'Creates initial topics for the application from JSON files'

    def handle(self, *args, **options):
        # Determine the directory where JSON files are stored
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'topics_data')

        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f'Topics data directory not found: {data_dir}'))
            return

        # Iterate over all .json files in the directory
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        
        if not json_files:
             self.stdout.write(self.style.WARNING(f'No JSON files found in {data_dir}'))
             return

        for filename in json_files:
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    topic_data = json.load(f)
                
                # Validate required fields
                if 'name' not in topic_data or 'form_fields' not in topic_data:
                    self.stdout.write(self.style.ERROR(f'Invalid JSON format in {filename}: Missing name or form_fields'))
                    continue

                topic, created = Topic.objects.update_or_create(
                    name=topic_data['name'],
                    defaults={
                        'template': topic_data.get('template', ''),
                        'form_fields': topic_data['form_fields']
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Topic "{topic.name}" created successfully (from {filename}).'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Topic "{topic.name}" updated successfully (from {filename}).'))

            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f'Error deciding JSON in {filename}: {e}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {filename}: {e}'))
