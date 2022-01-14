# GFXScrape User Guide

## Purpose

To explain the purpose of the GFXScrape Python Utility Script and how to use it.
The GFXScrape script is used to scrape the contents of various websites for graphics
card availibility. This tool WILL NOT automatically order products but merely alert you when a predefined list of options are available for order.

## Tools Used

1. [Python Requests Library]()
2. [BeautifulSoup 4]()

## Current Stores Available to Search

- BestBuy.com

## Notes

1. BestBuy.com
    1. BestBuy.com uses pagination at the server level. It is rececommended you keep search terms specific enough to show < 24 items in the results
    2. The Add To Cart button (designated by class fulfillment-add-to-cart-button) will have the internal text of 'Sold Out' when a product is sold out.
      - This button is actually in the following format
      ```html
        <div class="fulfillment-add-to-cart-button">
            <button>
               {'Sold Out' || 'Add To Cart' || 'See Details'}
            </button
        </div>
      ```

## Setup

1. Ensure Python 3 is installed
2. Install BeautifulSoup 4 using pip
3. Install requests using pip

## Usage

1. Manually
   1. Run the following script in a terminal, command prompt, etc
   2. python3 /path_to_script/GFXScrape.py email_from_account email_from_account_password 'comma_seperated_list_of_emails_to_send_to'
   3. -t
      1. Runs the script in Test mode which will pull from a known card that is ALWAYS in stock (configured in args.test conditional in GFXScrape)
2. Automatically (recommended)
   1. If running on Linux, create a new Cron entry that will run at the frequency you want by editing the crontab
      1. crontab -e
   2. CrontTab Example
      1. * * * * *  python3 /path_to_scrape/GFXScrape test@gmail.com Password123 'test@gmail.com'