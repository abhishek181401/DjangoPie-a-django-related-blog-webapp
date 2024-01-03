from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post,Comment,Tag,Profile,WebsiteMeta
from .forms import CommentForm,SubscribeForm,NewUserForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import authenticate, login


# Create your views here.
def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    post_tags = post.tags.all()
    comments = Comment.objects.filter(post=post,parent=None)
    
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()

    # bookmark part
    is_bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        is_bookmarked =True

    #like part
    post_is_liked =False
    if post.likes.filter(id=request.user.id).exists():
        post_is_liked = True
    likes_num = post.likes.count()


    #sidebar code
    recent_posts = Post.objects.exclude(id=post.id).order_by('-updated_at')[0:3]
    top_authors = User.objects.annotate(post_number = Count('post')).order_by('-post_number')
    all_tags = Tag.objects.all()
    
    related_posts = Post.objects.filter(author=post.author).exclude(id=post.id)[0:3]

    
    form = CommentForm()
    # if request.POST:
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            parent_obj= None
            if request.POST.get('parent'):
                #saving reply
                parent = request.POST.get('parent')
                parent_obj = Comment.objects.get(id=parent)
                if parent_obj:
                    comment_reply = commentform.save(commit=False)
                    comment_reply.post=post
                    comment_reply.parent = parent_obj
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page',kwargs={'slug':slug}))

            else:
                comment = commentform.save(commit=False)
                post_id = request.POST.get("post_id")
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page',kwargs={'slug':slug}))

    context={
        'post':post,
        'post_tags':post_tags,
        'form':form,
        'comments':comments,
        'is_bookmarked':is_bookmarked,
        'post_is_liked':post_is_liked,
        'likes_num':likes_num,
        'recent_posts':recent_posts,
        'top_authors':top_authors,
        'all_tags': all_tags ,
        'related_posts':related_posts,

    }
    return render(request,'blogapp/post.html',context)

def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in = [tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-updated_at')[0:3]
    tags = Tag.objects.all()
    context={
        "tag":tag,
        'top_posts':top_posts,
        'recent_posts':recent_posts,
        'tags':tags,
    }
    return render(request,'blogapp/tag.html',context)

def author_page(request,slug):
    profile = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by('updated_at')[0:3]
    top_authors = User.objects.annotate(post_count=Count('post')).order_by('-post_count')[0:3]

    context={
        "profile":profile,
        "top_posts":top_posts,
        "recent_posts":recent_posts,
        "top_authors":top_authors,
    }
    return render(request,'blogapp/author.html',context)


def search_page(request):
    search_query =''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)[0:9]
    context ={
            "posts":posts,

    }
    return render(request,'blogapp/search.html',context)

def about_page(request):
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context={
        "website_info":website_info
    }

    return render(request,'blogapp/about.html',context)

def register_page(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
    context={
        'form':form,
    }
    return render(request,'registration/registration.html',context)

def bookmark_blog(request,slug):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page',args=[str(slug)]))

def like_blog(request,slug):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

def bookmarked_blogs(request):
    bookmarked_blogs = Post.objects.filter(bookmarks=request.user)
    context ={
        "bookmarked_blogs":bookmarked_blogs,

    }
    return render(request,'blogapp/bookmarked_blogs.html',context)

def all_blogs(request):
    all_blogs = Post.objects.all()
    context = {
        'all_blogs':all_blogs,
    }
    return render(request,'blogapp/all_blogs.html',context)

def all_liked_blogs(request):
    all_liked_blogs = Post.objects.filter(likes=request.user)
    context = {
        'all_liked_blogs':all_liked_blogs,
    }
    return render(request,'blogapp/all_likedblogs.html',context)



def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.filter().order_by('-view_count')[0:3]
    new_posts = Post.objects.filter().order_by('updated_at')[0:3]
   

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    featured_post = Post.objects.filter(is_featured=True)

    if featured_post:
        featured_post = featured_post[0]

    subscribe_form = SubscribeForm()
    subscribe_success = None

    if request.POST:
        subscribeform = SubscribeForm(request.POST)

        if subscribeform.is_valid():
            subscribeform.save()
            request.session['subscribed'] = True
            subscribe_success = "Subscribed Successfully"
            subscribeform =  SubscribeForm()

    context={
        "posts":posts,
        'top_posts':top_posts,
        'new_posts':new_posts,
        'subscribe_form':subscribe_form,
        'subscribe_success':subscribe_success,
        'featured_post':featured_post,
        'website_info':website_info,
        
    }
    return render(request,'blogapp/index.html',context)