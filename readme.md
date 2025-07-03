Certainly! Here is a professional documentation for your provided Python web scraping code:

---

# Documentation: Google Maps Restaurant Scraper

## Overview

This script automates the process of scraping restaurant data from Google Maps for a specified location (Los Angeles, CA in this case). It uses `undetected_chromedriver` combined with Selenium to bypass bot detection, a proxy for anonymity, and advanced scrolling to load all listings. The collected data includes restaurant names, addresses, websites, phone numbers, review counts, and the latest review date. Results are saved as a CSV file.

---

## Dependencies

* `undetected_chromedriver`
* `selenium`
* `webdriver_manager`
* `pandas`
* `time`
* `random`

Install dependencies via pip if not already installed:

```bash
pip install undetected-chromedriver selenium webdriver-manager pandas
```

---

## Configuration

### Proxy & User-Agent

* Uses ScrapeOps proxy service with a specified API key to route requests.
* Custom user-agent string to mimic a typical Chrome browser session.

### Chrome Options

* Disables GPU to reduce resource usage.
* Sets browser language to English.
* Starts browser maximized.
* Disables Selenium automation detection features.
* Configures proxy and user-agent settings.

---

## Key Components

### 1. Initialization

* Initializes the undetected ChromeDriver with configured options and proxy.
* Navigates to Google Maps search URL for restaurants in Los Angeles.

### 2. Page Scrolling (`scroll_page`)

* Scrolls through the dynamically loaded results feed to load all restaurant entries.
* Uses JavaScript to scroll the container repeatedly until no new content loads (with retries).

### 3. Data Collection

* Collects URLs for all restaurants listed in the feed.

* Iterates over each restaurant URL to scrape detailed information:

  * **Name**
  * **Address**
  * **Website URL**
  * **Phone Number**
  * **Total number of reviews**
  * **Date of the latest review**

* Handles missing elements gracefully by using try-except blocks.

### 4. Review Section Interaction

* Clicks the reviews tab.
* Extracts total review count.
* Sorts reviews by newest.
* Extracts the date of the latest review.

### 5. Data Storage

* Stores collected restaurant data in a list of dictionaries.
* Converts the list to a Pandas DataFrame.
* Saves the DataFrame as `restaurants_data_upgraded.csv`.

### 6. Cleanup

* Closes the browser session after scraping completes.

---

## Usage

1. Update `SCRAPEOPS_PROXY_API_KEY` with your own API key if needed.
2. Run the script.
3. After execution, check the output CSV `restaurants_data_upgraded.csv` for the scraped restaurant data.

---

## Limitations & Notes

* Relies on the current structure of Google Maps; layout changes can break selectors.
* Proxy service and undetected chromedriver help reduce blocking but do not guarantee indefinite access.
* Scraping Google Maps may violate their Terms of Service; use responsibly.
* Sleep intervals and random waits are added to mimic human behavior and reduce detection risk.

---

## Summary

This scraper automates Google Maps restaurant data collection in a robust way, handling scrolling, dynamic content, and review extraction. The result is a structured dataset useful for analysis, business intelligence, or competitive research.

---

If you need further customization or integration guidance, feel free to ask!
