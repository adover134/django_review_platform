from django import forms
from customForms import customFields


#리뷰 작성 시 사용될 폼입니다.
class ReviewWriteForm(forms.Form):
    title = forms.CharField(widget=customFields.NonStickyTextInputField())
    address = forms.CharField(widget=customFields.NonStickyTextInputField())
    images = forms.ImageField(label='room_images', widget=customFields.NonStickyImageField(attrs={'multiple': True, 'autocomplete': 'off'}), required=False)


class TextReviewWriteForm(ReviewWriteForm):

    review_sentence = forms.CharField(widget=customFields.NonStickyTextarea(attrs={'rows': 5, 'cols': 20, 'style': 'resize:none;', 'autocomplete': 'off'}))

    field_order = ['title', 'address', 'review_sentence', 'images']


class UserInfoForm(forms.Form):
    성 = forms.CharField()
    이름 = forms.CharField()
    이메일 = forms.EmailField()


class RoomWriteForm(forms.Form):
    우편번호 = forms.IntegerField()
    주소 = forms.CharField()
    건물명 = forms.CharField()
    건축년도 = forms.IntegerField()
