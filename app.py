from flask import Flask, render_template, redirect

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 50000, "img": "/static/images/laptop.jpg"},
    {"id": 2, "name": "Phone", "price": 20000, "img": "/static/images/phone.jpg"},
    {"id": 3, "name": "Headphones", "price": 2000, "img": "/static/images/headphones.jpg"},
    {"id": 4, "name": "Smart Watch", "price": 5000, "img": "/static/images/watch.jpg"},
    {"id": 5, "name": "Camera", "price": 30000, "img": "/static/images/camera.jpg"},
    {"id": 6, "name": "Shoes", "price": 3000, "img": "/static/images/shoes.jpg"},
    {"id": 7, "name": "Backpack", "price": 1500, "img": "/static/images/bag.jpg"},
    {"id": 8, "name": "Keyboard", "price": 2500, "img": "/static/images/keyboard.jpg"},
    {"id": 9, "name": "Mouse", "price": 800, "img": "/static/images/mouse.jpg"},
    {"id": 10, "name": "Speaker", "price": 4000, "img": "/static/images/speaker.jpg"}
]

cart = []

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/add/<int:id>")
def add_to_cart(id):
    for p in products:
        if p["id"] == id:
            cart.append(p)
    return redirect("/cart")

@app.route("/cart")
def cart_view():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

app.run(host="0.0.0.0", port=5000)
