
import ollama
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import logging
logging.basicConfig(level=logging.WARNING)


option = int(input("Welcome to the CLI news reader! Enter 1 for direct news scraping, 2 for direct news summary , 3 for both: "))
# world_urls = {
#     "BBC": "https://www.bbc.com/news",
#     "Reuters": "https://www.reuters.com/world/",
#     "AP News": "https://apnews.com/world-news",
#     "Al Jazeera": "https://www.aljazeera.com/news/",
#     "NPR World": "https://www.npr.org/sections/world/"
# }
# indian_urls = {
#     "The Hindu": "https://www.thehindu.com/news/national/",
#     "Indian Express": "https://indianexpress.com/section/india/",
#     "NDTV India": "https://www.ndtv.com/india",
#     "Hindustan Times": "https://www.hindustantimes.com/india-news",
#     "Times of India": "https://timesofindia.indiatimes.com/india"
# }

# business_urls = {
#     "Mint": "https://www.livemint.com/",
#     "Economic Times": "https://economictimes.indiatimes.com/",
#     "Reuters Business": "https://www.reuters.com/business/",
#     "Bloomberg": "https://www.bloomberg.com/",
#     "CNBC": "https://www.cnbc.com/world/"
# }

# tech_urls = {
#     "TechCrunch": "https://techcrunch.com/",
#     "Ars Technica": "https://arstechnica.com/",
#     "The Verge": "https://www.theverge.com/",
#     "Wired": "https://www.wired.com/",
#     "Hacker News": "https://news.ycombinator.com/"
# }

world_urls = {
    "BBC": "https://www.bbc.com/news"
}

indian_urls = {
    "BBC India": "https://www.bbc.com/news/world/asia/india"
}
total_urls = world_urls.copy()
total_urls.update(indian_urls)

def fetch_news(i,url):
    extracted_news=[]
    src = f"Source:{i} "
    logging.debug(src)
    extracted_news.append(src)
    r=requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    nh2 =[]
    for tag in soup.find_all("h2"):
        text = tag.get_text(strip=True)
        if(len(text)>20):
            nh2.append(text)
    logging.debug(nh2)
    extracted_news.extend(nh2)
    return extracted_news

with ThreadPoolExecutor(max_workers=3) as executor:
    responses = executor.map(fetch_news,total_urls.keys(),total_urls.values())

total_response = []
for news_response in responses:
    total_response.append(news_response)

world_news = total_response[0][1:11]
indian_news = total_response[1][1:11]
if option == 1 or option==3:
    print("World news (BBC):")
    for headline in world_news:
        print(headline)
    print("Indian news (BBC):")
    for headline in indian_news:
        print(headline)
    # print(total_response[0][:11])
    # print(total_response[1][:11])
if option == 2 or option==3:
    prompt = """
    You are a news editor.

    Below is a list of headlines from BBC and BBC India.

    Remove duplicates and keep the most important stories.

    Output format:

    # Daily News Feed (World)

    • Headline

    • Headline

    • Headline

    # Daily News Feed (India)

    • Headline

    • Headline

    • Headline

    Do not summarize.
    Do not explain.
    Do not analyze.
    Output only the final news feed.

    Headlines:
    """ + str(" ".join(world_news))
    response = ollama.generate(
        model = "gemma4:e2b",
        prompt = prompt
    )

    print(response["response"])

