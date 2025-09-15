from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import DescentType, DescentSession, Entry

User = get_user_model()

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test"example.com',
            password='testpass123'
        )
        self.descent_type = DescentType.objects.create(
            name='Test Descent', 
            description='Atest descent type'
        )
        self.session = DescentSession.objects.create(
            user=self.user,
            descent_type=self.descent_type,
            title='Test Session'
        )
        self.entry = Entry.objects.create(
            session=self.session,
            content='Test content',
            emotion_level=3
        )
    
    def test_home_view(self):
        """Test the home page view"""
        response = self.client.get(reverse('journal:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/home.html')

    def test_start_descent_authenticated(self):
        """ Test starting a new descent while authenticated """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:start_descent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/start_descent.html')

    def test_start_descent_inauthenticated(self):
        """Test redirect when unauthenticated user tries to start descent"""
        response = self.client.get(reverse('journal:start_descent'))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('journal:start_descent')}"
        )

    def test_continue_descent_view(self):
        """ Test continuing a descent session """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:continue_descent.html', args=[self.session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/continue_descent.html')
        self.assertEqual(response.context['session'], self.session)

    def test_journal_history_view(self):
        """Test the journal history view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:journal_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/journal_history.html')
        self.assertIn(self.session, response.context['session'])

    def test_add_entry_view(self):
        """Test Adding a new entry"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('journal::add_entry', args=[self.session.id]),
            {
                'content': 'New test content',
                'emotion_level': 4, 
                'reflection': 'Test reflection'
            }
        )
        self.assertRedirects(
            response,
            reverse('journal:continue_descent', args=[self.session.id])
        )
        self.assertEqual(Entry.objects.count(), 2) # one from setUp, one new

    def test_edit_entry_view(self):
        """ Test editing on existing entry """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('journal:edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/edit_entry.html')

    def test_delete_entry_view(self):
        """Test deleting on entry"""
        self.client.login(username='testuser', password='testpass123')
        entry_id = self.entry_id
        session_id = self.session.id
        response = self.client.post(reverse('journal:delete_entry', args=[entry_id]))
        self.assertRedirects(
            response,
            reverse('journal:continue_descent', args=[session_id])
        )
        self.assertFalse(Entry.objects.filter(id=entry_id).exists())
