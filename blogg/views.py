from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.utils import timezone
from .models import Post
from .forms import PostForm,EmailPostForm,CommentForm
from django.core.mail import send_mail #For sending the mail from Django
from taggit.models import Tag
from django.db.models import Count


def post_list(request,tag_slug=None):
    object_list = Post.objects.filter(published_date__lte=timezone.now(),
                                status = 'published').order_by('published_date')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 2)  # 2 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blogg/post_list.html', {'posts': posts,'page':page,'tag': tag})


def post_detail(request, pk,slug=None):
    post = get_object_or_404(Post, pk=pk)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    comment_form = CommentForm()
    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():


            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

            # comment_form = CommentForm()

    else:
        comment_form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'comment_form': comment_form,
               'similar_posts': similar_posts}
    return render(request, 'blogg/post_detail.html', context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blogg/post_edit.html', {'form': form})



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogg/post_edit.html', {'form': form})



def post_share(request, pk):
 # Retrieve post by id
     post = get_object_or_404(Post, id=pk, status='published')
     if request.method == 'POST':
     # Form was submitted
         form = EmailPostForm(request.POST)
         if form.is_valid():
         # Form fields passed validation
             cd = form.cleaned_data
             post_url = request.build_absolute_uri(
                 post.get_absolute_url())
             subject = '{} ({}) recommends you reading "{}"'\
                 .format(cd['name'], cd['email'], post.title)
             message = 'Read "{}" at {}\n\n{}\'s comments: {}'\
                 .format(post.title, post_url, cd['name'], cd['comments'])
             send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
             sent = True
         # ... send email
     else:
         form = EmailPostForm()
     return render(request, 'blogg/share.html', {'post': post,
     'form': form})


