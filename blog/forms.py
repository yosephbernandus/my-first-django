from django import forms
from .models import Post, Comment, Tag

# CHOICES=[('item1','item 1'),
#          ('item2','item 2')]
class PostForm(forms.ModelForm):
    # tag = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)
    use_required_attribute = False
    class Meta:
        model = Post
        fields = ('title', 'text', 'tag') 
    
    def __init__ (self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["tag"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["tag"].queryset = Tag.objects.all()
        self.fields["tag"].required = False

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 2:
            raise forms.ValidationError("titile too short, minimum 5 characters required")
        return title
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 10:
            raise forms.ValidationError("Post should contain minimum 10 characters")
        return text
    
    # def clean(self):
    #     super(PostForm, self).clean()

    #     title = self.cleaned_data.get('title')
    #     text = self.cleaned_data.get('text')

    #     if len(title) < 2:
    #         self._errors['title'] = self.error_class(['Title minimum 5 characters required'])
    #     if len(text) < 5:
    #         self._errors['text'] = self.error_class(['Post should contain minimum 10 characters'])
        
    #     return self.cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('title', )