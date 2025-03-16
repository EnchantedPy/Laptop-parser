import requests
from let import *

def collect_data():
    page = 1
    result = []
    product_num = 0

    while True:
        ua = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
        url = f'https://im.comfy.ua/api/products/search?filter=category__120__&urlKey=notebook&cityId=506&storeId=5&size=50&page={page}&sortBy=&order=&showMarkdown=false'

        r = requests.get(url=url, headers={'user-agent': ua})
        data = r.json()
        products = data.get('items')

        if not products:
            break

        for i in products:
            product_num += 1
            product_name = i.get('name')
            product_url = "https://comfy.ua/ua" + i.get('url')
            product_brand = i.get('brand')['name']
            product_images = 'https://comfy.ua/' + i.get('images')[0]['url']
            product_price = i.get('prices')
            product_attributes = i.get('topAttributes')

            result.append(
                {
                    'num': product_num,
                    'name': product_name,
                    'url': product_url,
                    'brand': product_brand,
                    'images': product_images,
                    'price': product_price,
                    'attributes': product_attributes
                }
            )

        if len(products) < 50:
            break
            
        print(f'\rPage #{page} processed...', end='', flush=True)
        page += 1
    return result

def main():
    brands, cpus, gpus, min_price, max_price = get_user_input()
    products = collect_data()
    filtered_products = filter_by_something(products, brands, cpus, gpus, min_price, max_price)
    save_filtered_products(filtered_products)
    print("Filtered products saved successfully")

if __name__ == '__main__':
    main()