"""
This module implements common methods to interact with some-website from Python.
"""

import requests
from bs4 import BeautifulSoup


class Shop:
    def __init__(self, url):
        self.url = url

    def get_all_product_urls(self, catalog_url="/shop/all"):
        """
        Returns a list of product URLs listed on the given `catalog_url`.

        Examples:

        >>> shop = Shop('http://some-website')
        >>> shop.buy_product(shop.get_all_product_urls('/shop/all/tops-sweaters')[20])
        """
        all_product_urls = []
        if not catalog_url.startswith("http"):
            catalog_url = self.url + catalog_url
        print(
            "Getting all the product URLs form {catalog_url}...".format(
                catalog_url=catalog_url
            )
        )
        response = requests.get(catalog_url)
        response.raise_for_status()
        parsed_page = BeautifulSoup(response.text, "lxml")
        for article in parsed_page.find("div", id="container").find_all("article"):
            all_product_urls.append(article.find("a").get("href"))
        print("OK")
        return all_product_urls

    def buy_product(
        self, product_url, user_info, product_style=None, product_size=None
    ):
        """
        Buys a given product. You must specify at least `product_url` and
        `user_info`, and for some listings, also `product_style` and/or
        `product_size`.

        Examples:

        >>> shop = Shop('http://some-website')
        >>> shop.buy_product('/shop/jackets/que2rcwml/enfa3481d', user_info={...}, product_style='Red', product_size='Small')

        >>> shop.buy_product('/shop/accessories/zevy9f0ku/a3ou256yi', user_info={...}, product_style='White')

        >>> shop.buy_product('/shop/skate/teiunwfb3', user_info={...}, product_size='129')
        """
        product_info = self.get_product_info(product_url)
        _product_style = None if product_style is None else product_style.lower()
        # Check if the provided product style exists for the given product:
        if _product_style in product_info["styles"]:
            product_style_info = product_info["styles"][_product_style]
        else:
            if product_style is None:
                print(
                    "There are {styles} styles, but none selected. Please, specify `product_style`.".format(
                        styles=list(product_info["styles"].keys())
                    )
                )
            else:
                print(
                    'There is no available product "{name}" in style "{style}"'.format(
                        name=product_info["name"], style=product_style
                    )
                )
            return

        product_style_url = product_style_info["href"]
        # Ensure that we open the right page, which corresponds to the specific
        # style of the product:
        if not product_url.endswith(product_style_url):
            product_info = self.get_product_info(product_style_url)
            product_style_info = product_info["styles"][_product_style]

        _product_size = None if product_size is None else product_size.lower()

        # Check if the product is available:
        if (
            product_info["cart_url"] is None
            or _product_size not in product_style_info["sizes"]
        ):
            print(
                'Product "{name}" (Style: {style}, Size: {size}) is not available.'.format(
                    name=product_info["name"], style=product_style, size=product_size
                )
            )
            return

        print(
            'Product "{name}" (Style: {style}, Size: {size}, Price: {price}) is going to be bought...'.format(
                name=product_info["name"],
                style=product_style,
                size=product_size,
                price=product_info["price"],
            )
        )

        with requests.Session() as http_session:
            print("Adding the product to the cart...")
            response = http_session.post(
                self.url + product_info["cart_url"],
                data={
                    "style": product_style_info["id"],
                    "size": product_style_info["sizes"][_product_size],
                },
                headers={
                    "Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
                    "X-Requested-With": "XMLHttpRequest",
                },
            )
            response.raise_for_status()
            print("OK")

            print("Checking out the cart...")
            response = http_session.get(self.url + "/checkout")
            response.raise_for_status()
            parsed_page = BeautifulSoup(response.text, "lxml")
            authenticity_token = parsed_page.find(
                "input", attrs={"name": "authenticity_token"}
            ).get("value")
            print("OK")

            checkout_form_data = user_info.copy()
            checkout_form_data.update(
                {
                    "authenticity_token": authenticity_token,
                    "same_as_billing_address": "1",
                    "store_credit_id": "",
                    "order[terms]": 1,
                }
            )
            print("Finishing the purchase...")
            response = http_session.post(
                self.url + "/checkout.json", data=checkout_form_data
            )
            response.raise_for_status()
            order_info = response.json()
            if order_info["status"] == "failed":
                print(
                    'Product "{name}" (Style: {style}, Size: {size}) could not be bought: {errors}'.format(
                        name=product_info["name"],
                        style=product_style,
                        size=product_size,
                        errors=order_info,
                    )
                )
                return

        print(
            'Product "{name}" (Style: {style}, Size: {size}) has been bought!'.format(
                name=product_info["name"], style=product_style, size=product_size
            )
        )

        return {"product_info": product_info, "order_info": order_info}

    def _parse_product_sizes(self, parsed_product_page):
        sizes = {}
        sizes_box = parsed_product_page.find("select", id="size")
        if sizes_box:
            for size_box in sizes_box.find_all("option"):
                sizes[size_box.text.strip().lower()] = size_box.get("value")
        else:
            sizes[None] = parsed_product_page.find("input", id="size").get("value")
        return sizes

    def get_product_info(self, product_url):
        """
        Returns an information about the product by product URL.

        Examples:

        >>> shop = Shop('http://some-website')
        >>> shop.get_product_info('/shop/jackets/que2rcwml/enfa3481d')
        """
        print("Getting info about a product ({url})...".format(url=product_url))
        if not product_url.startswith("http"):
            product_url = self.url + product_url
        response = requests.get(product_url)
        response.raise_for_status()
        parsed_product_page = BeautifulSoup(response.text, "lxml")
        name = parsed_product_page.find("h1", class_="protect").text.strip()
        styles = {}
        styles_box = parsed_product_page.find("ul", class_="styles")
        if styles_box:
            # Extract the information about each style of the given product:
            for style_box in styles_box.find_all("li"):
                a = style_box.find("a")
                style_info = {
                    "id": a.get("data-style-id"),
                    "href": a.get("href"),
                    "is_sold_out": a.get("data-sold-out") == "true",
                }
                if (
                    product_url.endswith(style_info["href"])
                    and not style_info["is_sold_out"]
                ):
                    style_info["sizes"] = self._parse_product_sizes(parsed_product_page)
                styles[a.get("data-style-name").lower()] = style_info
        else:
            # Extract the information about the product style when there is
            # only a single style or no style at all:
            style_id_box = parsed_product_page.find("input", id="style")
            if not style_id_box:
                style_info = {"id": None, "href": product_url, "is_sold_out": True}
            else:
                style_info = {
                    "id": style_id_box.get("value"),
                    "href": product_url,
                    "is_sold_out": False,
                    "sizes": self._parse_product_sizes(parsed_product_page),
                }
            styles[None] = style_info

        price = parsed_product_page.find("p", class_="price").find("span").text.strip()
        cart_form = parsed_product_page.find("form", id="cart-addf")
        cart_url = cart_form.get("action") if cart_form else None
        print("OK")
        return {"name": name, "styles": styles, "cart_url": cart_url, "price": price}
