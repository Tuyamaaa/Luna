from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import Http404

products = [
    {
        "id": 1, "name": "Linen Blazer", "price": 189000,
        "category": "Clothing", "image": "blazer.png",
        "sizes": ["S", "M", "L"]
    },
    {
        "id": 2, "name": "Soft Blouse", "price": 129000,
        "category": "Clothing", "image": "blouse.png",
        "sizes": ["XS", "S", "M", "L"]
    },
    {
        "id": 3, "name": "Wide Pants", "price": 149000,
        "category": "Clothing", "image": "pants.png",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "id": 4, "name": "Classic Bag", "price": 159000,
        "category": "Bags", "image": "bag.png",
        "sizes": []
    },
    {
        "id": 5, "name": "Knit Cardigan", "price": 139000,
        "category": "Clothing", "image": "cardigan.png",
        "sizes": ["S", "M", "L"]
    },
    {
        "id": 6, "name": "Shoulder Bag", "price": 179000,
        "category": "Bags", "image": "shoulder-bag.png",
        "sizes": []
    },
    {
        "id": 7, "name": "Classic Heels", "price": 169000,
        "category": "Shoes", "image": "heels.png",
        "sizes": ["36", "37", "38", "39"]
    },
    {
        "id": 8, "name": "Midi Dress", "price": 189000,
        "category": "Clothing", "image": "dress.png",
        "sizes": ["XS", "S", "M", "L"]
    },
    {
        "id": 9, "name": "Satin Blouse", "price": 119000,
        "category": "Clothing", "image": "satin.png",
        "sizes": ["XS", "S", "M"]
    },
    {
        "id": 10, "name": "Trench Coat", "price": 259000,
        "category": "Clothing", "image": "coat.png",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "id": 11, "name": "Mini Crossbody", "price": 109000,
        "category": "Bags", "image": "crossbody.png",
        "sizes": []
    },
    {
        "id": 12, "name": "Leather Loafers", "price": 159000,
        "category": "Shoes", "image": "loafers.png",
        "sizes": ["36", "37", "38", "39", "40"]
    },
]


def home(request):
    return render(request, 'shop/home.html')


def shop_page(request):
    return render(request, 'shop/shop.html', {
        'products': products
    })


def page(request, page_name):
    allowed_pages = {'collection', 'cart', 'about', 'contact'}

    if page_name not in allowed_pages:
        raise Http404

    # Эдгээр хуудсын template-ийг дараа нь хөгжүүлнэ.
    return render(request, 'shop/home.html')

# PRODUCT DETAIL

