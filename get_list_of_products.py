"""
List all the products (URLs)
"""
from pprint import pprint

if __name__ == "__main__":
    from shop import Shop

    shop = Shop("http://some-website")

    pprint(shop.get_all_product_urls())
    # pprint(shop.get_all_product_urls('/shop/all/skate'))
    # pprint(shop.get_all_product_urls('/shop/all/tops_sweaters'))
