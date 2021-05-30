from django import forms
from .models import BlogPost

class FormPost(forms.ModelForm):

    # tags = forms.ChoiceField(choices=["Tech", "Art"])

    class Meta:
        model = BlogPost
        fields = ['title', 'short_desc', 'image', 'author', 'content', 'time', 'date', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog title' , 'required': 'true'}),
            'short_desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog description', 'required': 'true'}),
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog image', 'required': 'true'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog author name', 'required': 'true'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Blog content', 'required': 'true', 'id': 'textContent', 'oninput':'onInput()'}),
            'time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Reading time', 'required': 'true'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date yyyy-mm-dd', 'input':'date', 'required': 'true'}),
            'tags': forms.Select(attrs={'class': 'form-control'}),
        }