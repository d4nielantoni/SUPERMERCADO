from django import forms
from .models import ShoppingList, Item

class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Lista'})
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'unit', 'price', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Item'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(ex: kg, gramas)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }
