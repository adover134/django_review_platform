from django import forms
from customForms import customFields
from DBs.models import Review


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


class ReviewWriteForm2(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["reviewTitle", "reviewSentence", "fee_kind", "fee", "guarantee", "room_size"]

    def clean(self):

        # data from the form is fetched using super function
        super(ReviewWriteForm2, self).clean()

        # extract the username and text field from the data
        fee_kind = self.cleaned_data.get('fee_kind')
        fee = self.cleaned_data.get('fee')

        if fee_kind == 1 and fee is None:
            self._errors['fee'] = self.error_class(['월세일 시 월세 금액을 반드시 입력하셔야 합니다.'])


        # return any errors if found
        return self.cleaned_data