def product_detail(request, product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        raise Http404("Product not found")

    return render(request, "shop/product_detail.html", {
        "product": product,
        "colors": ["Beige", "Black", "White"]
    })


# ADD TO CART

@require_POST
def add_to_cart(request, product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        raise Http404("Product not found")

    size = request.POST.get("size", "")
    color = request.POST.get("color", "Beige")

    available_sizes = product["sizes"] or ["One Size"]

    if size not in available_sizes:
        return redirect("product_detail", product_id=product_id)

    if color not in ["Beige", "Black", "White"]:
        return redirect("product_detail", product_id=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    quantity = max(1, min(quantity, 10))

    cart = request.session.get("cart", {})

    # Ижил бараа, хэмжээ, өнгийг нэг мөрөнд нэгтгэнэ.
    cart_key = f"{product_id}:{size}:{color}"

    if cart_key in cart:
        old_quantity = cart[cart_key]["quantity"]
        cart[cart_key]["quantity"] = min(
            old_quantity + quantity, 10
        )
    else:
        cart[cart_key] = {
            "product_id": product_id,
            "size": size,
            "color": color,
            "quantity": quantity
        }

    request.session["cart"] = cart

    return redirect("cart")


# SHOPPING CART

def cart_page(request):
    cart = request.session.get("cart", {})

    cart_items = []
    total = 0

    for key, item in cart.items():
        product = next(
            (p for p in products
             if p["id"] == item["product_id"]),
            None
        )

        if product is None:
            continue

        quantity = item["quantity"]
        subtotal = product["price"] * quantity
        total += subtotal

        cart_items.append({
            "key": key,
            "product": product,
            "size": item["size"],
            "color": item["color"],
            "quantity": quantity,
            "subtotal": subtotal
        })

    return render(request, "shop/cart.html", {
        "cart_items": cart_items,
        "total": total
    })
    
@require_POST
def update_cart(request):
    key = request.POST.get("key")
    action = request.POST.get("action")

    cart = request.session.get("cart", {})

    if key in cart:
        quantity = cart[key]["quantity"]

        if action == "increase":
            cart[key]["quantity"] = min(quantity + 1, 10)

        elif action == "decrease":
            if quantity > 1:
                cart[key]["quantity"] = quantity - 1
            else:
                del cart[key]

        request.session["cart"] = cart

    return redirect("cart")


@require_POST
def remove_from_cart(request):
    key = request.POST.get("key")
    cart = request.session.get("cart", {})

    if key in cart:
        del cart[key]
        request.session["cart"] = cart

    return redirect("cart")


collections = [
    {
        "name": "SUMMER",
        "slug": "summer",
        "image": "summer.jpg",
        "description": "Light and effortless summer styles"
    },
    {
        "name": "AUTUMN",
        "slug": "autumn",
        "image": "autumn.jpg",
        "description": "Warm tones and timeless layers"
    },
    {
        "name": "WINTER",
        "slug": "winter",
        "image": "winter.jpg",
        "description": "Cozy essentials for cold days"
    },
    {
        "name": "ESSENTIALS",
        "slug": "essentials",
        "image": "essentials.jpg",
        "description": "Everyday pieces you'll love"
    },
]

# Цуглуулга бүрт хамаарах барааны ID
collection_products = {
    "summer": [2, 3, 8, 9],
    "autumn": [1, 3, 5, 10],
    "winter": [1, 5, 10, 12],
    "essentials": [1, 2, 4, 6, 11],
}


def collection_page(request):
    return render(request, "shop/collection.html", {
        "collections": collections
    })


def collection_detail(request, slug):
    collection = next(
        (c for c in collections if c["slug"] == slug),
        None
    )

    if collection is None:
        raise Http404("Collection not found")

    product_ids = collection_products[slug]

    selected_products = [
        p for p in products if p["id"] in product_ids
    ]

    return render(request, "shop/collection_detail.html", {
        "collection": collection,
        "products": selected_products
    })
def about_page(request):
    return render(request, "shop/about.html")


from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import redirect


def contact_page(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your message has been sent successfully!"
            )

            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "shop/contact.html", {
        "form": form
    })
    
from .forms import CheckoutForm
from .models import Order


def checkout_page(request):
    session_cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for key, item in session_cart.items():
        product = next(
            (p for p in products if p["id"] == item["product_id"]),
            None
        )

        if product is None:
            continue

        quantity = item["quantity"]
        subtotal = product["price"] * quantity
        total += subtotal

        cart_items.append({
            "name": product["name"],
            "price": product["price"],
            "size": item["size"],
            "color": item["color"],
            "quantity": quantity,
            "subtotal": subtotal
        })

    if not cart_items:
        return redirect("cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total
            order.items = cart_items
            order.save()

            request.session["last_order_id"] = order.id
            request.session["cart"] = {}

            return redirect("order_success", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, "shop/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total": total
    })


def order_success(request, order_id):
    if request.session.get("last_order_id") != order_id:
        raise Http404("Order not found")

    order = get_object_or_404(Order, id=order_id)

    return render(request, "shop/order_success.html", {
        "order": order
    })

@require_POST
def add_to_cart(request, product_id):
    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        raise Http404("Product not found")

    size = request.POST.get("size", "")
    color = request.POST.get("color", "Beige")

    available_sizes = product["sizes"] or ["One Size"]

    if size not in available_sizes:
        return redirect("product_detail", product_id=product_id)

    if color not in ["Beige", "Black", "White"]:
        return redirect("product_detail", product_id=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, min(quantity, 10))

    cart = request.session.get("cart", {})
    cart_key = f"{product_id}:{size}:{color}"

    if cart_key in cart:
        cart[cart_key]["quantity"] = min(
            cart[cart_key]["quantity"] + quantity, 10
        )
    else:
        cart[cart_key] = {
            "product_id": product_id,
            "size": size,
            "color": color,
            "quantity": quantity
        }

    request.session["cart"] = cart

    return redirect("cart")


