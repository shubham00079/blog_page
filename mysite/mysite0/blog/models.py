from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    # here author is connected to a superuser
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # can change the timezone as per our requirement in settings.py
    published_date = models.DateTimeField(blank=True,null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

        # it is not necessary to publish at the time of creation
        # we have option to publish it later, so when clicking publish
        # then it save the publish time.

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
        # only showing(filtering) those comments that are approved by the admin.

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})
        # after posting takes back to post_detail of that particular primary key

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')
    # after commenting takes back to post list.

    def __str__(self):
        return self.text
