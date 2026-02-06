from django.db import models

class AnalysisRecord(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary_data = models.JSONField() 
    def __str__(self):
        return f"Analysis {self.id} - {self.uploaded_at}"