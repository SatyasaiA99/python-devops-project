from flask import Flask, render_template, redirect

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 50000, "img": "https://picsum.photos/200?1"},
    {"id": 2, "name": "Phone", "price": 20000, "img": "https://picsum.photos/200?2"},
    {"id": 3, "name": "Headphones", "price": 2000, "img": "https://picsum.photos/200?3"},
    {"id": 4, "name": "Smart Watch", "price": 5000, "img": "https://picsum.photos/200?4"},
    {"id": 5, "name": "Camera", "price": 30000, "img": "https://picsum.photos/200?5"},
    {"id": 6, "name": "Shoes", "price": 3000, "img": "https://picsum.photos/200?6"},
    {"id": 7, "name": "Backpack", "price": 1500, "img": "https://picsum.photos/200?7"},
    {"id": 8, "name": "Keyboard", "price": 2500, "img": "https://picsum.photos/200?8"},
    {"id": 9, "name": "Mouse", "price": 800, "img": "https://picsum.photos/200?9"},
    {"id": 10, "name": "Speaker", "price": 4000, "img": "https://picsum.photos/200?10"}
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
