from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def home(request):
    blog_posts = BlogPost.objects.order_by('-date')
    return render(request, 'blog/home.html', {'blog_posts': blog_posts})


def blog_post(request, blog_id):
    blog = get_object_or_404(BlogPost, pk=blog_id)
    return render(request, 'blog/blog_post.html', {'blog': blog})
