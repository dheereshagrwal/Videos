from django import forms
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review_title', 'rating',
                  'review_description']
class ReviewFullForm(ReviewForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(ReviewForm.Meta):
        fields = ReviewForm.Meta.fields + ['images', ]
