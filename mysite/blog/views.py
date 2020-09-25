from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                DetailView,CreateView,UpdateView,
                                DeleteView,)


# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#
# def PostListfunc(request):
#     post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#     return render(request,'post_list.html',{'post_list': post })

# ListView returns a context object dictionary named model_list(post_list), but
# we can change this by typing context_object_name = 'posts' , etc etc.
# grab the Post model,all the objects here and filter out based on these condition
# grab the published_date lessThanOrEqualTo present timezone and order
# __lte means lessThanOrEqualTo
# them by descending(latest first)
# if no condition i.e(order_by('-published_date')) given then by default ascending(last is first)


class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    # if not logged in then go to log in page
    # only a logged in user can create a post.
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    # form to create a new Post
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    # reverse_lazy makes us wait until post is permanently deleted
    # nd then takes us back to post_list.

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')


################################################################################
################################################################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)



@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})



@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    # function in models
    return redirect('post_detail',pk=comment.post.pk)



@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    # here storing in another variable as after deletion data is lost
    comment.delete()
    return redirect('post_detail',pk=post_pk)
