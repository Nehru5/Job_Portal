from django.db import models
from recruiter_app.models import JobApplied, Recruiter
from candidate_app.models import Candidate

class Message(models.Model):
    application = models.ForeignKey(JobApplied, on_delete=models.CASCADE, related_name="messages")
    
    SENDER_CHOICES = [
        ("candidate", "Candidate"),
        ("recruiter", "Recruiter"),
    ]
    
    sender_type = models.CharField(max_length=20, choices=SENDER_CHOICES)
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, null=True, blank=True)
    
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender_type} - {self.message[:20]}"