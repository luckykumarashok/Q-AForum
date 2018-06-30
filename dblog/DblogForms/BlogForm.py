from django import   forms
from django.forms import ModelForm
from dblog.DblogModels.BlogModel import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class SubjectForm(forms.Form):
    Category = forms.ChoiceField(choices=(), required=True, widget=forms.Select(attrs={'class':'form-control'})) 
	
    
class TopicForm(forms.Form):    
    Type =  forms.ChoiceField(choices=(),required=True, widget=forms.Select(attrs={'class':"form-control"})) 
    Title =  forms.CharField( widget=forms.TextInput(attrs={'class':"form-control"}) , required=True) 
 
class SubTopicForm(forms.Form):        
    Details = forms.CharField(widget=SummernoteWidget( ),required=True)   
    

class TopicModelForm(ModelForm):    
    class Meta:
        model = Topic
        fields = ['topicName' ]
        labels = {'topicName': ('Title')    }  
        labels = {'type': ('Type')    }
        widgets = {'topicName':  forms.TextInput(attrs={'class':"form-control"})       }
  
class SubTopicModelForm(ModelForm):
    class Meta:
        model = SubTopic
        fields = [  'subtopicDesc' 
                  
                  ]
        labels = {
             'subtopicDesc':('Details') 
        }
        widgets = {
            'subtopicDesc':   SummernoteWidget(attrs={'class':"form-control", 'required':True})
        }
    def __init__(self, *args, **kwargs):
        super(SubTopicModelForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.iteritems():
            self.fields[key].required = True  
            self.fields[key].blank = False  