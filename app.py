from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Sample products
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 2000}
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
def view_cart():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
