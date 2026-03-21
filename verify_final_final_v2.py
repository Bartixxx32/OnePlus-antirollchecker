import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        path = os.path.abspath('page/index.html')
        await page.goto(f'file://{path}')
        await page.wait_for_selector('.card')
        nord_card = await page.query_selector("text='OnePlus Nord CE 3 Lite'")
        if nord_card:
            await nord_card.scroll_into_view_if_needed()
            await page.screenshot(path='final_view_v2.png')
            print("Screenshot saved to final_view_v2.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
