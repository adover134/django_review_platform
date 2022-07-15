from django import forms


class NonStickyImageField(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        value = None  # Clear the submitted value.
        return super().get_context(name, value, attrs)


class NonStickyTextInputField(forms.TextInput):
    def get_context(self, name, value, attrs):
        value = None  # Clear the submitted value.
        return super().get_context(name, value, attrs)


class NonStickyTextarea(forms.Textarea):
    def get_context(self, name, value, attrs):
        value = None  # Clear the submitted value.
        return super().get_context(name, value, attrs)


#리뷰 작성 시 사용될 폼입니다.
class ReviewWriteForm(forms.Form):
    title = forms.CharField(widget=NonStickyTextInputField())
    address = forms.CharField(widget=NonStickyTextInputField())
    images = forms.ImageField(label='room_images', widget=NonStickyImageField(attrs={'multiple': True, 'autocomplete': 'off'}), required=False)


class TextReviewWriteForm(ReviewWriteForm):
    review_sentence = forms.CharField(widget=NonStickyTextarea(attrs={'rows': 5, 'cols': 20, 'style': 'resize:none;', 'autocomplete': 'off'}))
    review_type = forms.CharField(label=False, initial='text', widget=forms.TextInput(attrs={'style': 'display:none;', 'autocomplete': 'off'}))

    field_order = ['title', 'address', 'review_sentence', 'images']


class ImageReviewWriteForm(ReviewWriteForm):
    icon_info = forms.CharField(widget=NonStickyTextarea(attrs={'rows': 5, 'cols': 20, 'style': 'resize:none;'}))
    review_type = forms.CharField(label=False, initial='image', widget=forms.TextInput(attrs={'style': 'display:none;', 'autocomplete': 'off'}))

    field_order = ['title', 'address', 'icon_info', 'images']


class UserInfoForm(forms.Form):
    user_nickname = forms.CharField()
    user_email = forms.EmailField()
    user_warn_count = forms.IntegerField(required=False, disabled=True)
