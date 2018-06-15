"""
Display the product information by its index on the page
"""

from pprint import pprint

if __name__ == "__main__":
    from shop import Shop

    shop = Shop("http://some-website")

    product_number = 21
    product_url = shop.get_all_product_urls(catalog_url="/shop/all/tops_sweaters")[
        product_number - 1
    ]

    pprint(shop.get_product_info(product_url=product_url))
