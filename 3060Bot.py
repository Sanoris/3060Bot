import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
import re
import os
from twilio.rest import Client as SMS
import time
import concurrent.futures
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Change this directory to your chromedriver.exe file
PATH = "D:\chromedriver.exe"

class Client():
    def __init__(self, url, number):
        self.phone = number
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        self.url = url
        self.BBbtn = re.compile(r">add to cart<", re.IGNORECASE)
        self.MicroRE = re.compile(r"<span>in stock</span>", re.IGNORECASE)
        self.number ='+1' + number
        self.SentSMS = False
        self.inCart = False

        #This block notifies you when the purchase process has been initiated
        #So probably get your own license - it's free
        self.sid = ''
        self.auth_token = ''
        self.twiphone = ''
        self.SMSclient = SMS(self.sid, self.auth_token)

        #Fill out your info here
        self.CreditCardNum = ''
        self.CVV = ''
        self.address1 = ''
        self.address2 = ''
        self.name1 = ''
        self.name2 = ''
        self.city = ''
        self.zip = ''
        self.email = ''

    def checkBB(self):
        try:
            with requests.get(self.url, headers=self.headers, timeout=5) as resp:
                #print(resp.content.decode())
                match = self.BBbtn.search(resp.content.decode())

                if(match == None):
                    print('Nope at ' + self.url)
                else:
                    self.SendAlert()
                    self.BuyBB()
        except Timeout:
            print('Request timed out')

    def BuyBB(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(self.url)
        while(q):
            if(not self.inCart):
                try:
                    element = self.driver.find_element_by_xpath("//button[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")
                    element.click()
                except:
                    print('waiting...')
            try:
                checkoutElement = self.driver.find_element_by_xpath("//div[@class='dot']")
                self.inCart = True
                self.driver.get('https://www.bestbuy.com/checkout/r/fulfillment')
                break
            except:
                print('waiting..........')

        while(q):
            try:
                if(self.driver.find_element_by_xpath('//input[@id="user.emailAddress"]')):
                    user_field = self.driver.find_element_by_xpath('//input[@id="user.emailAddress"]')
                    user_field.click()
                    user_field.click()
                    user_field.send_keys(self.email)

                num_field = self.driver.find_element_by_xpath('//input[@id="user.phone"]')
                num_field.send_keys(self.phone)

                self.driver.find_element_by_xpath('//button[@class="btn btn-lg btn-block btn-secondary"]').click()
                break
            except:
                print('Uh Oh')

        while(q):
            try:
                #self.driver.find_element_by_xpath('//buton[@class="btn btn-link v-medium address-form__showAddress2Link"]').click()
                self.driver.execute_script("document.getElementById('payment.billingAddress.state').children[53].selected = true")
                Name1 = self.driver.find_element_by_xpath('//input[@id="payment.billingAddress.firstName"]')
                Name2 = self.driver.find_element_by_xpath('//input[@id="payment.billingAddress.lastName"]')
                Address1 = self.driver.find_element_by_xpath('//input[@id="payment.billingAddress.street"]')
                #Address2 = self.driver.find_element_by_xpath('//input[@id="payment.billingAddress.street2"]')
                City = self.driver.find_element_by_xpath('//input[@id="payment.billingAddress.city"]')
                ZIP = self.driver.find_element_by_xpath('//input[@id="payment.billingAddress.zipcode"]')
                CC = self.driver.find_element_by_xpath('//input[@id="optimized-cc-card-number"]')

                CC.send_keys(self.CreditCardNum)
                Address1.click()
                Address1.click()
                Address1.send_keys(self.address1)
                Name1.click()
                Name1.click()
                Name1.send_keys(self.name1)
                Name2.click()
                Name2.click()
                Name2.send_keys(self.name2)
                #Address2.send_keys(self.address2)
                City.send_keys(self.city)
                ZIP.send_keys(self.zip)
                self.driver.execute_script("document.getElementsByName('expiration-month')[0].children[12].selected = true")
                self.driver.execute_script("document.getElementsByName('expiration-year')[0].children[1].selected = true")
                CCid = self.driver.find_element_by_xpath('//input[@id="credit-card-cvv"]')
                CCid.send_keys(self.CVV)
                self.driver.execute_script("document.getElementById('payment.billingAddress.state').children[53].selected = true")
                #ORDER!!!!!!!!!
                self.driver.find_element_by_xpath('//button[@class="btn btn-lg btn-block btn-primary" and @data-track="Place your Order - Contact Card"]').click()
                break
            except:
                print('Uh oh...')
            

    def checkMicroCenter(self):
        try:
            with requests.get(self.url, headers=self.headers, timeout=5) as resp:
                #print(resp.content.decode())
                match = self.MicroRE.search(resp.content.decode())

                if(match == None):
                    print('Nope at ' + self.url)
                else:
                    if(not self.SentSMS):
                        self.SendAlert()
                        self.SentSMS = True
        except Timeout:
            print('Request timed out')
        return "K"

    def SendAlert(self):
        if(not self.SentSMS):
            self.SMSclient.messages.create(
                from_=self.twiphone,
                body='Found one in stock!\n'+self.url,
                to=self.number
            )

#probably pull this out later
def main():
    URLS = ['https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402',
        'https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-3060-ti-ventus-2x-oc-bv-8gb-gddr6-pci-express-4-0-graphics-card-black/6441172.p?skuId=6441172',
        'https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3060-ti-gaming-oc-8g-gddr6-pci-express-4-0-graphics-card-black/6442484.p?skuId=6442484',
        'https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3060-ti-eagle-oc-8g-gddr6-pci-express-4-0-graphics-card-black/6442485.p?skuId=6442485',
        'https://www.bestbuy.com/site/evga-geforce-rtx-3060-ti-xc-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444445.p?skuId=6444445',
        'https://www.bestbuy.com/site/evga-geforce-rtx-3060-ti-ftw3-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444444.p?skuId=6444444',
        'https://www.bestbuy.com/site/evga-geforce-rtx-3060-ti-ftw3-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444449.p?skuId=6444449',
        'https://www.bestbuy.com/site/pny-geforce-rtx-3060ti8gb-uprising-dual-fan-graphics-card/6446660.p?skuId=6446660']

    BestBuyClients = []
    for url in URLS:
        BestBuyClients.append(Client(url, '')) #Add your phone number between ''
    
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=100)
    while(q):
        #threadpool.submit(micro.checkMicroCenter)
        #threadpool.submit(micro2.checkMicroCenter)
        for c in BestBuyClients:
            threadpool.submit(c.checkBB)
        time.sleep(5)


if __name__ == '__main__':
    q = True
    try:
        main()
    except KeyboardInterrupt:
        q = False