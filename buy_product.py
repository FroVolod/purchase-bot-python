"""
Buy a product of a specific style (color) and size by URL
"""
from pprint import pprint

if __name__ == "__main__":
    from config import USER_INFO
    from shop import Shop

    shop = Shop("http://some-website")

    # This is "Jacquard Logo Silk Polo", which has different styles (colors) and sizes,
    # so you specify those config options via `product_style` and `product_size` parameters.
    product = shop.buy_product(
        product_url="/shop/shirts/l9t7jgefb/nva2e8r67",
        product_style="pale yellow",
        product_size="Large",
        user_info=USER_INFO,
    )

    # This is "Independent® Truck", which doesn't have any styles, but has sizes,
    # so you only need to specify `product_size` parameter.
    # product = shop.buy_product(
    #    product_url='/shop/skate/teiunwfb3',
    #    product_size='129',
    #    user_info=USER_INFO
    # )

    # This is "Ganesh Keychain", which doesn't have any sizes, but has a style (Gold),
    # so you omit the `product_size` parameter and only specify `product_style`
    # product = shop.buy_product(
    #    product_url='/shop/accessories/xcujpwfq4',
    #    product_style='Gold',
    #    user_info=USER_INFO
    # )

    if product is None:
        print(
            "ERROR: The purchase could not be completed. For more details, read the messages above!"
        )
    else:
        pprint(product)
