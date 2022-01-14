__version__ = '0.1'
__author__ = 'rbascio'

import requests
import smtplib
import sys
import argparse
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import BestBuy
import GFX

BASE_SEARCH_DICTIONARY = { 'amd': [],
                            'nvidia': ['3060', '3070', '3080']
                         }
BASE_HEADERS = { 'User-Agent': 'Mozilla/5.0' }
BASE_SUBJECT = 'New Graphics Cards in Stock'
TEST_SUBJECT = 'GFXScrape TEST'

parser = argparse.ArgumentParser()
parser.add_argument('email_user')
parser.add_argument('email_pass')
parser.add_argument('email_recipients')
parser.add_argument('-t', '--test', action='store_true')

def fetch_search_results(urls):
    pages = []

    if not urls:
        return pages
    
    for url in urls:
        response = requests.get(url, headers=BASE_HEADERS)
        if response.status_code != 200:
            continue
        pages.append(response.content)
    return pages

def find_gfx_item_name(gfx_soup, header_class_name):
    sku_header_html = gfx_soup.find(class_=header_class_name)
    sku_title = sku_header_html.a.string
    return sku_title

def find_gfx_item_instock_status(gfx_soup, button_class_name):
    instock_button_html = gfx_soup.find('button', class_= button_class_name)
    instock_status = instock_button_html.text
    return instock_status

def find_gfx_item_url(gfx_soup, url_class_name, base_url='{}'):
    sku_header_html = gfx_soup.find(class_=url_class_name)
    sku_url = sku_header_html.a.get('href')
    full_url = base_url.format(sku_url)
    return full_url

# Go to the Product page and verify the Add To Cart Button
def validate_gfx_item_instock(gfx_instock, button_class_name, invalid_statuses):
    valid_gfx_instock = [] 
    for gfx in gfx_instock:
        product_page = fetch_search_results([gfx.url])

        if not product_page:
            return valid_gfx_instock

        product_soup = BeautifulSoup(product_page[0], 'html.parser')
        instock_status = find_gfx_item_instock_status(product_soup, button_class_name)
        if(instock_status not in invalid_statuses):
            valid_gfx_instock.append(gfx)
    return valid_gfx_instock

def create_gfx_stock(gfx_html_items, company_name, 
                    header_class_name, button_class_name, 
                    url_class_name, base_url='{}'):
    gfx_stock = []
    for gfx_html in gfx_html_items:
        gfx_name = find_gfx_item_name(gfx_html, header_class_name)
        gfx_instock_status = find_gfx_item_instock_status(gfx_html, button_class_name)
        gfx_item_url = find_gfx_item_url(gfx_html, url_class_name, base_url)
        gfx_item = GFX.GFX(gfx_name,gfx_item_url, gfx_instock_status, company_name)
        print(gfx_item.to_string())
        gfx_stock.append(gfx_item)
    return gfx_stock

def parse_pages_with_beautiful_soup(pages, list_class_name, 
                    company_name, header_class_name, 
                    button_class_name, url_class_name, base_url='{}'):
    gfx_stock_list = []
    for page in pages:
        soup = BeautifulSoup(page, 'html.parser')
        gfx_html_items = soup.find_all(class_=list_class_name)
        gfx_stock = create_gfx_stock(gfx_html_items, company_name, header_class_name,
                                    button_class_name, url_class_name, base_url)
        gfx_stock_list.extend(gfx_stock)
    return gfx_stock_list

def build_instock_list(stock, invalid_statuses):
    gfx_instock = []
    if not stock:
        return gfx_instock
    for item in stock:
        print(item.instock_status)
        if(item.instock_status not in invalid_statuses):
            gfx_instock.append(item)
    return gfx_instock

def send_instock_emails(instock_gfx, email_user, email_pass, email_recipients, email_subject):
    if not instock_gfx:
        return
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    email_sender = 'gfxscraper@gmail.com'
    email_to = email_recipients
    msg_body_base = '<h4>New Graphics Cards in Stock</h4><ul>{}</ul>'
    msg_body_li = ''
    for gfx in instock_gfx:
        instock_li = '<li><a href="{}">{}</a> in stock at {}</li>'.format(gfx.url, gfx.name, gfx.store)
        msg_body_li = msg_body_li + instock_li
    msg_body = msg_body_base.format(msg_body_li)
    msg = MIMEText(msg_body, 'html', 'utf-8')
    msg['Subject'] = email_subject
    mail_server.login(email_user, email_pass)
    mail_server.sendmail(email_sender, email_to, msg.as_string())
        

def main(search_dictionary, email_user, email_pass, email_recipients, email_subject):
    instock_gfx = []
    best_buy = BestBuy.BestBuy(search_dictionary)
    pages = fetch_search_results(best_buy.search_strings)
    best_buy_stock = parse_pages_with_beautiful_soup(pages, best_buy.list_class_name,
                                                    'Best Buy', best_buy.header_class_name,
                                                    best_buy.button_class_name,best_buy.url_class_name, 
                                                    best_buy.base_url)
    instock_best_buy_gfx = build_instock_list(best_buy_stock, best_buy.invalid_statuses)
    print(instock_best_buy_gfx)
    validated_instock_bestbuy_gfx = validate_gfx_item_instock(instock_best_buy_gfx, best_buy.button_class_name, best_buy.invalid_statuses)
    send_instock_emails(validated_instock_bestbuy_gfx, email_user, email_pass, email_recipients, email_subject)

if __name__ == '__main__':
    args = parser.parse_args()
    search_dictionary = BASE_SEARCH_DICTIONARY
    email_subject = BASE_SUBJECT
    if(args.test):
        print('Finding Test to be true')
        search_dictionary = { 'nvidia': ['GT1030'] }
        email_subject = TEST_SUBJECT
    email_user = args.email_user
    email_pass = args.email_pass
    email_recipients = args.email_recipients.split(',')
    print(search_dictionary)
    main(search_dictionary, email_user, email_pass, email_recipients, email_subject)