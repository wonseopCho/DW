from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Comment, Board

class CommentForm(forms.ModelForm):	
	class Meta:
		model = Comment
		#fields = '__all__'
		fields = ['message', 'board', 'parent']

class BoardForm(forms.ModelForm):
	class Meta:
		model = Board
		fields = ['b_title', 'video', 'rating', 'text']
		widgets = {
				'text' : SummernoteWidget(attrs={'width': '100%', 'height': '400px'},)
		}