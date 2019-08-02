from django.shortcuts import render, redirect
from .forms import ProductForm, SalesForm, UpdateSalesForm
from django.http import HttpResponse
from django.contrib import messages
from faker import Faker
from .models import Company, Product, Sales
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime

import random


# Create your views here.

def dasboard(request):
    context = {}
    context["form"] = ProductForm()
    context["company_list"] = Company.objects.all()
    page = Paginator(Product.objects.filter(user=request.user), 10)
    context["product_list"] = page.get_page(request.GET.get('page', 1))
    context["page_count"] = page.num_pages
    if "q" in request.GET:
        query = request.GET.get('q')
        product_list = Product.objects.filter(
            Q(user=request.user) &
            (Q(name__icontains=query) |
             Q(company__name__icontains=query))
        )
        page = Paginator(product_list, 10)
        context["product_list"] = page.get_page(request.GET.get("page", 1))

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, f"{product.name} ugurla elave edildi"
            )
            return redirect("dashboard")
        else:
            context["form"] = form
    if request.is_ajax():
        return render(request, "include/product.html", context)
    else:
        return render(request, "dashboard.html", context)


def sales_view(request):
    context = {}
    context["sales_list"] = Sales.objects.filter(salesman=request.user).order_by("-id")
    context["form"] = SalesForm()
    if request.method == "POST":
        form = SalesForm(request.POST)
        if form.is_valid():
            sales = form.save(commit=False)
            sales.salesman = request.user
            sales.total_price = sales.product.price * sales.quantity
            sales.save()
        else:
            context["form"] = form
    return render(request, "sales.html", context)


def sales_update_view(request, id):
    context = {}
    sales = Sales.objects.filter(id=id).last()
    if sales:
        context["sales"] = sales
        context["form"] = UpdateSalesForm(instance=sales)
        if request.method == "POST":
            form = UpdateSalesForm(request.POST, instance=sales)
            if form.is_valid():
                form.save()
            else:
                context["form"] = form
                return redirect("sales_view")
        return render(request, "include/sales_form.html", context)
    else:
        return redirect("dashboard")


def update_view(request, id):
    context = {}
    product = Product.objects.filter(id=id).last()
    if product:
        if request.method == "POST":
            form = ProductForm(request.POST, instance=product, prefix="update")
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Ugurla update oldu"
                )
                return redirect("dashboard")
            else:
                messages.error(
                    request, f"Formda problem var {form.errors}"
                )
                return redirect("dashboard")
        context["product"] = Product.objects.filter(id=id).last()
        context["form"] = ProductForm(
            instance=product,
            prefix="update"
        )
        return render(request, "include/product_form.html", context)
    else:
        return redirect("dashboard")


def delete_view(request, id):
    context = {}
    product = Product.objects.filter(id=id).last()
    if product:
        if request.method == "POST":
            product.delete()
            messages.success(
                request, "Product ugurla silindi !"
            )
            return redirect("dashboard")
        context["product"] = product
        return render(request, "include/product_confirm.html", context)
    else:
        return redirect("dashboard")


def add_data(request):
    fake = Faker()
    for x in range(100):
        Product.objects.create(
            name=fake.job(),
            quantity=random.randint(1, 100),
            company=Company.objects.all().order_by("?").last(),
            expire_date=timezone.now(),
            price=random.randint(500, 5000)
        )
    return HttpResponse("Success")
