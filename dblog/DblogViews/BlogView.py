from django.shortcuts import render 
from dblog.DblogForms.BlogForm import   * 
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect  
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory 
from django.contrib.auth import authenticate, login, logout
from django.utils import   timezone
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
#@login_required
def index(request):    
    subjectList= Subject().getSubjectList()
    website= Website.objects.get(pk=1)
    return render(request,'dblog/index.html',{'website':website,'subjectList':subjectList})
  
class subjectView(View):
    def get(self,request,subject_id ):
        website= Website.objects.get(pk=1)
        subId=subject_id
        topiclist= Topic().getToipcList(subId)
        
        
        subjectList= Subject().getSubjectList()
        try: subject= Subject.objects.get(pk=subId)
        except: subject=None
        try :
             topic =  Topic.objects.all().filter(subject=subId ).order_by('id').first()
             SubTopic_list =  topic.subtopic_set.all()
        except Exception as e:
             topic=None  
             SubTopic_list=None        
        return render(request,'dblog/category.html' ,{ 'website':website,'subject': subject  ,'topic':topic,'SubTopic_list':SubTopic_list, 'subjectList':subjectList,'topiclist':topiclist})
       
     
def readTopicByPagination(request,subject_id,pageNum):
    website= Website.objects.get(pk=1)
    topiclist= Topic().getToipcList(subject_id)
    subjectList= Subject().getSubjectList()
    paginator = Paginator(topiclist,1) 
    try:
        topics = paginator.page(pageNum)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        topics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        topics = paginator.page(paginator.num_pages)

    try: subject= Subject.objects.get(pk=subject_id)
    except: subject=None
    try : 
        topic =  topics[0]
        SubTopic_list =   topic.subtopic_set.all()
    except Exception as ex: 
        topic=None
        SubTopic_list =None
    return render(request,'dblog/readTopic.html', {'website':website,'subject': subject,  'cur_topic':topic ,'topics':topics,'SubTopic_list':SubTopic_list, 'subjectList':subjectList,'topiclist':topiclist})
def readTopicById(request,subject_id,topic_id):
    website= Website.objects.get(pk=1)
    topiclist= Topic().getToipcList(subject_id)
    subjectList= Subject().getSubjectList()
     
    try: subject= Subject.objects.get(pk=subject_id)
    except: subject=None
    try : 
        topic= Topic.objects.get(pk=topic_id)
        
        SubTopic_list =   topic.subtopic_set.all()
    except Exception as ex: 
        topic=None
        SubTopic_list =None
    return render(request,'dblog/readTopic.html', {'website':website,'subject': subject, 'cur_topic':topic  ,  'SubTopic_list':SubTopic_list, 'subjectList':subjectList,'topiclist':topiclist})
    
class createTopicView(View):  
    def __init__(self):
        super(createTopicView,self).__init__()
        self.subjectList= Subject().getSubjectList() 
        self.topic_id=''      
        self.TopicFormSet = formset_factory(TopicForm  )
        self.SubjectFormSet = formset_factory(SubjectForm  )    
        self.SubTopicFormSet = formset_factory(SubTopicForm  )
        website= Website.objects.get(pk=1)
        
           
    def post(self, request, *args, **kwargs):          
        subjectFormSet = self.SubjectFormSet(request.POST)
        topicformset = self.TopicFormSet(request.POST)
        subtopicformset = self.SubTopicFormSet(request.POST)
        if subjectFormSet.is_valid() and topicformset.is_valid():
            topic_id = Topic.objects.createTopic(subjectFormSet.cleaned_data[0]['Category'],topicformset.cleaned_data[0], request.user)
            if topic_id is not None: 
                if subtopicformset.is_valid():
                    SubTopic.objects.createSubTopic(subtopicformset.cleaned_data,topic_id,request.user)
        return HttpResponseRedirect('/dblog/topic/'+subjectFormSet.cleaned_data[0]["Category"]+'/%s'%   (topic_id))
   
    def get(self, request, *args, **kwargs):    
        website= Website.objects.get(pk=1)     
        subject = Subject.objects.all()
        SUBJECT_CHOICE= [('','SELECT CATEGORY')]
        for sub in subject:
            SUBJECT_CHOICE.append((sub.id,sub.subName))
        subject_id = self.SubjectFormSet.form.base_fields['Category']
        subject_id.choices=SUBJECT_CHOICE    
        topicformset = self.TopicFormSet()
        topic_type=topicformset.form.base_fields['Type']
        topic_type.choices=(('','SELECT Type'),(1,'Tutorial'), (2, 'Question'))
        subtopicformset = self.SubTopicFormSet()
        return render(request, "dblog/addNewTopic.html", {'website':website, "topicformset": topicformset,'subtopicformset':subtopicformset, 'subjectList':self.subjectList,'SubjectFormSet':self.SubjectFormSet })
    
  
class editTopicView( View ):      
    def __init__(self):
        self.editTopicSet =  modelformset_factory(Topic ,form = TopicModelForm,  extra=0)    
         
    def post(self,request,subject_id,topic_id): 
        topicformset=self.editTopicSet(request.POST )
        if topicformset.is_valid():
            topicformset.save()  
        return HttpResponseRedirect('/dblog/topic/%s/%s' % (subject_id,topic_id))
                      
    def get(self,request,subject_id,topic_id): 
        website= Website.objects.get(pk=1) 
        editTopic=self.editTopicSet(queryset=Topic.objects.filter(pk=topic_id) )
        try: topic=Topic.objects.get(pk=topic_id) 
        except Exception as  ex : 
             topic=None
        return render(request, "dblog/editPost.html", {'website':website,'topic':topic,'editTopic':editTopic, 'subjectList': Subject().getSubjectList()})   
    


class editDetailsView(View):   
    def __init__(self):   
        self.editSubTopicSet =  modelformset_factory(SubTopic,form =SubTopicModelForm, extra=0) 
             
    def post(self,request,subject_id,topic_id):
        subtopicformset = self.editSubTopicSet(request.POST)
        if subtopicformset.is_valid():
            subtopicformset.save()      
        return HttpResponseRedirect('/dblog/topic/%s/%s' % (subject_id,topic_id)) 
                   
    def get(self,request,subject_id,topic_id): 
        website= Website.objects.get(pk=1) 
        editSubTopic = self.editSubTopicSet(queryset= SubTopic.objects.all().filter(topic=topic_id))
        topic=Topic.objects.all().get(pk=topic_id)          
        return render(request, "dblog/editPost.html", {'website':website,'topic':topic,'editSubTopic':editSubTopic, 'subjectList': Subject().getSubjectList()})   




