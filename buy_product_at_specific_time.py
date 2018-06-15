"""
Buy a product by index on the page at specific time
"""

from datetime import datetime
from pprint import pprint
import time

if __name__ == "__main__":
    from config import USER_INFO
    from shop import Shop

    shop = Shop("http://some-website")

    buy_product_at = datetime(year=2018, month=6, day=8, hour=21, minute=4)

    while datetime.now() < buy_product_at:
        time.sleep(10)

    product_number = 21
    product_url = shop.get_all_product_urls(catalog_url="/shop/all/tops_sweaters")[
        product_number - 1
    ]

    product = shop.buy_product(
        product_url=product_url,
        product_style="White",
        product_size="XLarge",
        user_info=USER_INFO,
    )

    if product is None:
        print(
            "ERROR: The purchase could not be completed. For more details, read the messages above!"
        )
    else:
        pprint(product)
