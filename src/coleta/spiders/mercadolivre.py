import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/smartphone#topkeyword"] #faz o request na página
    count_page = 1
    max_page = 10

    def parse(self, response):
        produtos = response.css('div.ui-search-result__content-wrapper') #busca todos os itens selecionados
        for produto in produtos:
           
           prices = produto.css('span.andes-money-amount__fraction::text').getall()
           cents = produto.css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').getall()

           yield {
               'barnd': produto.css('h2.ui-search-item__title::text').get(),
               'old_price': prices[0] if len(prices) > 0 else None,
               'old_price_cents': cents[0] if len(cents) > 0 else None,
               'new_price': prices[1] if len(prices) > 1 else None,
               'new_price_cents': cents[1] if len(cents) > 1 else None,
               'reviews_rating_number':produto.css('span.ui-search-reviews__rating-number::text').get(),
               'reviews_amount': produto.css('span.ui-search-reviews__amount::text').get()
               } #categoriza o que eu quero dentro do bloco
        
        if self.count_page < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)')
            if next_page:
                self.count_page += 1
                yield scrapy.Request(url=next_page, callback=self.parse)