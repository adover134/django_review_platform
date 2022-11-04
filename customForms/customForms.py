from django import forms
from customForms import customFields
from DBs.models import Review


#리뷰 작성 시 사용될 폼입니다.
class ReviewWriteForm(forms.Form):
    title = forms.CharField(widget=customFields.NonStickyTextInputField())
    address = forms.CharField(widget=customFields.NonStickyTextInputField())
    postcode = forms.CharField(widget=customFields.NonStickyTextInputField())
    checking = forms.IntegerField()
    deposit = forms.IntegerField()
    monthly = forms.IntegerField(required=None)
    area = forms.FloatField()
    room_area = forms.CharField(widget=customFields.NonStickyTextInputField())
    proof = forms.IntegerField()
    sunshine = forms.IntegerField()
    clean = forms.IntegerField()
    humidity = forms.IntegerField()
    images = forms.ImageField(label='room_images', widget=customFields.NonStickyImageField(attrs={'multiple': True, 'autocomplete': 'off'}), required=False)


class TextReviewWriteForm(ReviewWriteForm):

    review_sentence = forms.CharField(widget=customFields.NonStickyTextarea(attrs={'rows': 5, 'cols': 20, 'style': 'resize:none;', 'autocomplete': 'off'}))

    field_order = ['title', 'address', 'review_sentence', 'images']


class RoomWriteForm(forms.Form):
    room_address = forms.CharField(widget=customFields.NonStickyTextInputField())
    postcode = forms.IntegerField(widget=customFields.NonStickyTextInputField())
    name = forms.CharField(required=False, widget=customFields.NonStickyTextInputField())
    builtYear = forms.IntegerField(required=False, widget=customFields.NonStickyTextInputField())
    buildingFloorNum = forms.IntegerField(required=False, widget=customFields.NonStickyTextInputField())
    commonInfo = forms.JSONField(required=False)
    ownerPhone = forms.CharField(required=False, widget=customFields.NonStickyTextInputField())


class UserInfoForm(forms.Form):
    last_name = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()


class ReviewWriteForm2(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["reviewTitle", "reviewSentence", "rent", "monthlyRent", "deposit", "roomSize"]

    def clean(self):

        # data from the form is fetched using super function
        super(ReviewWriteForm2, self).clean()

        # extract the username and text field from the data
        rent = self.cleaned_data.get('rent')
        monthlyRent = self.cleaned_data.get('monthlyRent')

        if rent == 1 and monthlyRent is None:
            self._errors['monthlyRent'] = self.error_class(['월세일 시 월세 금액을 반드시 입력하셔야 합니다.'])


        # return any errors if found
        return self.cleaned_data
