from app import app


from flask import render_template, request, url_for, redirect
# from .models import User, Product
from .myfunctions import Amiibo, Amiibo_all

from flask import render_template, request, url_for, redirect,flash
from .models import User, Product
from .myfunctions import Amiibo

from flask_login import current_user, login_required, login_user, logout_user

@app.route('/')
# @login_required
def home():
    return render_template('home.html')

@app.route('/products', methods=["GET", "POST"])
# @login_required
def products():
    if request.method == "POST":
        for p in Product.query.all():
            if p.product_id in request.form:
                product_id = p.product_id
                return redirect(url_for('product', product_id=product_id))
                    # add this to href link on html to route to product {{ url_for(product, product_id=p.id) }}
    amiibos = Amiibo_all()
    p = amiibos.request_data()
    return render_template('products.html', p=p)

@app.route('/cart')
# @login_required
def cart():
    return render_template('cart.html')

@app.route('/checkout')
# @login_required
def checkout():
    # if cart empty show there are no items in your cart to checkout
    return render_template('checkout.html')

@app.route('/add-product/<int:product_id>')
# @login_required
def add_product(product_id):
    ### increment count of chosen product in cart
    product = Product.query.get(product_id)
    product.add_it(current_user)
    return redirect(url_for('product.html'))

@app.route('/add-product-database')
# @login_required
def qwertyadd_product():
    for i in range(2,100):
    ### increment count of chosen product in cart
        product = Amiibo(i)
        amiibo = product.details()
        name = amiibo['name']
        img = amiibo['img_url']
        qwerty = Product(name, img)
        qwerty.save_it()
        print('works')
    return 'yes, yes, yes'


@app.route('/remove-product/<int:product_id>')
# @login_required
def remove_product(product_id):
    ### decrement count of chosen product in cart if it is in the cart
    product = Product.query.get(product_id)
    if product in current_user.added:
        product.remove_it(current_user)
    else:
        flash("You currently don't have this product in your cart")
    return redirect(url_for('product.html'))

@app.route('/clear-products/')
# @login_required
def clear_products():
    ### clear all items in the cart

    # if current_user.added:
    #     for product in current_user.added:
    #         product.remove_it(current_user)
    return redirect(url_for('products.html'))

    if current_user.added:
        for product in current_user.added:
            product.remove_it(current_user)
    return redirect(url_for('product.html'))


@app.route('/product/<int:product_no>')
# @login_required
def product(product_no):
    amiibo = Amiibo(product_no)
    # amiibo has methods .name .img_url .video_game .release etc. to use with jinja on html
    return render_template('ind-product.html', p=amiibo)