from django import forms
from manage.models import Product, Inbound, Outbound

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'description', 'price', 'size']

class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product', 'quantity', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 상품 선택 필드를 위한 선택 옵션을 추가합니다.
        self.fields['product'].queryset = Product.objects.all()

class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(stock_quantity__gt=0)

    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')
        if quantity > product.stock_quantity:
            raise forms.ValidationError(f'출고 수량이 재고 수량을 초과합니다. (재고: {product.stock_quantity}개)')
        return quantity
