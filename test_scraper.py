import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            print("Checking USArmy...")
            await page.goto("https://x.com/USArmy", timeout=30000)
            await page.wait_for_selector("article", timeout=15000)
            await page.wait_for_timeout(3000)
            
            articles = await page.query_selector_all("article")
            print(f"Found {len(articles)} articles")
            for i, article in enumerate(articles):
                html = await article.inner_html()
                has_video = "<video" in html or "playback" in html
                print(f"Article {i}: has_video={has_video}")
                
                links = await article.query_selector_all("a[href*='/status/']")
                for link in links:
                    href = await link.get_attribute("href")
                    if href and "/status/" in href and "photo" not in href:
                        print(f"  Link: {href}")
                        break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

asyncio.run(run())
