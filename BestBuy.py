class BestBuy:
    'Creates the Best Buy class for GFXScrape'
    url = 'https://www.bestbuy.com/site/searchpage.jsp?'
    search_base = 'st={}+grapics+card+{}'
    search_strings = []
    header_class_name = 'sku-header'
    button_class_name = 'add-to-cart-button'
    url_class_name = 'sku-header'
    list_class_name = 'sku-item'
    invalid_statuses = ['Sold Out', 'Pre-Order', 'Coming Soon', 'In Store Only']
    base_url = 'https://www.bestbuy.com{}'

    def __init__(self, search_dictionary = {}):
        'Creates the Base Best Buy Class'
        self.search_strings = self.build_search_strings(search_dictionary)

    def build_search_strings(self, search_dictionary):
        search_strings = []
        for brand in search_dictionary:
            if not search_dictionary[brand]:
                continue
            for model in search_dictionary[brand]:
                search_string = self.search_base.format(brand, model)
                search_url = self.url + search_string
                search_strings.append(search_url)
        return search_strings