from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Inventory,Product

class edit_user_form(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
class edit_inventory(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name','date_created']   
        
class product_adding(ModelForm):
    class Meta:
        model = Product
        fields = ['pname','weight', 'value', 'date_added'] 
        
class product_edit(ModelForm):
    class Meta:
        model = Product
        fields = ['pname','weight','value']                 