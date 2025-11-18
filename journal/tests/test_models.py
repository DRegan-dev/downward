from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import DescentType, DescentSession, Entry

User = get_user_model()

class TestDescentType(TestCase):
    def test_create_descent_type(self):
        """ Test creating a new descent type """
        descent_type = DescentType.objects.create(
            name="Test Descent",
            description="A test descent type",
            type='EMOTIONAL'
        )
        self.assertEqual(str(descent_type), "Test Descent")
        self.assertEqual(descent_type.description, "A test descent type")
        self.assertEqual(descent_type.is_active, True)

class TestDescentSession(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.descent_type = DescentType.objects.create(
            name="Test Descent",
            type='EMOTIONAL',
            description="Test description"
        )

    def test_create_descent_session(self):
        """Test creating a new descent session"""
        session = DescentSession.objects.create(
            user=self.user,
            descent_type=self.descent_type,
        )
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.descent_type, self.descent_type)
        self.assertEqual(session.status, 'STARTED')
        self.assertIsNotNone(session.started_at)

class TestEntry(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.descent_type = DescentType.objects.create(
            name='Test Descent',
            type='EMOTIONAL',
            description="Test description"
            
        )
        self.session = DescentSession.objects.create(
            user=self.user,
            descent_type=self.descent_type,
        )

    def test_create_entry(self):
        """ Test creating a new journal entry """
        entry = Entry.objects.create(
            session=self.session,
            content="Test Content",
            emotion_level=3,
            reflection="Test reflection"
        )
        self.assertEqual(entry.content, "Test Content")
        self.assertEqual(entry.emotion_level, 3)
        self.assertEqual(entry.reflection, "Test reflection")
        self.assertEqual(entry.session, self.session)