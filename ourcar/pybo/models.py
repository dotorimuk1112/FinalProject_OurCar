from django.db import models
from common.models import CustomUser
from config.settings import MEDIA_ROOT

class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(CustomUser, related_name='voter_question')  # 추천인 추가
    
    def __str__(self):
        return self.subject



class Answer(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(CustomUser, related_name='voter_answer')
    
class UploadedImage(models.Model):
    uploadedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')
    processedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')
    has_car = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)


class UploadedImage2(models.Model):
    uploadedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')
    processedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')  # processedimage 필드 추가
    has_car = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'pybo_uploadedimage2'