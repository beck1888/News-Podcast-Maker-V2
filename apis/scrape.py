from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
from PIL import Image
import pytesseract
from datetime import datetime
import time
import os

def capture_fullpage_screenshot(url, screenshot_path="screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Set a larger viewport width before navigation
        page.set_viewport_size({"width": 1920, "height": 1080})
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            # Wait 1 extra second for everything to load
            time.sleep(1)
            # Get full scrollable height and width
            page_width = page.evaluate("() => document.documentElement.scrollWidth")
            page_height = page.evaluate("() => document.documentElement.scrollHeight")
            page.set_viewport_size({"width": page_width, "height": page_height})
            page.screenshot(path=screenshot_path)
        except TimeoutError:
            browser.close()
            return False
        browser.close()
        return True

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def scrape_page(url: str):
    # Run the full process
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = f"screenshot_{timestamp}.png"
    # print(f"Screenshot saved to {screenshot_file}")
    success = capture_fullpage_screenshot(url, screenshot_file)
    if not success:
        return "This story could not be loaded. Just announce the headline."
    text = extract_text_from_image(screenshot_file)
    try:
        os.remove(screenshot_file)
    except Exception as e:
        print(f"Warning: could not delete screenshot file: {e}")
    return text
