from django.db import models
from django.contrib.auth.models import User
from file_manager.models import Folder, File

class PlagiarismReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    report_name = models.CharField(max_length=255)

class PlagiarismReportDetail(models.Model):
    report = models.ForeignKey(PlagiarismReport, on_delete=models.CASCADE, related_name='details')
    file1 = models.ForeignKey(File, on_delete=models.CASCADE, related_name='file1_details')
    file2 = models.ForeignKey(File, on_delete=models.CASCADE, related_name='file2_details')
    similarity_score = models.FloatField()
