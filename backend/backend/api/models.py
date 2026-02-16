from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.contrib import admin


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
from django.db import models
@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    """
    When a new User is created, if is_staff=False, create a Student record.
    """
    if created and instance.is_staff == 0:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_student(sender, instance, **kwargs):
    """
    Save the linked Student object when User is saved.
    """
    if hasattr(instance, 'student'):
        instance.student.save()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(max_length=500, blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    playlist_url = models.URLField(max_length=500, blank=True, null=True, default="")


    def get_embed_url(self):

        # ✅ If playlist exists, give playlist embed
        if self.playlist_url:
            if "list=" in self.playlist_url:
                playlist_id = self.playlist_url.split("list=")[1].split("&")[0]
                return f"https://www.youtube.com/embed/videoseries?list={playlist_id}"

        # ✅ If single video exists
        if self.video_url:
            if "youtu.be/" in self.video_url:
                video_id = self.video_url.split("youtu.be/")[1].split("?")[0]
                return f"https://www.youtube.com/embed/{video_id}?rel=0"

            if "watch?v=" in self.video_url:
                video_id = self.video_url.split("watch?v=")[1].split("&")[0]
                return f"https://www.youtube.com/embed/{video_id}?rel=0"

            if "embed/" in self.video_url:
                return self.video_url

        return None

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.course}"



admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)         
# Create your models here.
