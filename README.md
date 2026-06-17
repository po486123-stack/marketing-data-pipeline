# Marketing Data Pipeline: CRM & Traffic Scraping

A Python-based data pipeline that scrapes marketing data from an HTML dump, merges data using Pandas, and calculates key business metrics (ROI).

## Features
- **Safe Web Scraping**: Built with `BeautifulSoup` and includes defensive checks for missing HTML tags to prevent runtime errors.
- **Advanced Data Cleaning**: Uses Regular Expressions (RegEx) via Pandas to strip formatting (currency symbols, spaces) and handle data type casting securely.
- **Zero-Division Protection**: Uses `.where()` method to gracefully handle zero-cost ad campaigns without producing `inf` values.
- **Business Logic**: Calculates automated **ROI** across multiple acquisition channels.

## Tech Stack
- **Python 3.x**
- **BeautifulSoup4** (lxml parser)
- **Pandas**

## How It Works
1. Extracts campaign conversion data (Orders, Revenue) from CRM layout.
2. Extracts traffic costs (Money spent) from marketing cabinet layout.
3. Merges datasets via a `LEFT JOIN` logic on the campaign name.
4. Cleans text into numerical formats and computes ROI metrics.
