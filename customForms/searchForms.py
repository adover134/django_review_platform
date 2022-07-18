from django import forms
from django.core.exceptions import ValidationError


class ReviewSearchForm(forms.Form):
    # 여러 체크 박스를 모아서 하나로 만드는 경우, 각 체크 박스는 튜플로 작성된다.
    # 각 튜플은 'value', 'label' 형태로 이뤄진다.
    # ('a', 'A')의 경우, 체크 시 'a'를 반환하며 'A'라는 이름으로 웹에 표시된다.
    commonInfoOptions = (
        ('ParkingLot', 'ParkingLot'),
        ('Elevator', 'Elevator'),
        ('CCTV', 'CCTV'),
    )
    built_from = forms.IntegerField(min_value=1960, max_value=2022, initial=1960)
    built_to = forms.IntegerField(min_value=1960, max_value=2022, initial=2022)

    공통_정보 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=commonInfoOptions, required=False)

    field_order = ['공통_정보', 'built_from', 'built_to']

    def clean(self):

        cd = super().clean()
        built_from = cd.get("built_from")
        built_to = cd.get("built_to")

        if built_from and built_to:
            # Only do something if both fields are valid so far.
            if built_from > built_to:
                raise ValidationError(message="올바르지 않은 연도 범위입니다.", code="built_year_error")

        return cd
