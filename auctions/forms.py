from django import forms
from .models import Product, Category, Bid, Comment


# How to get category show up on select
# Hard coding
cats = [('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Home', 'Home')]
# get category from Model



class ProductForm(forms.Form):
    product = forms.CharField(label="Product Name:", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Product Name'}))
    description = forms.CharField(label="Description:", max_length=300, widget=forms.Textarea(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label="Price:", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.CharField(label="Image URL", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Image URL (optional)'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category:",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(label="Is Active:", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input m-2'}))



class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class BidsForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid_amount',)

        widgets = {
            'bid_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'AUD $'}),
        }

class commentForm(forms.ModelForm):
     class Meta:
          model = Comment
          fields = ('comment',)

          widgets = {
               'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post com'})
               
          }


class checkForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('is_active',)  # Include only the fields you want to display

        widgets = {
            'is_active': forms.BooleanField(
                label="Is Active:",
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input m-2'})
            )
        }
        