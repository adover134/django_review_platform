from django import forms


#리뷰 작성 시 사용될 폼입니다.
class ReviewWriteForm(forms.Form):
    images = forms.ImageField(label='room_images', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


class TextReviewWriteForm(ReviewWriteForm):
    address = forms.CharField()

    field_order = ['address', 'images']
