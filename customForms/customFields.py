from django import forms
from django.core.validators import RegexValidator


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
