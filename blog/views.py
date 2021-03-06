from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

#lte : less than equal <=
#lt : less than <
#gte : greater than equal >=
#gt : greater than >

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
#    try:
#        post = Post.objects.get(pk=pk)
#    except Post.DoesNotExit:
#        raise http404 #djnago.http.HTTP404
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required(login_url='admin:login')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #return redirect('blog.views.post_detail', pk=post.pk)
            return redirect('post_detail', pk=post.pk) #DjangoGirls english 버전
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required(login_url='admin:login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
