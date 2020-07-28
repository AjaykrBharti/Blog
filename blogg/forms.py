from django import forms

from .models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','slug' ,'post_image','text','status','tags')

# This form will help user to share the post
class EmailPostForm(forms.Form):
     name = forms.CharField(max_length=25)
     email = forms.EmailField()
     to = forms.EmailField()
     comments = forms.CharField(required=False,
     widget=forms.Textarea)


# Model based forms
class CommentForm(forms.ModelForm):

     class Meta:
         model = Comment
         fields = ('name', 'email', 'body')

