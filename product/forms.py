from django import forms
from .models import Product, Sales


class ProductForm(forms.ModelForm):
    expire_date = forms.DateTimeField(input_formats=["%m/%d/%Y %H:%M %p"])

    class Meta:
        model = Product
        fields = [
            "name", "quantity", "company",
            "expire_date", "price"
        ]


class UpdateSalesForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(UpdateSalesForm, self).__init__(*args, **kwargs)
    #     self.fields["product"].widgets.attrs["readonly"] = True

    class Meta:
        model = Sales
        fields = [
            "quantity", "company"
        ]

        widgets = {
            "product": forms.Select(attrs={
                "disabled": True
            })
        }

    def clean(self):
        if self.instance.quantity > self.instance.product.quantity:
            raise forms.ValidationError("Kifayet qeder mehsul yoxdur")
        else:
            return super(UpdateSalesForm, self).clean()


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = [
            "product", "quantity", "company"
        ]

    def clean(self):
        product = self.cleaned_data.get("product")
        quantity = self.cleaned_data.get("quantity")
        if quantity > product.quantity:
            raise forms.ValidationError("Kifayet qeder mehsul yoxdur")
