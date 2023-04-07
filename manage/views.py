from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Inbound, Outbound
from manage.form import InboundForm, OutboundForm, ProductForm


# Create your views here.
@login_required
def product_list(request):
# 등록 된 상품의 리스트를 볼 수 있는 view
    products = Product.objects.all()
    return render(request, 'manage/product_list.html', {'products': products})


@login_required
def product_create(request):
    # 상품 등록 view
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '상품이 등록되었습니다.')
            return redirect('manage/product_list.html')
    else:
        form = ProductForm()
    return render(request, 'manage/product_create.html', {'form': form})


@login_required
@transaction.atomic
def inbound_create(request):
    if request.method == 'POST':
        form = InboundForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']

            # 입고 기록 생성
            inbound = Inbound.objects.create(product=product, quantity=quantity, price=price)

            # 입고 수량 조정
            product.stock_quantity += quantity
            product.save()

            messages.success(request, f"{product.name} {quantity}개 입고 완료!")
            return render('manage/inbound_create.html')
    else:
        form = InboundForm()
    context = {'form': form}
    return render(request, 'manage/inbound_create.html', context)



@login_required
def outbound_create(request, product_id):
    # 상품 출고 view
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = OutboundForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity > product.stock_quantity:
                messages.error(request, '재고 수량이 충분하지 않습니다.')
            else:
                # 출고 기록 생성
                outbound = Outbound.objects.create(product=product, quantity=quantity)

                # 재고 수량 조정
                product.stock_quantity -= quantity
                product.save()

                messages.success(request, f"{product.name} {quantity}개 출고 완료!")
                return redirect('manage/inventory.html')
    else:
        form = OutboundForm()
    context = {'form': form, 'product': product}
    return render(request, 'manage/outbound_create.html', context)


def inventory(request):
    # 총 입고 수량, 가격 계산
    total_inbound_quantity = Inbound.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_inbound_price = Inbound.objects.aggregate(Sum('quantity', 'price'))['quantity__sum'] or 0

    # 총 출고 수량, 가격 계산
    total_outbound_quantity = Outbound.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_outbound_price = Outbound.objects.aggregate(Sum('quantity', 'product__price'))['quantity__sum'] or 0

    # 재고 수량, 가격 계산
    total_stock_quantity = total_inbound_quantity - total_outbound_quantity
    total_stock_price = total_inbound_price - total_outbound_price

    context = {
        'total_inbound_quantity': total_inbound_quantity,
        'total_inbound_price': total_inbound_price,
        'total_outbound_quantity': total_outbound_quantity,
        'total_outbound_price': total_outbound_price,
        'total_stock_quantity': total_stock_quantity,
        'total_stock_price': total_stock_price,
    }
    return render(request, 'manage/inventory.html', context)

