from django.forms import ModelForm, TextInput
from .models import Order, TabluarOrders

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['number', 'date', 'client' , 'type_play', 'amount', 'comment', 'returned_container', 'id']

        widgets = {
            'comment' : TextInput(attrs={
               'class' : 'form-control',
            'placeholder': 'Комментарий',
        }),
        }