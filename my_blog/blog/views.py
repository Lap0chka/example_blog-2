from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404

from django.contrib import messages

from .models import Post, Comments
from .forms import CommentForm, ContactForm
from .tasks import send_email_celery


def index(request):
    """Rendering first page"""
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    return render(request, 'base.html', {'posts': posts})


def singel_post(request, slug):
    """Rendering post page and comments"""
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    comments = Comments.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            user = request.user
            new_comment = Comments.objects.create(body=body, post=post, author=user)
            new_comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog/post.html', {
        'post': post,
        'coments': comments,
        'form': form,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data["message"]
            send_email_celery.delay(name, email, subject, message)
            messages.success(request, 'Your message has been sent.')
            return HttpResponseRedirect(reverse('blog:contact'))
        else:
            messages.error(request, 'Something went wrong. Please try again.')
    else:
        form = ContactForm()
        return render(request, 'blog/contact.html', {'form': form})


def about(request):
    return render(request, 'blog/about.html')
