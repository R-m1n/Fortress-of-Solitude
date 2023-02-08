import random
import string
import csv
import sys
import openpyxl
from pathlib import Path


class Product:
    def __init__(self, name: str, weight: float, length: float, width: float,
                 height: float, price: float, discount: float, categories: str) -> None:

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
        self.sale_price = price - (price * (discount / 100))
        self.categories = categories

    def info(self) -> list[str]:
        return [
            self.id, self.type, self.sku, self.name, self.published, self.is_featured,
            self.visibility, self.short_desc, self.desc, self.in_stock, self.weight,
            self.length, self.width, self.height, self.costumer_review, self.sale_price,
            self.price, self.categories,
        ]


def generate_id():
    return "".join(random.choices(string.digits, k=8))


if __name__ == "__main__":
    is_empty = True
    csv_file_path = Path("products.csv")

    try:
        source_file = Path(sys.argv[1])

    except IndexError:
        sys.exit()

    with openpyxl.load_workbook(source_file) as xlsx_file:
        sheet = xlsx_file["Sheet1"]

    with open(csv_file_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)

        if is_empty:
            columns = [
                "ID", "Type", "SKU", "Name", "Published",
                "is featured?", "Visibility in catalog",
                "Short description", "Description", "In stock?",
                "Stock", "Weight", "Length", "Width", "Height",
                "Allow customer reviews?", "Sale price", "Regular price",
                "Categories",
            ]

            writer.writerow(columns)
