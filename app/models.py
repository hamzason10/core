from django.db import models

# Create your models here.

class FaceEnroll(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to ='user_faces')
    feature = models.TextField()


class FaceDetection(models.Model):
    face_enroll = models.ForeignKey(FaceEnroll,on_delete=models.CASCADE,null=True,blank=True)
    img = models.ImageField(upload_to ='user_matched_faces')
    date = models.DateTimeField(auto_now_add=True)
