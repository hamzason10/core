from django.contrib import admin

from app.models import FaceEnroll , FaceDetection

# Register your models here.
@admin.register(FaceEnroll)
class FaceEnrolladmin(admin.ModelAdmin):
    list_display=['id','name','img']


@admin.register(FaceDetection)
class FaceDetectionadmin(admin.ModelAdmin):
    list_display=['id','face_enroll','img','date']