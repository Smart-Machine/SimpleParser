import scrapy 

class PrinterSpider(scrapy.Spider):
    name = "printers"
    start_urls = ["https://www.emag.ro/search/imprimanta+foto+portabila"]

    next_counter = 2

    def get_price(self, s):
        data = s.split("sup")
        b = "" 
        for m in data:
            for i in m:
                if i.isdigit():
                    b += i
            b += "."
        return b

    def parse(self, response):
        for products in response.css("div.card-item.card-standard.js-product-data"):
            try:
                yield {
                        'name' : products.css('a.card-v2-title.semibold.mrg-btm-xxs.js-product-url::text').get(),
                        'price': self.get_price(products.css("p.product-new-price").get()),
                        'link' : products.css("a.card-v2-title.semibold.mrg-btm-xxs.js-product-url").attrib['href'] 
                        }
            except:
                print("ERROR")

        
        next_page = f"https://www.emag.ro/search/imprimanta+foto+portabila/p{self.next_counter}" 
        if next_page:
            print(f"WE ARE GOING MADDD\n\n{self.next_counter}\n\n")
            self.next_counter += 1
            yield response.follow(next_page, callback=self.parse)

