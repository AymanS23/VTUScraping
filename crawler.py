# -*- coding: utf-8 -*-
import scrapy
import pytesseract
from PIL import Image
import re
import math
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
class captchaclass:
    
    def solve_captcha(self):
        #BREAK CAPTCHA
        driver = webdriver.Chrome(executable_path='C:\\Users\\GV62\\Downloads\\selechrome\\chromedriver_win32\\chromedriver.exe')
        driver.get("http://results.vtu.ac.in/resultsvitavicbcs_19/index.php")
        img = driver.find_elements(By.TAG_NAME, "img")
        src = img[1].get_attribute('src')
        #print("##################################################")
        print(src)
        loc = img[1].location
        size = img[1].size
        print(loc,size)
        driver.save_screenshot('ss.png')
        im = Image.open('ss.png')
        left = loc['x']
        top = loc['y']
        right = loc['x'] + size['width']
        bottom = loc['y'] + size['height']
        im = im.crop((left,top,right,bottom))
        im.show()
        im.save('ss.png')
        try:
            captcha_text = pytesseract.image_to_string(Image.open('ss.png'))
        except:
            print("captcha string error")
        print(captcha_text)
        return captcha_text
        #captcha = driver.find_element(By.NAME,'captchacode')
        #captcha.clear()
        #captcha.send_keys(captcha_text)

class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['results.vtu.ac.in']
    start_urls = ['http://results.vtu.ac.in/resultsvitavicbcs_19/index.php']
    
    def parse(self, response):
        c = captchaclass()
        token1 = response.css('input[name="token"]::attr(value)').extract_first()
        retrcap = c.solve_captcha()
        data = {
            'token' : token1 ,
            'lns' : '1PE16CS036' ,
            'captchacode' : retrcap
        }
        yield scrapy.FormRequest(url = self.allowed_domains, formdata = data, callback = self.parse_result)

    def parse_result(self,response):
        for res in response.css('div.divTableRow')[2]:
            yield {
                'sub_code' : res.css('div.divTableCell::text').extract_first()
            }
            
