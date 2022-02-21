from django.utils import timezone
from django.db import models
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/',null=True,blank=True,default="photosdefault.jpg")
    description = models.TextField(null=True,blank=True)
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    Tag = models.ManyToManyField('Tag',blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Published = models.DateTimeField(default = timezone.now)
    Vote_total = models.IntegerField(default=0,null=True,blank=True)
    Vote_ratio = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.name
    
    @property
    def reviewers(self):
        return self.review_set.all().values_list('owner__id',flat=True)

    @property
    def getVoteCount(self):

        reviews = self.review_set.all()
        upVotes=reviews.filter(value='up')
        upcount = upVotes.count()
        totalcount = reviews.count()
        self.Vote_total= totalcount
        self.Vote_ratio=(upcount/totalcount)*100
        self.save()

class Review(models.Model):
    vote_type = [('up','Up Vote'),
                  ('down','Down Vote'),]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=100,choices=vote_type)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value
    
    class Meta:
        unique_together=[['project','owner']]

class Tag(models.Model):
    name = models.CharField(max_length=100)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
