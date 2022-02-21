from django.forms import ModelForm,models
from .models import Project,Review
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        #fields = '__all__'
        fields = ['name','image','description','demo_link','source_link','Tag']
        widgets={
            'Tag':forms.CheckboxSelectMultiple(),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'value':'Add your vote for the Comment',
            'body':'Add your comments here'
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for label,field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text','placeholder':'Enter Value'})



        #self.fields['title'].widget.attrs.update({'class':'input'})
    


    
