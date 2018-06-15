"""
Tries to buy a specified product (by its index on a page, `product_number`) until it succeeds (retries every 10 minutes)
"""
from pprint import pprint
import time


if __name__ == "__main__":
    from config import USER_INFO
    from shop import Shop

    shop = Shop("http://some-website")
    catalog_url = "/shop/all/tops_sweaters"
    product_number = 21

    while True:
        product_url = shop.get_all_product_urls(catalog_url=catalog_url)[
            product_number - 1
        ]
        product = shop.buy_product(
            product_url=product_url,
            product_style="White",
            product_size="XLarge",
            user_info=USER_INFO,
        )
        if product is not None:
            pprint(product)
            break

        # Retry in 10 minutes
        time.sleep(10 * 60)
