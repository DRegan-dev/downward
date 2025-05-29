from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

def create_initial_data(sender, **kwargs):
    if sender.name == 'journal':
        DescentType = apps.get_model('journal', 'DescentType')
        Ritual = apps.get_model('journal', 'Ritual')
        
        # Create all descent types first
        type_data = [
            {
                'type': 'EMOTIONAL',
                'name': 'Emotional',
                'description': 'A journey to explore and process emotions'
            },
            {
                'type': 'MENTAL',
                'name': 'Mental',
                'description': 'A journey to explore thoughts and mental patterns'
            },
            {
                'type': 'SPIRITUAL',
                'name': 'Spiritual',
                'description': 'A journey to explore spiritual experiences'
            },
            {
                'type': 'PHYSICAL',
                'name': 'Physical',
                'description': 'A journey to explore physical sensations'
            },
            {
                'type': 'EXISTENTIAL',
                'name': 'Existential',
                'description': 'A journey to explore life\'s big questions'
            }
        ]
        
        # Create all descent types
        for data in type_data:
            DescentType.objects.create(**data)
        
        # Get all types after creation
        emotional_type = DescentType.objects.get(type='EMOTIONAL')
        mental_type = DescentType.objects.get(type='MENTAL')
        spiritual_type = DescentType.objects.get(type='SPIRITUAL')
        physical_type = DescentType.objects.get(type='PHYSICAL')
        existential_type = DescentType.objects.get(type='EXISTENTIAL')

        # Create rituals
        rituals = [
            # Emotional Rituals
            {
                'name': 'Grounding Exercise',
                'type': 'PRE',
                'description': 'A ritual to help you ground yourself before emotional exploration',
                'instructions': 'Sit comfortably, close your eyes, and take deep breaths. Focus on your breath and your physical sensations.',
                'descent_type_id': emotional_type.id
            },
            {
                'name': 'Emotional Release',
                'type': 'DURING',
                'description': 'A ritual to help process and release emotions',
                'instructions': 'Write down any emotions you\'re feeling. Allow yourself to fully experience them without judgment.',
                'descent_type_id': emotional_type.id
            },

            # Mental Rituals
            {
                'name': 'Mindfulness Meditation',
                'type': 'PRE',
                'description': 'Prepare your mind for deep reflection',
                'instructions': 'Sit quietly and focus on your breath. Clear your mind of distractions.',
                'descent_type_id': mental_type.id
            },
            {
                'name': 'Thought Journaling',
                'type': 'DURING',
                'description': 'A ritual to explore your thoughts',
                'instructions': 'Write down any thought that come to mind. Don\'t censor or judge them.',
                'descent_type_id': mental_type.id
            },

            # Spiritual Rituals
            {
                'name': 'Centering Prayer',
                'type': 'PRE',
                'description': 'Prepare your spirit for exploration',
                'instructions': 'Sit in a quiet place and open your heart to divine presence.',
                'descent_type_id': spiritual_type.id
            },
            {
                'name': 'Spiritual Reflection',
                'type': 'DURING',
                'description': 'A ritual to connect with your spiritual self',
                'instructions': 'Reflect on your spiritual beliefs and xperiences.',
                'descent_type_id': spiritual_type.id
            },

            # Physical Rituals
            {
                'name': 'Body Scan',
                'type': 'PRE',
                'description': 'Prepare your body for physical exploration',
                'instructions': 'Lie dowmn comfortably and scan your body for tension.',
                'descent_type_id': physical_type.id
            },
            {
                'name': 'Physical Release',
                'type': 'DURING',
                'description': 'A ritual to release physical tension.',
                'instructions': 'Move your body in ways that feel natural and freeing',
                'descent_type_id': physical_type.id
            },

            # Existential Rituals
            {
                'name': 'Silent Contemplation',
                'type': 'PRE',
                'description': 'Prepare for deep existential exploration',
                'instructions': 'Sit in silence and open yourself to big questions.',
                'descent_type_id': existential_type.id
            },
            {
                'name': 'Life Reflection',
                'type': 'DURING',
                'description': 'A ritual to explore life\'s meaning.',
                'instructions': 'Reflect on your life\'s purpose and values',
                'descent_type_id': existential_type.id
            }
        ]


        for ritual_data in rituals:
            Ritual.objects.get_or_create(**ritual_data)

@receiver(post_migrate)
def create_initial_data_signal(sender, **kwargs):
    create_initial_data(sender, **kwargs)