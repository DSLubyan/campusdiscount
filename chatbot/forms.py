from django import forms
from django.forms import DateInput

from .models import User_Model, Store_Model



class UserForm(forms.ModelForm):

    class Meta:
        model = User_Model
        fields = ('department','user_id')
class StoreModelForm(forms.ModelForm):
    class Meta:
        model = Store_Model
        fields = ('store_name','first_menu_name','first_menu_image','contents','naver_map_URL')