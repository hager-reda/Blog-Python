from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import comments, replys, Post, likes, forbWords,subscribe,Categories
from .forms import commentForm,likeForm, postForm , wordForm, categoryForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


#to 5 posts in lamding page
def showPosts(request):
  if request.user.is_authenticated:
    allcomments=[]
    allreplys=[]
    all_posts = Post.objects.all().order_by('-time_created')
    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page')

    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)



    for x in all_posts:
      alldislikes = likes.objects.filter(postId=x.id, like="dislike").count()
      if alldislikes==10:
        x.delete();
    allcomments = comments.objects.filter(postId=1).order_by('commentTime')
    allreplys = replys.objects.filter(postId=1).order_by('replyTime')
    all_cat=Categories.objects.all()
    sub_cat=Categories.objects.filter(users_id=request.user)
    context = {'all_posts':all_posts, 'comments': allcomments, 'replys': allreplys,'all_cat':all_cat,'sub_cat':sub_cat}
    return render(request ,'showPosts.html' ,context)
  else:
      all_posts = Post.objects.all().order_by('-time_created')[:5]
      all_cat=Categories.objects.all()
      context = {'all_posts':all_posts,'all_cat':all_cat}
      return render(request ,'showPosts.html' ,context)

def showOnePost(request, post_id):
    x = Post.objects.get(id = post_id)
    allcomments = comments.objects.filter(postId=x.id).order_by('commentTime')
    allreplys = replys.objects.filter(postId=x.id).order_by('replyTime')
    alllikes = likes.objects.filter(postId=x.id, like="like").count()
    alldislikes = likes.objects.filter(postId=x.id, like="dislike").count()
    urlike = likes.objects.filter(postId=x.id, userId=request.user)
    all_cat=Categories.objects.all()
    sub_cat=Categories.objects.filter(users_id=request.user)

    badWords = forbWords.objects.all()
    xword = []
    for word in badWords:
        xword.append(word.forbWord)

    if request.user.is_authenticated:
      urlike = likes.objects.filter(postId=x.id, userId=request.user)

      context = {'post':x, 'comments': allcomments, 
          'replys': allreplys, 
          'likescount': alllikes, 
          'dislikescount': alldislikes,
          'urlike':urlike,
          'all_cat':all_cat,
          'sub_cat':sub_cat, 
          'forbWords': xword}
    else:
      context = {'post':x,
          'likescount': alllikes, 
          'dislikescount': alldislikes,
          'all_cat':all_cat, 
          'comments': allcomments, 
          'forbWords': xword}

    return render(request ,'showOnePost.html' ,context)

#add new post through form
def addPost(request):
  if request.user.is_authenticated:
    new_post=postForm()
    added_post=None
    if request.method=="POST":
      new_post=postForm(request.POST,request.FILES)
      if new_post.is_valid():
        added_post=new_post.save(commit=False)
        added_post.author=request.user
        added_post.save()
        return HttpResponseRedirect('/posts/')
    return render(request,'new.html',{'new_post':new_post})
  else:
    return HttpResponseRedirect('/posts/')


# when user choose specific category
def allCategoryPosts(request,cat_num):
      cat_posts = Post.objects.filter(category_type=cat_num).order_by('-time_created')
      all_cat=Categories.objects.all()
      if request.user.is_authenticated:
        sub_cat=Categories.objects.filter(users_id=request.user)
        context={'cat_posts':cat_posts,'all_cat':all_cat,'sub_cat':sub_cat}
      else:
        context={'cat_posts':cat_posts,'all_cat':all_cat}
      return render(request ,'CategotyPage.html' ,context)


#search for posts with title or tag
def searchForPost(request):
  print(request.GET.get('word'))
  term = request.GET.get('word')
  print(term)
  all_posts = Post.objects.filter(
    Q(title__icontains=term) |
    Q(tag_post__icontains=term)
    ).order_by('-time_created')
  all_cat=Categories.objects.all()
  sub_cat=Categories.objects.filter(users_id=request.user)
  context={'all_posts':all_posts,'all_cat':all_cat,'sub_cat':sub_cat}
  return render(request ,'searchPage.html' ,context)

def subcribe(request,cat_num):
  category=Categories.objects.get(id=cat_num)
  if request.POST.get('subscribe')=='0':
    category.users_id.remove(request.user)
  else:
    category.users_id.add(request.user)
    try:
    	send_mail('Confirmation','Hello! THis is GASH Blog. You have just subscribe to our blog.',
    	'gashblogiti@gmail.com',['hgrreda@gmail.com'],
    	fail_silently=False)
    except(e):
    	print(e)
  return HttpResponseRedirect('/posts/')

#========================================================
#to list all posts
def listPosts(request):
    all_posts = Post.objects.all().order_by('-time_created')
    context = {'all_posts':all_posts}
    return render(request ,'postslist.html' ,context)

