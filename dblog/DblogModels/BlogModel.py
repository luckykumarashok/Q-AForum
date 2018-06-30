from django.db import models
from django.utils import timezone
from django.conf import   settings

class Website(models.Model):
    name =  models.CharField(max_length=128)
    desc  = models.TextField(default=None)    
    url= models.URLField(default=None)
    email=models.EmailField(default=None)
    createdOn = models.DateTimeField()
    modifiedOn = models.DateTimeField()
    createdBy= models.ForeignKey(settings.AUTH_USER_MODEL) 
    
    
class Subject(models.Model):   
    subName =  models.CharField(max_length=256)
    subDesc = models.TextField()
    createdOn = models.DateTimeField()
    modifiedOn = models.DateTimeField()
    createdBy= models.ForeignKey(settings.AUTH_USER_MODEL) 
    
    def getSubjectList(self):
        return Subject.objects.all()
       
class TopicManager(models.Manager):  
    class Meta:
        ordering =[ 'id']
    
    def createTopic(self,subject_id ,topicDict, user):   
        topic = self.model()
        topic.subject_id=subject_id
        topic.topicName=topicDict['Title']
        topic.type=topicDict['Type']
        topic.modifiedOn= timezone.now()
        topic.createdOn= timezone.now()
        topic.createdBy = user
        topic.save()
        return topic.id        
    
class Topic(models.Model):
    subject = models.ForeignKey('Subject')
    topicName =  models.CharField(max_length=256,default=None)
    type =       models.IntegerField(default=1)
    verified  = models.BooleanField(default=False)
    rating    = models.IntegerField(default=0) 
    publish = models.BooleanField(default=False)
    createdOn = models.DateTimeField()
    modifiedOn = models.DateTimeField()
    createdBy= models.ForeignKey(settings.AUTH_USER_MODEL)
    
    def getToipcList(self,sub_id):
        return Topic.objects.all().filter(subject = sub_id).order_by('id')   
    
    objects=TopicManager()

class SubTopicManager(models.Manager):
    def createSubTopic(self,subtopicList,topicid,user): 	    
        for subtopicDict in subtopicList:
            subtopic= SubTopic() 
            subtopic.topic_id =  topicid
            if subtopicDict =={} or   subtopicDict['Details'] is None:
			    subtopic.subtopicDesc ='N/A'  
            else :  				
                subtopic.subtopicDesc =  subtopicDict['Details']
            subtopic.modifiedOn =  timezone.now()
            subtopic.createdOn=timezone.now()
            subtopic.createdBy = user
            subtopic.save()
            
class SubTopic(models.Model):  
    topic = models.ForeignKey('Topic')
    subtopicDesc = models.TextField( )
    createdOn = models.DateTimeField()
    modifiedOn = models.DateTimeField()
    createdBy= models.ForeignKey(settings.AUTH_USER_MODEL)
    class Meta:
        ordering=['id']
    objects = SubTopicManager() 

       


     



 
