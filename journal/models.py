from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DescentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class DescentSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descent_type = models.ForeignKey(DescentType, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.descent_type.name} session"
    
class Entry(models.Model):
    session = models.ForeignKey(DescentSession, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry for {self.session}"
    
class Ritual(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices = [
        ('candle', 'Candle Lighting'),
        ('music', 'Music'),
        ('silence', 'Silence Timer'),
        ('custom', 'Custom Ritual')

    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
