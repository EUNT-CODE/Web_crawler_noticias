from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from bs4 import BeautifulSoup

options=webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
base_url="https://myanimelist.net/news"
news_list=[]
def extract_news():
    driver.get(base_url)
    time.sleep(5)
    soup=BeautifulSoup(driver.page_source, "html.parser")
    articles=soup.find_all("div", class_="news-unit")
    if not articles:
        print("No se encontraron noticias")
    for article in articles:
        title=article.find("p", class_="title").find("a").text.strip() if article.find("p", class_="title") else "Titulo no disponible"
        link=article.find("p", class_="title").find("a")["href"] if article.find("a") else "No disponible"
        description=article.find("div", class_="text").text.strip() if article.find("div", class_="text") else "Descripcion no disponible"
        print(f"Titulo: {title}")
        print(f"Enlace: {link}")
        print(f"Descripcion: {description}")
        news_list.append({ "Titulo": title, "Descripcion": description, "Enlace": link, })
extract_news()
df = pd.DataFrame(news_list)
print(df.head())
df.to_csv("noticias_anime.csv", index=False, encoding="utf-8")
print("Archivo csv generado con exito.")

driver.quit()