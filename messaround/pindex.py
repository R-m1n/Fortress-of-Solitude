import os
import random
import string
import csv
import sys
import openpyxl
from pathlib import Path


class Product:
    def __init__(self, name: str, price: str,
                 discount: str, weight: str,
                 length: str, width: str,
                 height: str, categories: str) -> None:

        self.id = generate_id()
        self.type = "simple"
        self.sku = ""
        self.name = name
        self.published = 1
        self.is_featured = 0
        self.visibility = 1
        self.short_desc = ""
        self.desc = ""
        self.in_stock = 1
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.costumer_review = 1
        self.price = price
        self.sale_price = str(
            float(price) - (float(price) * (float(discount) / 100))
        )
        self.categories = categories

    def info(self) -> list[str]:
        return [
            self.id,
            self.type,
            self.sku,
            self.name,
            self.published,
            self.is_featured,
            self.visibility,
            self.short_desc,
            self.desc,
            self.in_stock,
            self.weight,
            self.length,
            self.width,
            self.height,
            self.costumer_review,
            self.sale_price,
            self.price,
            self.categories,
        ]


def generate_id(id_list: list[str]):
    id = random.choices(string.digits, k=8)

    id = "".join(id)
    if id not in id_list:
        id_list.append(id)

        return id

    generate_id(id_list)


if __name__ == "__main__":
    id_list = []

    csv_file_path = Path("product_record.csv")

    files = [Path(file.name) for file in os.scandir(os.getcwd())
             if Path(file.name).suffix == ".xlsx"]

    source_file = files.pop() if len(files) != 0 else sys.exit()

    xlsx_file = openpyxl.load_workbook(source_file)
    sheet = xlsx_file.active

    products = []
    for row in range(1, sheet.max_row + 1):
        product_info = []

        for column in range(1, sheet.max_column + 1):
            product_info.append(sheet.cell(row=row, column=column).value)

        product = Product(name=product_info[0],
                          price=product_info[1],
                          discount=product_info[2],
                          weight=product_info[3],
                          length=product_info[4],
                          width=product_info[5],
                          height=product_info[6],
                          categories=product_info[7],
                          )

        products.append(product.info())

    with open(csv_file_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)

        columns = [
            "ID",
            "Type",
            "SKU",
            "Name",
            "Published",
            "is featured?",
            "Visibility in catalog",
            "Short description",
            "Description",
            "In stock?",
            "Weight",
            "Length",
            "Width",
            "Height",
            "Allow customer reviews?",
            "Sale price",
            "Regular price",
            "Categories",
        ]

        writer.writerow(columns)

        writer.writerows(products)
