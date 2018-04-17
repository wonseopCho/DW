from django import forms
from .models import Comment, Category, Article, Listicle

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
