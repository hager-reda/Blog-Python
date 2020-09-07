from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
	category_name = models.CharField(max_length=200)
	users_id = models.ManyToManyField(User)

	def __str__(self):
		return self.category_name
    
		


class Post(models.Model):
	title=models.CharField(max_length=200)
	content=models.TextField()
	time_created = models.DateTimeField(auto_now_add=True)
	author= models.ForeignKey(User, on_delete=models.DO_NOTHING )
	tag_post = models.CharField(max_length=200)
	photo = models.ImageField(blank=True,null=True)
	category_type = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
	def __str__(self):
		return self.content



# class poststable(models.Model):
# 	# postId = models.CharField(primary_key=True, max_length=10)
# 	pass
		

class comments(models.Model):
	commentText = models.TextField(max_length=100)
	commentTime = models.DateTimeField(auto_now_add=True)
	postId = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
	userId = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


	def __str__(self):
		return self.commentText

		

class replys(models.Model):
	replyText = models.CharField(max_length=100)
	replyTime = models.DateTimeField(auto_now_add=True)
	commentId = models.ForeignKey(comments, on_delete=models.CASCADE)
	postId = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
	userId = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return  self.replyText


class likes(models.Model):
	like = models.CharField(
	        max_length=7,
	        choices=(
	            ("like", "like"),
	            ("dislike", "dislike"),
	            ("none", "none"),
	        ),default="none"
	    )
	postId = models.ForeignKey(Post, on_delete=models.CASCADE)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.like

class subscribe(models.Model):
	
	category_id = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
	users_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	subscribe = models.BooleanField(default=True)
	def __str__(self):
		return self.subscribe

		

class forbWords(models.Model):
	forbWord = models.CharField(max_length=30, default="rude")
	def __str__(self):
		return self.forbWord
		