from django.db import models
import os
# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='photos/')  # For storing facial images

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.date}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='photos/')  # For storing images
    face_encoding = models.BinaryField(blank=True, null=True)  # Store face encoding

    def save(self, *args, **kwargs):
        # Generate a student ID if not provided
        if not self.student_id:
            self.student_id = f"STU{self.pk or ''}{os.urandom(4).hex()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name