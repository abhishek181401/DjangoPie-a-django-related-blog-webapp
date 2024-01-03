from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,unique=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag,self).save(*args,**kwargs)

class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="profile_images/",blank=True,null=True)
    bio = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    def save(self,*args,**kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
            return super(Profile,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.user.first_name


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField(null=True,blank=True,upload_to='images/')
    tags = models.ManyToManyField(Tag,blank=True,related_name='post')
    view_count = models.IntegerField(null=True,blank=True)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    bookmarks = models.ManyToManyField(User,default=None,null=True,blank=True,related_name="bookmarks")
    likes = models.ManyToManyField(User,default=None,blank=True,null=True,related_name="likes")

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True,related_name="replies")

class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    about = models.TextField()
    
    class Meta:
        verbose_name_plural ="Website Meta"
       
 