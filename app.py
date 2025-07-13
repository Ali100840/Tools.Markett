from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import csv

app = Flask(_name_)

products = {
    0: ["saw", 10],
    1: ["drill", 30],
    2: ["hammer", 15]
}

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/generate-bill", methods=["POST"])
def generate_bill():
    try:
        data = request.get_json()
        if not data:
            return "Invalid data", 400

        quantities = data["quantities"]
        name = data.get("name", "")
        phone = data.get("phone", "")
        location = data.get("location", "")

        bill = []
        total_all = 0

        for i, qty in enumerate(quantities):
            qty = int(qty)
            if qty > 0:
                product_name, price = products[i]
                total = qty * price
                bill.append({
                    "name": product_name,
                    "price": price,
                    "qty": qty,
                    "total": total
                })
                total_all += total

        csv_file = "/tmp/bills.csv"

        # إذا الملف مش موجود، أضف الرأس
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Phone", "Location", "Total", "Qty", "Price", "Product", "Date"])
            for item in bill:
                writer.writerow([
                    name,
                    phone,
                    location,
                    item["total"],
                    item["qty"],
                    item["price"],
                    item["name"],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])

        return jsonify({
            "bill": bill,
            "total": total_all,
            "date": datetime.now().strftime("%d-%m-%Y"),
            "name": name,
            "phone": phone,
            "location": location
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    app.run(debug=True)
