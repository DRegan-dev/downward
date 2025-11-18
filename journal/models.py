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
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='EMOTIONAL')
    is_active = models.BooleanField(default=True, help_text='Designates whether this descent type is active and can be selected.')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Descent Type'
        verbose_name_plural = 'Descent Types'
        ordering = ['name']
    
class DescentSession(models.Model):
    STATUS_CHOICES = [
        ('STARTED', 'Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descent_type = models.ForeignKey(DescentType, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='STARTED')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    abandoned_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    @property
    def duration(self):
        if self.completed_at:
            return self.completed_at - self.started_at
        elif self.abandoned_at:
            return self.abandoned_at - self.started_at
        return timezone.timedelta()

    def __str__(self):
        return f"{self.user.username}'s {self.descent_type.name} descent"
    
class Entry(models.Model):
    session = models.ForeignKey(DescentSession, on_delete=models.CASCADE, related_name='entries')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    emotion_level = models.IntegerField(default=5) # 1-10 scale
    reflection = models.TextField(blank=True)

    def __str__(self):
        return f"Entry for {self.session}"
    
