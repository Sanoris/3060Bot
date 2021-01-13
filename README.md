# 3060Bot
This is a bot to buy items from Best Buy when they are available at a given URL.

!IMPORTANT Read this entire document please!

At a rate of 1 scan per 5 seconds, we check to see if all target urls listed in URL[] at line 156 have an item that is not sold out.
If it is not sold out, you will recieve a message that the item is available along with the link, and the process of buying the item will be initiated.
By default, this program will attempt to buy each item at the URLs listed, so be careful if you don't want to buy 8 3060 ti's
This code bypasses BestBuy's security measures that prevent bots from buying items as soon as they appear. 

libraries required:
twilio
bs4
selenium

Things you need to change to make this work for you:
Download the chrome webdriver appropriate to you at https://sites.google.com/a/chromium.org/chromedriver/downloads
Change line 14 to the directory your chromedriver.exe is located

Activate a twilio account and insert your credentials in lines 29-31
OR comment out lines 32&53 if you do not want text alerts from twilio

Fill out your credentials for lines 35-43

Run the program and wait :)
