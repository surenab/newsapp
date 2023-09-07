from django import forms
from .models import News, Message, NewsComment, UserProfile
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model


class NewsForm(forms.ModelForm):
    NEWS_TYPES = (
        ("1", "Political"),
        ("2", "Business"),
        ("3", "International"),
        ("4","National"),
        ("5","Lifestyle"),
        ("6", "Sport"),
        ("7", "Cultural"),
        ("8", "Crime")
    )

    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'News Description'}))
    news_type = forms.ChoiceField(label="", choices=NEWS_TYPES, widget=forms.Select())
    image = forms.ImageField(label="")
    
    class Meta:
        model = News

        fields = ["title", "description", "news_type", 'image']


class MessageForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(max_length=1000, required=True)

    class Meta:
        model = Message
        exclude = ()


class NewsCommentForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = NewsComment
        fields = ["text"]


# class ProfileForm(forms.ModelForm):

#     class Meta:
#         model = Profile
#         fields = ['image', 'tel', 'address', 'birthday']


class SetPasswordForm(SetPasswordForm):

    class Meta:
        model = get_user_model
        fields = ['new_password1', 'new_password2']


# class PasswordResetForm(PasswordResetForm):

#     def __init__(self, *args, **kwargs):
#         super(PasswordResetForm, self).__init__(*args, **kwargs)


class UserProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=20, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    image = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'clearablefileinput'}), label='')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name',  'image', 'profession', 'address', 'tel', 'birthday']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']

        user_profile = super(UserProfileForm, self).save(commit=commit)

        if commit:
            self.instance.user.save()

        return user_profile
