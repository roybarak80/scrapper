# Metal Archives Web Scraper

A Python web scraper for https://www.metal-archives.com/ using Selenium with headless Chrome.

## Features

- **Two scraper versions**: Basic and Enhanced with Cloudflare bypass techniques
- Headless Chrome browser automation with stealth options
- Comprehensive logging and error handling
- Human behavior simulation to avoid detection
- Easy to extend for more complex scraping tasks

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have Chrome browser installed on your system.

## Usage

### Basic Scraper
Run the basic scraper:
```bash
python metal_archives_scraper.py
```

### Enhanced Scraper (Recommended)
Run the enhanced scraper with Cloudflare bypass:
```bash
python metal_archives_enhanced.py
```

Both scripts will:
- Launch a headless Chrome browser
- Navigate to Metal Archives
- Attempt to bypass Cloudflare protection (enhanced version)
- Scrape page information and log all activities

## Files

- `metal_archives_scraper.py` - Basic scraper script
- `metal_archives_enhanced.py` - Enhanced scraper with Cloudflare bypass
- `requirements.txt` - Python dependencies
- `scraping.log` - Basic scraper log file
- `enhanced_scraping.log` - Enhanced scraper log file

## Important Notes

### Cloudflare Protection
Metal Archives uses Cloudflare protection which can block automated scrapers. The enhanced version includes:
- Stealth browser options
- Human behavior simulation
- Cloudflare detection and waiting
- Multiple user agent rotation

### Usage Recommendations
1. **Start with the enhanced version** for better success rates
2. **Set `headless=False`** in the main function to see the browser and debug issues
3. **Add delays** between requests to be respectful to the server
4. **Check the logs** for detailed information about the scraping process

### Legal and Ethical Considerations
- Always respect the website's robots.txt file
- Add delays between requests to avoid overwhelming the server
- Consider contacting the website owner for permission to scrape
- Be aware of the website's terms of service

## Customization

You can modify the scrapers by:
- Changing `headless=False` to see the browser in action
- Adding more scraping methods to extract specific data
- Customizing Chrome options for different behaviors
- Adding more sophisticated Cloudflare bypass techniques
- Implementing data storage (CSV, JSON, database)

## Troubleshooting

If you encounter issues:
1. Check the log files for detailed error messages
2. Try running with `headless=False` to see what's happening
3. Ensure Chrome browser is installed and up to date
4. Check your internet connection and firewall settings
