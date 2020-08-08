from django.db import models
from taggit.managers import TaggableManager
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

from django.utils.text import slugify

class Categories(models.Model):
    catergory_name = models.CharField(max_length=15, null=False,default='Default Choice')

    def __str__(self):
        return self.catergory_name


STATUS_CHOICES = (
 ('draft', 'Draft'),
 ('published', 'Published'),
 )

# Post model
class Post(models.Model):
    slug = models.SlugField(max_length=250, unique_for_date='published_date')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    choices = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, default=True)
    post_image= models.ImageField(default=False, null=False)
    text = RichTextField(blank=True,null=True)
    #text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    tags = TaggableManager()


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    #It will get the absolute url in post detail
    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.id])

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Post,self).save(*args,**kwargs)



# Comment model
class Comment(models.Model):

     post = models.ForeignKey(Post, on_delete=models.CASCADE ,related_name='comments')
     name = models.CharField(max_length=80)
     email = models.EmailField()
     body = models.TextField()
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     active = models.BooleanField(default=True)
     class Meta:
         ordering = ('created',)
     def __str__(self):
         return 'Comment by {} on {}'.format(self.name, self.post)





