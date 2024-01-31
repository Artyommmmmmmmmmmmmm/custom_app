from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives

class Article(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )


    title = models.CharField(max_length=64)

    text = RichTextUploadingField(blank=True, null=True)

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='articles'
    )

    def __str__(self):
        return self.title
     


    def get_absolute_url(self):
        return reverse('change', args=[str(self.id)]) 
    
class Comment(models.Model):
    
    text = models.TextField()

    replied = models.BooleanField(default=False)
    
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='comments',     
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.title
    
class Category(models.Model):
    
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title