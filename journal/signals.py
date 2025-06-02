from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


# def create_initial_data(sender, **kwargs):
#     if sender.name == 'journal':
#         DescentType = apps.get_model('journal', 'DescentType')
        
        
#         # Create all descent types first
#         type_data = [
#             {
#                 'type': 'EMOTIONAL',
#                 'name': 'Emotional',
#                 'description': 'A journey to explore and process emotions'
#             },
#             {
#                 'type': 'MENTAL',
#                 'name': 'Mental',
#                 'description': 'A journey to explore thoughts and mental patterns'
#             },
#             {
#                 'type': 'SPIRITUAL',
#                 'name': 'Spiritual',
#                 'description': 'A journey to explore spiritual experiences'
#             },
#             {
#                 'type': 'PHYSICAL',
#                 'name': 'Physical',
#                 'description': 'A journey to explore physical sensations'
#             },
#             {
#                 'type': 'EXISTENTIAL',
#                 'name': 'Existential',
#                 'description': 'A journey to explore life\'s big questions'
#             }
#         ]
        
#         # Create all descent types
#         for data in type_data:
#             DescentType.objects.create(**data)

        
# @receiver(post_migrate)
# def create_initial_data_signal(sender, **kwargs):
#     create_initial_data(sender, **kwargs)