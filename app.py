from flask import Flask, render_template, request, jsonify
from datetime import datetime
from openpyxl import Workbook, load_workbook
import os

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

        excel_file = '/tmp/ALI(2).xlsx'  # تأكد من استخدام /tmp في Render

        if os.path.exists(excel_file):
            wb = load_workbook(excel_file)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.append(["Name", "Phone", "Location", "Total", "Qty", "Price", "Product", "Date"])

        for item in bill:
            ws.append([
                name,
                phone,
                location,
                item["total"],
                item["qty"],
                item["price"],
                item["name"],
                datetime.now().strftime("%Y-%m-%d")
            ])

        wb.save(excel_file)

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
