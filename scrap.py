from bs4 import BeautifulSoup
import requests
import csv
import time
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

def getstarscount(tag):
    return len(tag.findChildren('img',attrs={'class':'css-177n1u3'}))

def getproductdesc(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url_clean = "https://"+url[url.find('www.tokopedia.com'):].replace('%2F','/').replace('%3F','?')
    time.sleep(1)
    r = requests.get(url_clean, headers=headers)
    prser = BeautifulSoup(r.text, 'html.parser')

    desc = prser.find('div',attrs={'data-testid':'lblPDPDescriptionProduk'})
    img =  prser.find('img',attrs={'class':'success fade'})
    return desc.text.encode('utf-8'), img.get('src').encode('utf-8')

def makecsv(data):
    header = ['Product Name','Description','Image link','Price','Rating','Merchant']
    f = open('toped.csv', 'w')
    writer = csv.writer(f,lineterminator="\n")
    writer.writerow(header)

    print("Writing Products")
    for d in data:
        writer.writerow(d)

    f.close()


# option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(executable_path='/Users/rofi.alfarid/Downloads/chromedriver')

driver.get('https://www.tokopedia.com/p/handphone-tablet/handphone')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(3)
test = driver.page_source

# url = "https://www.tokopedia.com/p/handphone-tablet/handphone"
# headers = {'User-Agent':'Mozilla/5.0'}
#
# r = requests.get(url, headers=headers)
soup = BeautifulSoup(test, 'html.parser')
#
print("Searching Products")
prds = soup.find_all('div',attrs={'class':'css-bk6tzz e1nlzfl3'})

print(prds)
prd_info = [[]]

print("Parsing Products")
for p in prds:
    print(p)
    url = p.findChild('a', attrs={'class': 'css-89jnbj'}).get('href')
    prd_name = p.findChild('span', attrs={'class': 'css-1bjwylw'}).text.encode('utf-8')
    prd_merchant = p.findChildren('span', attrs={'class': 'css-1kr22w3'})[1].text.encode('utf-8')
    prd_stars = len(p.findChildren('img', attrs={'alt': 'star'}))
    prd_price = p.findChild('span', attrs={'class': 'css-o5uqvq'}).text.encode('utf-8')
    prd_desc, prd_img = getproductdesc(url)

    prd = [prd_name,prd_desc,prd_img,prd_price,prd_stars,prd_merchant]
    prd_info.append(prd)

makecsv(prd_info)
print("Success")



