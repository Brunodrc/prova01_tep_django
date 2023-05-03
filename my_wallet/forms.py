from django import forms
from .models import Transaction

class RegisterTransaction(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ["date_done", "stock", "quantity_stock", "unite_price", "type_of", "brokerage"]
