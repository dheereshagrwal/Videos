from django import forms
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review_title', 'rating',
                  'review_description', 'review_image']
