"""
Display the product information by URL
"""

from pprint import pprint

if __name__ == "__main__":
    from shop import Shop

    shop = Shop("http://some-website")

    pprint(shop.get_product_info(product_url="/shop/jackets/pxakc9yqe/ghvud8p49"))