def deletePost(request,post_num):
  post=Post.objects.get(id=post_num)
  post.delete()
  return HttpResponseRedirect('/posts/list/')

#edit post through form
def editPost(request,post_num):
  post=Post.objects.get(id=post_num)
  if request.method=="POST":
    new_post=postForm(requestadded_badWords.POST,request.FILES,instance=post)
    if new_post.is_valid():
      new_post.save()
      return HttpResponseRedirect('/posts/list/')
  else:
    new_post=postForm(instance=post)
  return render(request,'new.html',{'new_post':new_post}) 

#list all categories
def listCategories(request):
    all_categories = Categories.objects.all()
    context = {'all_categories':all_categories}
    return render(request ,'categorylist.html' ,context) 

#add new cat through form
def addCategory(request):
  new_cat=categoryForm()
  added_cat=None
  if request.method=="POST":
    new_cat=categoryForm(request.POST)
    if new_cat.is_valid():
      new_cat.save()
      return HttpResponseRedirect('/posts/catlist/')
  return render(request,'newcat.html',{'new_cat':new_cat})

def deleteCategory(request,cat_num):
  category=Categories.objects.get(id=cat_num)
  category.delete()
  return HttpResponseRedirect('/posts/catlist/')   

#edit post through form
def editCategory(request,cat_num):
  category=Categories.objects.get(id=cat_num)
  if request.method=="POST":
    new_cat=categoryForm(request.POST,instance=category)
    if new_cat.is_valid():
      new_cat.save()
      return HttpResponseRedirect('/posts/catlist/')
  else:
    new_cat=categoryForm(instance=category)
  return render(request,'newcat.html',{'new_cat':new_cat})    
	
#=========================================================================
def commentsReplys(request):
	allcomments = comments.objects.filter(postId=1).order_by('commentTime')
	allreplys = replys.objects.filter(postId=1).order_by('replyTime')
	# context = {'commentReply':(allcomments , allreplys)}
	context = {'comments': allcomments, 'replys': allreplys }
	return render(request, 'showPosts.html', context)



def addComment(request):
    postid = request.GET['post']
    newComment = request.GET['text']
    if newComment:
        x = Post.objects.get(id=postid)
        new_comment = comments.objects.create(postId = x, userId=request.user)
        new_comment.commentText=newComment
        new_comment.save()
        count = str(comments.objects.filter(postId=x).count())
        return HttpResponse(json.dumps({'newComment':newComment, 'count':count}))


def addReply(request):
    postid = request.GET['post']
    commentid = request.GET['comment']
    newReply = request.GET['text']
    if newReply:
        p = Post.objects.get(id=postid)
        c = comments.objects.get(id=commentid, postId=p)
        new_reply = replys.objects.create(postId = p, commentId=c, userId=request.user)
        new_reply.replyText=newReply
        new_reply.save()
        count = str(replys.objects.filter(postId=p, commentId=commentid).count())
        return HttpResponse(json.dumps({'newReply':newReply, 'count':count}))


def addLike(request):
  if request.user.is_authenticated:
    postid = request.GET['post']
    newLike = request.GET['like']
    p = Post.objects.get(id=postid)
    new_like, create = likes.objects.get_or_create(postId = p, userId=request.user)
    new_like.like=newLike
    new_like.save()
    countlike = str(likes.objects.filter(postId=p, like="like").count())
    countdislike = str(likes.objects.filter(postId=p, like="dislike").count())
    return HttpResponse(json.dumps({'newLike':newLike, 'countlike':countlike, 'countdislike':countdislike}))
  

def adminForbWords(request):
  added_badWords=None
  if request.method=="POST":
    new_badWords=wordForm(request.POST)
    if new_badWords.is_valid():
      added_badWords=new_badWords.save(commit=False)
      added_badWords.save()
      return HttpResponseRedirect('/adminForbWords/')
  else:
    new_badWords=wordForm()

  badWords = forbWords.objects.all()
  context = {'badWords':badWords,
              'form':new_badWords}
  return render(request,'forbWords.html',context)



def editWords(request, word_num):
  w = forbWords.objects.get(id=word_num)
  added_badWords=None
  if request.method=="POST":
    new_badWords=wordForm(request.POST, instance=w)
    if new_badWords.is_valid():
      added_badWords=new_badWords.save(commit=False)
      added_badWords.save()
      return HttpResponseRedirect('/adminForbWords/')
  else:
    new_badWords=wordForm()

  badWords = forbWords.objects.all()
  context = {'badWords':badWords,
              'form':new_badWords}
  return render(request,'editforbWords.html',context)


def deleteWords(request, word_num):
  badWords = forbWords.objects.filter(id=word_num)
  badWords.delete()
  return HttpResponseRedirect('/adminForbWords/')


