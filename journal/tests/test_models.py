from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import DescentType, DescentSession, Entry

User = get_user_model()

class TestDescentType(TestCase):
    def test_create_descent_type(self):
        """ Test creating a new descent type """
        descent_type = DescentType.objects.create(
            name="Test Descent",
            description="A test descent type"
        )
        self.assertEqual(str(descent_type), "Test Descent")
        self.assertEqual(descent_type.description, "A test descent type")
        self.assertEqual(descent_type.is_active)