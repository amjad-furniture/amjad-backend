from django.db import models


class Support(models.Model):
    """
    Model for support requests.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Request for {self.phone_number}"
    
    class Meta:
        ordering = ['-created_at']
