from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_location = models.CharField(max_length=200)
    company_description = models.TextField()

    def __str__(self):
        return f"{self.company_name} - {self.company_location}"


class Job(models.Model):
    job_title = models.CharField(max_length=200)
    job_description = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    def __str__(self):
        return self.job_title

# models.py

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.company.company_name} ({self.job.job_title})"


from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('jobseeker', 'Job Seeker'),
            ('employer', 'Employer')
        ]
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"