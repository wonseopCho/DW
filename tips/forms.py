from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Comment, Category, Article, Listicle

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['category', 'title', 'video', 'text']
		widgets = {
				'text' : SummernoteWidget(attrs={'width': '100%', 'height': '400px'}),
		}


class CommentForm(forms.ModelForm):	
	class Meta:
		model = Comment
		#fields = '__all__'
		fields = ['message','article', 'parent']

class ListicleForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'instance' in kwargs and kwargs['instance'] is not None:
			category = kwargs['instance'].category
			category_id = Category.objects.get(category=category).id
			self.fields['articles'].queryset = self.fields['articles'].queryset.filter(category=category_id)
		
	class Meta:
		model = Listicle
		fields = '__all__'

	class Media:
		js = ['js/tips/listicle.js']
