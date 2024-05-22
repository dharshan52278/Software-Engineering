from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Course(models.Model):
  course_name = models.CharField(max_length=100)
  credit = models.PositiveIntegerField()
  description = models.CharField(max_length=300)
  images = models.ImageField(upload_to='images')
  enrolled_students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE)
  topics = models.ManyToManyField(Topic, related_name='courses')


  def __str__(self):
        return str(self.course_name)

class Info(models.Model):
  institution_name = models.CharField(max_length=50)
  role = models.CharField(max_length=50)
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class StudentCourseProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_progress')
    completed_topics = models.ManyToManyField(Topic, related_name='completed_by_students')

    class Meta:
        unique_together = ('student', 'course')

    @property
    def progress(self):
        total_topics = self.course.topics.count()
        if total_topics == 0:
            return 0
        completed_topics_count = self.completed_topics.count()
        return (completed_topics_count / total_topics) * 100

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name} - {self.progress}%"

class File(models.Model):
    file = models.FileField(upload_to = 'uploads')        




          