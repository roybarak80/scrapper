#!/usr/bin/env python3
"""
Enhanced Metal Archives Web Scraper
A Python script to scrape data from https://www.metal-archives.com/
using Selenium with enhanced Cloudflare bypass techniques.
"""

import logging
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class EnhancedMetalArchivesScraper:
    def __init__(self, headless=True):
        """
        Initialize the enhanced scraper with Chrome WebDriver
        
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
                logging.FileHandler('enhanced_scraping.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with enhanced stealth options"""
        try:
            self.logger.info("Setting up enhanced Chrome WebDriver...")
            
            # Enhanced Chrome options for bypassing detection
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Stealth options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            
            # Enhanced user agent and headers
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Disable automation indicators
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize WebDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute stealth script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Enhanced Chrome WebDriver setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome WebDriver: {str(e)}")
            raise
    
    def wait_for_cloudflare(self, timeout=30):
        """
        Wait for Cloudflare protection to pass
        
        Args:
            timeout (int): Maximum time to wait in seconds
        """
        self.logger.info("Checking for Cloudflare protection...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check if we're still on a Cloudflare page
                page_source = self.driver.page_source.lower()
                if "cloudflare" in page_source or "checking your browser" in page_source:
                    self.logger.info("Cloudflare protection detected, waiting...")
                    time.sleep(2)
                    continue
                elif "verifying you are human" in page_source:
                    self.logger.info("Human verification detected, waiting...")
                    time.sleep(2)
                    continue
                else:
                    self.logger.info("Cloudflare protection passed!")
                    return True
            except Exception as e:
                self.logger.warning(f"Error checking Cloudflare status: {str(e)}")
                time.sleep(1)
        
        self.logger.warning("Cloudflare protection timeout reached")
        return False
    
    def simulate_human_behavior(self):
        """Simulate human-like behavior to avoid detection"""
        try:
            # Random mouse movements
            actions = ActionChains(self.driver)
            for _ in range(random.randint(2, 5)):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset)
                actions.perform()
                time.sleep(random.uniform(0.5, 1.5))
            
            # Random scrolling
            scroll_amount = random.randint(100, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1, 2))
            
            # Scroll back
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            time.sleep(random.uniform(0.5, 1))
            
            self.logger.info("Simulated human behavior completed")
            
        except Exception as e:
            self.logger.warning(f"Error simulating human behavior: {str(e)}")
    
    def scrape_metal_archives(self):
        """
        Enhanced scraping of Metal Archives with Cloudflare bypass
        """
        try:
            self.logger.info("Starting enhanced scraping of Metal Archives...")
            self.logger.info("Navigating to https://www.metal-archives.com/")
            
            # Navigate to the site
            self.driver.get("https://www.metal-archives.com/")
            
            # Wait for initial page load
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            self.logger.info("Initial page loaded")
            
            # Wait for Cloudflare protection to pass
            if not self.wait_for_cloudflare(timeout=30):
                self.logger.warning("Cloudflare protection may still be active")
            
            # Simulate human behavior
            self.simulate_human_behavior()
            
            # Try to find actual site content
            try:
                # Look for common Metal Archives elements
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
            
            self.logger.info(f"Final URL: {current_url}")
            self.logger.info(f"Page source length: {page_source_length} characters")
            
            # Check if we successfully bypassed protection
            page_source_lower = self.driver.page_source.lower()
            if "cloudflare" not in page_source_lower and "checking your browser" not in page_source_lower:
                self.logger.info("✅ Successfully bypassed Cloudflare protection!")
                return True
            else:
                self.logger.warning("⚠️ Cloudflare protection may still be active")
                return False
            
        except TimeoutException:
            self.logger.error("Timeout while waiting for page to load")
            return False
        except Exception as e:
            self.logger.error(f"Error during enhanced scraping: {str(e)}")
            return False
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.logger.info("Closing WebDriver...")
            self.driver.quit()
            self.logger.info("WebDriver closed")


def main():
    """Main function to run the enhanced scraper"""
    scraper = None
    try:
        # Initialize scraper (set headless=False to see the browser)
        scraper = EnhancedMetalArchivesScraper(headless=True)
        
        # Run the enhanced scraping task
        success = scraper.scrape_metal_archives()
        
        if success:
            print("✅ Enhanced scraping completed successfully! Check enhanced_scraping.log for detailed logs.")
        else:
            print("⚠️ Enhanced scraping completed with warnings. Check enhanced_scraping.log for details.")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
