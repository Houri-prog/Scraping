import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import datetime

async def scrape_meta_ads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=FR&q=%22immobilier%22&search_type=keyword_exact_phrase"
        await page.goto(url)
        await asyncio.sleep(10)

        for _ in range(5):
            await page.mouse.wheel(0, 8000)
            await asyncio.sleep(2)

        ads_blocks = await page.query_selector_all("div[role='article']")
        ads_data = []

        for ad in ads_blocks:
            try:
                content = await ad.inner_text()
                ads_data.append({
                    "ad_text": content,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except:
                continue

        df = pd.DataFrame(ads_data)
        df.to_csv("ads_immobilier.csv", index=False)
        print("✅ Fichier ads_immobilier.csv généré")

if __name__ == "__main__":
    asyncio.run(scrape_meta_ads())
