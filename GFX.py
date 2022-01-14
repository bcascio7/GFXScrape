class GFX:
    'Object representing a Graphics card item from a website'
    store = ''
    name = ''
    url = ''
    instock_status = ''

    def __init__(self, name, url, instock_status, store=''):
        self.name = name
        self.url = url
        self.instock_status = instock_status
        self.store = store

    def to_string(self):
        return '{} - {} is currently: {}'.format(self.store, self.name, self.instock_status)