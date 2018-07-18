from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Comment, Qna

class CommentForm(forms.ModelForm):	
	class Meta:
		model = Comment
		#fields = '__all__'
		fields = ['message','qna', 'parent']

class QnaForm(forms.ModelForm):
	class Meta:
		model = Qna
		fields = ['q_title', 'video', 'rating', 'text']
		widgets = {
				'text' : SummernoteWidget(attrs={'width': '100%', 'height': '400px'},)
		}