import scrapy


class GoldSpider(scrapy.Spider):
    name = "gold"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/"]

    def parse(self, response):
        for category_link in response.xpath(
            "//aside//div[contains(@class,'sidebar-category')]//div[@class ='box-content']//ul[@class='dropmenu']/li/a[@class='activSub']"
        ):
            href = category_link.xpath("./@href").get()
            text = category_link.xpath("./text()").get()

            if href and text:
                yield response.follow(
                    response.urljoin(href), self.parse_category, meta={"category": text}
                )

    def parse_category(self, response):
        category = response.meta.get("category", "Unknown Category")
        for product in response.css(".product-layout"):
            price = product.css(".price .price-new::text").get(default=None)

            if price is not None:
                price = price.strip()
            else:
                price = product.css(".price::text").get()
            product_url = product.css(".image a::attr(href)").get()

            product_data = {
                "category": category,
                "product": {
                    "title": product.css(".caption h4 a::text")
                    .get(default="No title available")
                    .strip(),
                    "price": price,
                    "description": product.css(".desc::text")
                    .get(default="No description available")
                    .strip(),
                    "image_url": product.css(".image img::attr(src)").get(
                        default="No image available"
                    ),
                },
            }
            if product_url:
                yield response.follow(
                    product_url,
                    self.parse_product_detail,
                    meta={"product": product_data, "product_url": product_url},
                )

    def parse_product_detail(self, response):
        product_data = response.meta.get("product", {})
        brand = response.xpath("//li[span[contains(text(),'Brand:')]]/a/text()").get(
            default="Unknown Brand"
        )
        product_code = response.xpath(
            "//li[span[contains(text(),'Product Code:')]]/text()"
        ).get(default="Unknown Code")
        product_data["product"].update(
            {
                "brand": brand,
                "product_code": product_code,
            }
        )
        yield product_data
