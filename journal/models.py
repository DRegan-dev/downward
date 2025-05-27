from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class DescentType(models.Model):
    TYPE_CHOICES = [
        ('EMOTIONAL', 'Emotional'),
        ('MENTAL', 'Mental'),
        ('SPIRITUAL', 'Spiritual'),
        ('PHYSICAL', 'Physical'),
        ('EXISTENTIAL', 'Existential')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choice=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
class DescentSession(models.Model):
    STATUS_CHOICES = [
        ('STARTED', 'Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descent_type = models.ForeignKey(DescentType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='STARTED')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    abandoned_at = models.DateTimeField(null=TRUE, blank=True)
    notes = models.TextField(blank=True)

    @property
    def duration(self):
        if self.status == 'COMPLETED':
            return self.completed_at - self.started_at
        elif self.status == 'ABANDONED':
            return self.abandoned_at - self.started_at
        return timezone.now() - self.started_at

    def __str__(self):
        return f"{self.user.username}'s {self.descent_type.name} session"
    
class Entry(models.Model):
    session = models.ForeignKey(DescentSession, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    emotion_level = models.IntegerField(default=5) # 1-10 scale
    reflection = models.TextField(blank=True)

    def __str__(self):
        return f"Entry for {self.session}"
    
class Ritual(models.Model):
    TYPE_CHOICES = [
        ('PRE', 'Pre-Descent'),
        ('DURING', 'During Descent'),
        ('POST', 'Post-Descent')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
