import ollama
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
world_urls = {
    "BBC": "https://www.bbc.com/news",
    "Reuters": "https://www.reuters.com/world/",
    "AP News": "https://apnews.com/world-news",
    "Al Jazeera": "https://www.aljazeera.com/news/",
    "NPR World": "https://www.npr.org/sections/world/"
}
indian_urls = {
    "The Hindu": "https://www.thehindu.com/news/national/",
    "Indian Express": "https://indianexpress.com/section/india/",
    "NDTV India": "https://www.ndtv.com/india",
    "Hindustan Times": "https://www.hindustantimes.com/india-news",
    "Times of India": "https://timesofindia.indiatimes.com/india"
}

business_urls = {
    "Mint": "https://www.livemint.com/",
    "Economic Times": "https://economictimes.indiatimes.com/",
    "Reuters Business": "https://www.reuters.com/business/",
    "Bloomberg": "https://www.bloomberg.com/",
    "CNBC": "https://www.cnbc.com/world/"
}

tech_urls = {
    "TechCrunch": "https://techcrunch.com/",
    "Ars Technica": "https://arstechnica.com/",
    "The Verge": "https://www.theverge.com/",
    "Wired": "https://www.wired.com/",
    "Hacker News": "https://news.ycombinator.com/"
}
total_urls = world_urls.copy()
total_urls.update(indian_urls)

def fetch_news(i,url):
    extracted_news=""
    src = f"Source:{i} "
    logging.debug(src)
    extracted_news+=src
    r=requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    nt = soup.title
    logging.debug(nt)
    nh1 = soup.find_all("h1")
    logging.debug(nh1)
    nh2 =""
    for tag in soup.find_all("h2"):
        text = tag.get_text(strip=True)
        if(len(text)>20):
            nh2+=text+"\n"
    logging.debug(nh2)
    extracted_news+=str(nt)+str(nh1)+str(nh2)
    return extracted_news

with ThreadPoolExecutor(max_workers=3) as executor:
    responses = executor.map(fetch_news,total_urls.keys(),total_urls.values())

total_response = ""
for news_response in responses:
    total_response+=news_response
print(total_response)
response = ollama.generate(
    model = "gemma4:e4b",
    prompt = "Convert these headlines into a news briefing. For each headline:- Explain what happened.- Keep it to 2-3 sentences."+str(total_response)
)

print(response["response"])

