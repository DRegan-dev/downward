from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import DescentSessionForm, EntryForm
from ..models import DescentType, DescentSession

User = get_user_model()

class TestDescentSessionForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.descent_type = DescentType.objects.create(
            name = 'Test Descent',
            type='Emotional',
            is_active=True
        )
        self.inactive_descent_type = DescentType.objects.create(
            name='Inactive Descent',
            type='EMOTIONAL',
            is_active=False
        )

    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'descent_type': self.descent_type.id,
            'notes': 'Some test notes' 
        }
        form = DescentSessionForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """Test form with missing required fields"""
        form_data = {}
        form = DescentSessionForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('descent_type', form.errors)

    def test_form_with_inactive_descent_type(self):
        """Test form with inactive descent type"""
        form_data = {
            'descnet_type': self.inactive_descent_type.id, 
            'title': 'Test Session'       
        }
        form = DescentSessionForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('descent_type', form.errors)


class TestEntryForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testUser',
            email='test@example.com',
            password='testpass123'
        )
        self.descent_type = DescentType.objects.create(
            name='Test Descent',
            description='Test description',
            type='EMOTIONAL',
            is_active=True
        )
        self.session = DescentSession.objects.create(
            user=self.user,
            descent_type=self.descent_type,
            notes="Test Notes"
        )

    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'content': 'Test content',
            'emotion_level': 3,
            'reflection': 'Test refelection'
        }
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """Test form with missing required fields"""
        form_data = {}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertIn('emotion_level', form.errors)

    def test_emotion_level_validation(self):
        """Test emotion level validation"""
        # Test below minimum
        form_data = {
            'content': 'Test content',
            'emotion_level': 0,
            'reflection': 'Test reflection'
        }
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('emotion_level', form.errors)

        # Test above maximum

        form_data['emotion_level'] = 11
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('emotion_level', form.errors)

        # Test valid range
        for level in range(1, 11):
            form_data['emotion_level'] = level
            form = EntryForm(data=form_data)
            self.assertTrue(form.is_valid(), f"Emotion level {level} should be valid")

    def test_reflection_not_required(self):
        """Test that reflection is not a required field"""
        form_data = {
            'content': 'Test content',
            'emotion_level': 5,
            'reflection': ''
        }
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())                    