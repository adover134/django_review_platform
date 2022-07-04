from django import forms


#리뷰 작성 시 사용될 폼입니다.
class ReviewWriteForm(forms.Form):
    title = forms.CharField()
    address = forms.CharField()
    images = forms.ImageField(label='room_images', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class TextReviewWriteForm(ReviewWriteForm):
    review_sentence = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20, 'style': 'resize:none;'}))
    review_type = forms.CharField(label=False, initial='text', widget=forms.TextInput(attrs={'style': 'display:none;'}))

    field_order = ['title', 'address', 'review_sentence', 'images']


class ImageReviewWriteForm(ReviewWriteForm):
    icon_info = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':20, 'style': 'resize:none;'}))
    review_type = forms.CharField(label=False, initial='image', widget=forms.TextInput(attrs={'style': 'display:none;'}))

    field_order = ['title', 'address', 'icon_info', 'images']
