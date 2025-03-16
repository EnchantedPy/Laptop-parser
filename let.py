import json

async def filter_by_something(products, brands, cpus, gpus, min_price, max_price):
    filtered_products = []

    for product in products:
        product_brand = product["brand"].strip().lower()
        product_cpu = next((attr["value"] for attr in product["attributes"] if attr["label"] == "Модель центрального процесора"), "").strip().lower()
        product_gpu = next((attr["value"] for attr in product["attributes"] if attr["label"] == "Модель графічного процесора"), "").strip().lower()
        product_price = product["price"].get("price", 0)

        if (min_price is None or float(product_price) >= min_price) and (max_price is None or float(product_price) <= max_price):
            if (not brands or product_brand in brands) and \
                (not cpus or any(cpu in product_cpu for cpu in cpus)) and \
                (not gpus or any(gpu in product_gpu for gpu in gpus)):
                filtered_products.append(product)
    return filtered_products

async def get_user_input():
    brands = input("Choose brand(s) (HP, Asus, Acer, Apple, Lenovo, Xiaomi, Gigabyte). Tap 'Enter' to skip: ").strip().lower().split(',')
    cpus = input("Choose CPU model(s) (Core i3, i5, i7, i9 | Ryzen 3, 5, 7, 9 | M1, 2, 3). Tap 'Enter' for any CPU: ").strip().lower().split(',')
    gpus = input("Choose GPU model(s) (GeForce GTX(1080, 1660) RTX(2050, 3050, 3060, 4050, 4060, 4090) | Radeon RX). Tap 'Enter' to for any GPU: ").strip().lower().split(',')
    price_range = input("Enter price range as ('min price', 'max price') (e.g., 30000, 40000). Enter 'Skip' to allow any price: ").strip().lower()
    brands = [brand.strip() for brand in brands if brand]
    cpus = [cpu.strip() for cpu in cpus if cpu]
    gpus = [gpu.strip() for gpu in gpus if gpu]

    if price_range != "skip" and price_range:
        try:
            min_price, max_price = map(float, price_range.split(','))
        except ValueError:
            min_price, max_price = None, None
    else:
        min_price, max_price = None, None

    return brands if brands else None, cpus if cpus else None, gpus if gpus else None, min_price, max_price

async def save_filtered_products(filtered_products):
    with open('result.json', 'w', encoding='UTF-8') as f:
        json.dump(filtered_products, f, indent=4, ensure_ascii=False)