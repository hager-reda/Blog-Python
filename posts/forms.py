from django import forms
from .models import comments, likes, Post, Categories, forbWords

class commentForm(forms.ModelForm):
	class Meta:
		model = comments
		fields = ('commentText',)

class likeForm(forms.ModelForm):
	class Meta:
		model = likes
		fields = ('like',)

class postForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','content','tag_post','category_type','photo')


class wordForm(forms.ModelForm):
	class Meta:
		model = forbWords
		fields = ('forbWord',)

class categoryForm(forms.ModelForm):
	class Meta:
		model = Categories
		fields = ('category_name',)
