from django import forms
from .models import ConstractorInfo, RequestInfo

# 施工業者ログイン用フォーム
class LoginForm(forms.Form):
    username = forms.CharField(label="ユーザー名")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# 施工業者情報編集用フォーム
class ConstractorForm(forms.ModelForm):
    class Meta:
        model = ConstractorInfo
        fields = (
            'password', 'constractor', 'representative', 'address', 'tel'
        )
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# 工事申請書用フォーム
class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestInfo
        fields = (
            'client', 'address', 'tel', 'constract', 'place', 'start', 'end'
        )
        widgets = {
            'constract': forms.Select(choices=(('0', '新設'), ('1', '改造'), ('2', '増設'))),
            'start': forms.TextInput(attrs={'class': 'datepicker-ui'}),
            'end': forms.TextInput(attrs={'class': 'datepicker-ui'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = (field.widget.attrs['class'] if 'class' in field.widget.attrs else '') + ' form-control'
            field.widget.attrs['placeholder'] = field.label