import scrapy
class HomesSpider(scrapy.Spider):
    name = "homes"
    file=open("homes.txt","a",encoding="utf-8")
    home_count=1
    page_count=0
    start_urls = [
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili/2-otaqli?page=1'
    ]
    
    def parse(self,response):
        bill_of_sale=response.css("div.bill_of_sale").extract()
        house_doc=response.css("div.abs_block").extract()
        location=response.css("div.card_params div.location::text").extract()
        prices=response.css("div.price span.price-val::text").extract()     
        azn=response.css("div.price span.price-cur::text").extract_first()
        house_area=response.css("ul.name li:nth-child(2)::text").extract()
        house_floor=response.css("ul.name li:nth-child(3)::text").extract()
        room_count= response.css("ul.name li:first-child::text").extract()
        i=0
   
        self.page_count+=1
  
        while i<len(house_area):   
            if "bill_of_sale" in house_doc[i]:
                kupca="var"
                self.file.write("--------------------------------------------------"+ "\n")
                self.file.write("Page "+str(self.page_count) + ".\n")
                self.file.write("Mənzil N:" + str(self.home_count)+ ".\n") 
                self.file.write("Mərtəbə: "+ house_floor[i] + "\n")
                self.file.write("Sahə:"+ house_area[i] + "\n")
                self.file.write("Otaq sayı: "+ room_count[i] + "\n")
                self.file.write("Kupça: " + kupca +"\n")
                if "mortgage" in house_doc[i]:
                    ipoteka="var"
                    self.file.write("İpoteka: " + ipoteka +"\n")
                self.file.write("Qiymət: "+ prices[i] + " "+azn + "\n")
                self.file.write("Yerləşir: "+ location[i] + "\n")
                self.file.write("--------------------------------------------------"+ "\n")
                self.home_count += 1
            i+=1     
            
            
        next_url=response.css("span.next a::attr(href)").extract_first()
        if next_url is not None:
            next_url="https://bina.az"+ next_url
            yield scrapy.Request(url=next_url,callback=self.parse)
        else:
            self.file.close()

    """link=response.css("div.bill_of_sale a.item_link::attr(href)").extract() 28 link var https://bina.az/baki/alqi-satqi/menziller/kohne-tikili/2-otaqli?page=1
    while i<len(link):
        house_link="https://bina.az/" + link[i] 
        doc_have=response.css(" tr:nth-child(5)  td:nth-child(2)::text").extract_first() meselen https://bina.az/items/1339417 saytindaki VAR dir"""