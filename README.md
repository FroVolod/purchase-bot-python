# Automation for \<some-website\>

NOTE: This is a project I have developed for a website that I cannot name here,
so this project is just for the showcase purposes of how I deliver my projects!

This is a solution made in python that is able to purchase a product on
\<some-website\> based on a few inputs.

## Inputs

1. time to refresh the browser
2. product number (based on the order of the HTML page),
3. sizing choice if applicable, and
4. color choice if applicable.

## Other requirements

1. Ability to fire off at a specific time or when new products are loaded
2. Runs with Python
3. Waits for the element to be loaded to fire the next step (e.g. it does not
   try to enter payment information before the page has loaded or try to click
   the checkout button before it has loaded).

## Usage

1. Install Python 3.5 or newer
2. Install extra project modules buy issuing the following command from the terminal:

    ```
    cd "C:\path\to\the\project\folder"
    pip install -r requirements.txt
    ```
3. Configure the payment and delivery information in `config.py` file
4. Open any of the provided example (`.py` files) in a text editor, scan it
   through and adapt the values (e.g. `catalog_url`, `product_number`,
   `product_url`, or `buy_product_at`)
5. Run a script (there are a few examples in the folder) like this:

    ```
    python buy_product_at_specific_time.py
    ```
