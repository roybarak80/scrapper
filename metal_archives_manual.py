#!/usr/bin/env python3
"""
Manual Metal Archives Web Scraper
A Python script that opens Chrome and waits for manual navigation to Metal Archives.
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ManualMetalArchivesScraper:
    def __init__(self, headless=False):
        """
        Initialize the manual scraper with Chrome WebDriver
        
        Args:
            headless (bool): Whether to run Chrome in headless mode (default: False for manual use)
        """
        self.headless = headless
        self.driver = None
        self.setup_logging()
        self.setup_driver()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('manual_scraping.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with basic options"""
        try:
            self.logger.info("Setting up Chrome WebDriver...")
            
            # Basic Chrome options
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Basic options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Initialize WebDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.logger.info("Chrome WebDriver setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome WebDriver: {str(e)}")
            raise
    
    def wait_for_manual_navigation(self):
        """
        Wait for user to manually navigate to Metal Archives
        """
        self.logger.info("🚀 Chrome browser is now open and ready!")
        self.logger.info("📝 Please manually navigate to https://www.metal-archives.com/")
        self.logger.info("⏳ Waiting for metal-archives.com to open...")
        
        print("\n" + "="*60)
        print("🚀 CHROME BROWSER IS READY!")
        print("📝 Please manually navigate to: https://www.metal-archives.com/")
        print("⏳ Waiting for metal-archives.com to open...")
        print("="*60 + "\n")
        
        # Wait for the user to navigate to Metal Archives
        while True:
            try:
                current_url = self.driver.current_url
                
                # Check if we're on Metal Archives
                if "metal-archives.com" in current_url:
                    self.logger.info(f"✅ Successfully detected Metal Archives URL: {current_url}")
                    print(f"✅ Successfully detected Metal Archives URL: {current_url}")
                    return True
                
                # Log current URL every 10 seconds
                self.logger.info(f"Current URL: {current_url}")
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.warning(f"Error checking current URL: {str(e)}")
                time.sleep(5)
    
    def scrape_current_page(self):
        """
        Scrape the current page (assuming it's Metal Archives)
        """
        try:
            self.logger.info("Starting to scrape the current page...")
            
            # Wait for page to be fully loaded
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            self.logger.info("Page loaded successfully")
            
            # Try to find page content
            try:
                # Look for common page elements
                possible_selectors = [
                    "h1", "h2", ".title", ".site-title", ".logo",
                    ".main-content", ".content", ".header",
                    "nav", ".navigation", ".menu"
                ]
                
                found_content = False
                for selector in possible_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            element_text = elements[0].text.strip()
                            if element_text and len(element_text) > 2:
                                self.logger.info(f"Found content with selector '{selector}': '{element_text}'")
                                found_content = True
                                break
                    except Exception:
                        continue
                
                if not found_content:
                    # Fallback to page title
                    page_title = self.driver.title
                    self.logger.info(f"Using page title: '{page_title}'")
                
            except Exception as e:
                self.logger.warning(f"Error finding content: {str(e)}")
            
            # Get page information
            current_url = self.driver.current_url
            page_source_length = len(self.driver.page_source)
            
            self.logger.info(f"Current URL: {current_url}")
            self.logger.info(f"Page source length: {page_source_length} characters")
            
            # Get some basic page content
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text[:200]
                self.logger.info(f"First 200 characters of page content: '{body_text}'")
            except Exception as e:
                self.logger.warning(f"Could not extract page content: {str(e)}")
            
            self.logger.info("✅ Scraping completed successfully!")
            return True
            
        except TimeoutException:
            self.logger.error("Timeout while waiting for page to load")
            return False
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            return False
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.logger.info("Closing WebDriver...")
            self.driver.quit()
            self.logger.info("WebDriver closed")


def main():
    """Main function to run the manual scraper"""
    scraper = None
    try:
        # Initialize scraper (headless=False so you can see the browser)
        scraper = ManualMetalArchivesScraper(headless=False)
        
        # Wait for manual navigation
        if scraper.wait_for_manual_navigation():
            # Scrape the current page
            success = scraper.scrape_current_page()
            
            if success:
                print("✅ Manual scraping completed successfully! Check manual_scraping.log for detailed logs.")
            else:
                print("⚠️ Manual scraping completed with warnings. Check manual_scraping.log for details.")
        else:
            print("❌ Failed to detect Metal Archives navigation")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
