from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import re
from datetime import datetime

def get_product_info():
    """Load product URL and target price from product.json"""
    with open("product.json", "r") as file:
        data = json.load(file)
    return data['product'], float(data['price'])

def get_price(url):
    """Get current price from Amazon product page"""
    # Setup Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening browser window
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the product page
        driver.get(url)
        time.sleep(3)
        
        # Find price element (Amazon uses different classes)
        price_selectors = [
            "span.a-price-whole",
            "span.a-price",
            ".a-price .a-offscreen"
        ]
        
        current_price = None
        for selector in price_selectors:
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, selector)
                price_text = price_element.text
                # Extract number from price text
                price_numbers = re.findall(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_numbers:
                    current_price = float(price_numbers[0])
                    break
            except:
                continue
        
        return current_price
    
    finally:
        driver.quit()

def save_result(url, current_price, target_price, alert):
    """Save results to CSV and display on console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to CSV
    with open("price_log.csv", "a") as file:
        file.write(f"{timestamp},{current_price},{target_price},{alert}\n")
    
    # Display results
    print(f"{timestamp}")
    print(f"Current Price: ${current_price}")
    print(f"Target Price: ${target_price}")
    
    if alert:
        print("PRICE ALERT! Target price reached!")
        print(f"You can save: ${target_price - current_price}")
    else:
        print(f"Still ${current_price - target_price:.2f} above target")
    
    print("-" * 40)

def main():
    """Main price tracking function"""
    print("Amazon Price Tracker")
    print("=" * 25)
    
    # Get product info
    product_url, target_price = get_product_info()
    print(f"Tracking: {product_url}")
    
    # Get current price
    current_price = get_price(product_url)
    
    if current_price:
        # Check if price alert should trigger
        price_alert = current_price <= target_price
        
        # Save and display results
        save_result(product_url, current_price, target_price, price_alert)
    else:
        print(" Could not get price. Check the product URL.")

if __name__ == "__main__":
    main()

