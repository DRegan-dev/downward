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

class TestDescentSession(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.descent_type = DescentType.objects.create(name="Test Descent")

    def test_create_descent_session(self):
        """Test creating a new descent session"""
        session = DescentSession.objects.create(
            user=self.user,
            descent_type=self.descent_type,
            title="Title Session"
        )
        self.assertEqual(str(session), f"{self.user.username}'s {self.descent_type.name}")
        self.assertEqual(session.status, 'IN_PROGRESS')

class TestEntry(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.descent_type = DescentType.objects.create(name='Test Descent')
        self.session = DescentSession.objects.create(
            user=self.user,
            descent_type=self.descent_type,
            title="Test Session"
        )

    def test_create_entry(self):
        """ Test creating a new journal entry """
        entry = Entry.objects.create(
            session=self.session,
            content="Test Content",
            emotion_level=3,
            reflection="Test reflection"
        )
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.emotion_level, 3)
        self.assertEqual(entry.reflection, "Test reflection")