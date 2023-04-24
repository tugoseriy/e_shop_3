from django.shortcuts import render, redirect
from . import models
from telebot import TeleBot
bot = TeleBot('6195505853:AAHtqc6dXovW0zmHjcVwZ06Oy9rrQecSa-w', parse_mode='HTML')

def home(request):
    all_products = models.Product.objects.all()
    all_categories = models.Category.objects.all()
    context = {'products': all_products, 'categories': all_categories}
    return render(request, 'index.html', context)


def about_product(request, pk):
    # poluchit po jope
    current_product = models.Product.objects.get(product_name=pk)
    context = {'product': current_product}
    return render(request, 'about.html', context)


# Create your views here
def category_products(request, pk):
    products_from_category = models.Category.objects.get(category_name=pk)
    products_from_category = models.Product.objects.filter(product_category=products_from_category)
    context = {'products': products_from_category}
    return render(request, 'index.html', context)


def search_for_product(request):
    product_from_front = request.GET.get('search')
    find_product_from_db = models.Product.objects.filter(product_name__contains=product_from_front)
    context = {'products': find_product_from_db}
    return render(request, 'index.html', context)


def add_product_to_cart(request, pk):
    current_product = models.Product.objects.get(id=pk)
    checker = models.UserCart.objects.filter(user_id=request.user.id, user_product=current_product)
    if checker:
        checker[0].quantity = int(request.POST.get('pr_count'))
        checker[0].total_for_product = current_product.product_price * checker[0].quantity


    else:
        models.UserCart.objects.create(user_id=request.user.id, user_product=current_product,
                                       quantity=request.POST.get('pr_count'),
                                       total_for_product=int(
                                           request.POST.get('pr_count')) * current_product.product_price)
    return redirect(f'/product-detail/{current_product.product_name}')
def get_user_cart(request):
    user_cart =models.UserCart.objects.filter(user_id=request.user.id)
    context = {'user_cart': user_cart}
    return render(request, 'cart.html', context)
def delete_pr_from_cart(request, pk):
    prod_to_delete = models.UserCart.objects.get(id=pk)
    prod_to_delete.delete()
    return redirect('/cart')
def order_zakaz(request):
    user_cart = models.UserCart.objects.filter(user_id= request.user.id)
    username = request.POST.get('username')
    phone_number = request.POST.get('phone_number')
    adress = request.POST.get('address')
    result = sum([i.total_for_product for i in user_cart])
    invoice_message = f'<b>новый заказ</b>\n\n<b>имя:</b> {username}\n<b>номер:</b> {phone_number}\n<b>address dostavki</b> {adress}\n--------\n'
    for i in user_cart:
        invoice_message+= f'<b>{i.user_product}</b> X <b>{i.quantity}</b>= <b>{i.total_for_product}</b>\n'
    invoice_message +=f'\n--------------\n <b>итог:</b> {result} sum'
    bot.send_message(1695366, invoice_message)
    return redirect('/')

