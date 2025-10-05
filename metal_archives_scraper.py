#!/usr/bin/env python3
"""
Metal Archives Web Scraper
A Python script to scrape data from https://www.metal-archives.com/
using Selenium with headless Chrome browser.
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


class MetalArchivesScraper:
    def __init__(self, headless=True):
        """
        Initialize the scraper with Chrome WebDriver
        
        Args:
            headless (bool): Whether to run Chrome in headless mode
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
                logging.FileHandler('scraping.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        try:
            self.logger.info("Setting up Chrome WebDriver...")
            
            # Chrome options
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Additional options for better performance and stealth
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Initialize WebDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.logger.info("Chrome WebDriver setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome WebDriver: {str(e)}")
            raise
    
    def scrape_site_title(self):
        """
        Scrape a simple element from Metal Archives - the site title
        This is a basic test to verify the scraper is working
        """
        try:
            self.logger.info("Starting to scrape Metal Archives...")
            self.logger.info("Navigating to https://www.metal-archives.com/")
            
            # Navigate to the site
            self.driver.get("https://www.metal-archives.com/")
            
            # Wait for the page to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            self.logger.info("Page loaded successfully")
            
            # Try to find the site title
            try:
                # Look for the main title or logo
                title_element = self.driver.find_element(By.CSS_SELECTOR, "h1, .title, .logo, .site-title")
                title_text = title_element.text.strip()
                self.logger.info(f"Found site title: '{title_text}'")
                
            except NoSuchElementException:
                # If no specific title found, get the page title
                page_title = self.driver.title
                self.logger.info(f"Page title: '{page_title}'")
                
                # Try to find any heading element
                headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
                if headings:
                    first_heading = headings[0].text.strip()
                    self.logger.info(f"First heading found: '{first_heading}'")
            
            # Get some basic page information
            current_url = self.driver.current_url
            page_source_length = len(self.driver.page_source)
            
            self.logger.info(f"Current URL: {current_url}")
            self.logger.info(f"Page source length: {page_source_length} characters")
            
            # Look for any text content on the page
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text[:200]
                self.logger.info(f"First 200 characters of page content: '{body_text}'")
            except Exception as e:
                self.logger.warning(f"Could not extract page content: {str(e)}")
            
            self.logger.info("Scraping completed successfully!")
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
    """Main function to run the scraper"""
    scraper = None
    try:
        # Initialize scraper in headless mode
        scraper = MetalArchivesScraper(headless=True)
        
        # Run the scraping task
        success = scraper.scrape_site_title()
        
        if success:
            print("Scraping completed successfully! Check scraping.log for detailed logs.")
        else:
            print("Scraping failed. Check scraping.log for error details.")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
