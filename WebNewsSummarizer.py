import ollama
from bs4 import BeautifulSoup
import threading
import requests
world_urls = {"CNN":"https://edition.cnn.com/world","BBC":"https://www.bbc.com/news","Reuters":"https://www.reuters.com/"}
indian_urls = {"CNN":"https://edition.cnn.com/world/india"}
def fetch_news():
    extracted_news=""
    for i in world_urls:
        src = f"Source:{i}"
        print(src)
        extracted_news+=src
        r=requests.get(world_urls[i])
        soup = BeautifulSoup(r.content,"html.parser")
        print(soup.text)
        extracted_news+=str(soup.title)
    for i in indian_urls:
        src = f"Source:{i}"
        print(src)
        extracted_news+=src
        r=requests.get(indian_urls[i])
        soup = BeautifulSoup(r.content)
        print(soup.title)
        extracted_news+=str(soup.title)
    return extracted_news

extracted_news = fetch_news()
response = ollama.generate(
    model = "gemma4:e2b",
    prompt = "This is the extracted news dump from multiple major sites. Make sure to summarize only the news articles in the extracted data. Make sure to ignore all of the other links you would typically find in a news website. Only focus on the news articles"+extracted_news
)

print(response)

