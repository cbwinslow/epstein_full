# GitHub Projects for News Data Acquisition

> **Document:** Open Source Projects for Reuse  
> **Last Updated:** April 4, 2026  
> **Purpose:** Catalog existing tools to avoid reinventing the wheel

---

## GDELT Project Tools

### 1. gdeltPyR (Python Framework) ⭐ HIGHLY RECOMMENDED
**URL:** https://github.com/linwoodc3/gdeltPyR  
**Stars:** 200+  
**Language:** Python  
**License:** MIT

**What it does:**
- Retrieves GDELT 1.0 and 2.0 data programmatically
- Downloads events, mentions, and GKG data
- Handles CSV parsing and DataFrame conversion
- Automatic S3 bucket file discovery

**Reusable for us:**
```python
from gdelt import gdelt

# Get GDELT data for specific dates
g = gdelt.gdelt()
results = g.Search(['2024 01 01'], table='events', coverage=True)
# Filter for Epstein-related events
epstein_events = results[results['Actor1Name'].str.contains('Epstein', case=False, na=False)]
```

---

### 2. gdelt-doc-api (Python Client) ⭐ RECOMMENDED
**URL:** https://github.com/alex9smith/gdelt-doc-api  
**Stars:** 100+  
**Language:** Python  
**License:** MIT

**What it does:**
- Simple Python client for GDELT 2.0 Doc API
- Fetches news article data without managing raw files
- JSON response parsing

**Reusable for us:**
```python
from gdelt_doc_api import GdeltDoc

gdelt = GdeltDoc()

# Search for Epstein articles from 2019-2025
articles = gdelt.article_search(
    query="Epstein",
    start_date="2019-01-01",
    end_date="2025-12-31"
)
```

---

### 3. News-scraper (GDELT-Based) ⭐ RECOMMENDED
**URL:** https://github.com/kenneth-zhou/News-scraper  
**Language:** Python  
**License:** Not specified

**What it does:**
- Downloads daily news articles from GDELT
- Parallelized across all available CPU cores
- High-volume article processing

**Reusable for us:**
- Already parallelized - perfect for our server
- Can modify query to focus on Epstein-related news only
- Saves to structured format

---

### 4. newsfeed (GDELT CLI Tool)
**URL:** https://github.com/Cyclododecene/newsfeed  
**Language:** Python  
**License:** Not specified

**What it does:**
- CLI tool to query GDELT databases
- Download full-text articles
- Time-range based queries

**Usage:**
```bash
python -m newsfeed --db gkg --version 2.0 --start 2019-07-01 --end 2019-08-31 --format json
```

---

### 5. gdeltnews (Web News NGrams Reconstructor)
**URL:** https://github.com/iandreafc/gdeltnews  
**Language:** Python  
**License:** Not specified

**What it does:**
- Reconstructs full-text news articles from GDELT Web News NGrams 3.0
- Downloads decompressed data

**Reusable for us:**
- Can extract article text from GDELT's ngram data
- Alternative to scraping original sources

---

## Wayback Machine / Internet Archive Tools

### 6. wayback-machine-downloader ⭐ ESSENTIAL
**URL:** https://github.com/hartator/wayback-machine-downloader  
**Stars:** 3,000+  
**Language:** Ruby  
**License:** MIT

**What it does:**
- Download entire websites from Wayback Machine
- Supports wildcard patterns
- Filters by date ranges
- Preserves directory structure

**Reusable for us:**
```bash
# Download CNN Epstein articles
wayback_machine_downloader http://cnn.com/*epstein* --from 20190101 --to 20251231
```

---

### 7. waybackpy (Python Wayback Client)
**URL:** https://github.com/akamhy/waybackpy  
**Stars:** 500+  
**Language:** Python  
**License:** MIT

**What it does:**
- Python wrapper for Wayback Machine APIs
- Save pages, get snapshots, CDX API access
- Async support

**Reusable for us:**
```python
from waybackpy import WaybackMachineCDXServerAPI

# Search for all BBC Epstein snapshots
cdx_api = WaybackMachineCDXServerAPI("bbc.com/news/epstein", "epstein_cdx")
snapshots = cdx_api.snapshots()
```

---

## News Article Extraction

### 8. newspaper3k (Article Extraction)
**URL:** https://github.com/codelucas/newspaper  
**Stars:** 13,000+  
**Language:** Python  
**License:** MIT

**What it does:**
- Extract article text, title, authors, publish date
- Multi-language support
- Works on most news sites

**Reusable for us:**
```python
from newspaper import Article

url = "https://wayback.archive.org/web/20190710000000/https://cnn.com/epstein"
article = Article(url)
article.download()
article.parse()
print(article.text)  # Full article text
```

---

### 9. news-please (News Article Extractor)
**URL:** https://github.com/fhamborg/news-please  
**Stars:** 2,500+  
**Language:** Python  
**License:** Apache 2.0

**What it does:**
- Extract news articles from websites
- Supports recursive crawling
- Saves to JSON/CSV/SQL
- Built-in RSS feed support

**Reusable for us:**
```bash
# Crawl specific news site
news-please -c wayback_urls.txt -o /data/news/
```

---

## General Web Scraping

### 10. Scrapy (Web Crawling Framework) ⭐ INDUSTRY STANDARD
**URL:** https://github.com/scrapy/scrapy  
**Stars:** 50,000+  
**Language:** Python  
**License:** BSD 3-Clause

**What it does:**
- Full web crawling framework
- Handles rate limiting, retries, proxies
- Built-in export to JSON/CSV/XML

**Reusable for us:**
- Build custom spiders for news sites
- Integrate with Wayback Machine URLs
- Export directly to PostgreSQL

---

### 11. BeautifulSoup (HTML Parsing)
**URL:** https://github.com/wention/BeautifulSoup4  
**Stars:** -  
**Language:** Python  
**License:** MIT

**Already in our stack - perfect for parsing Wayback HTML**

---

## RSS Feed Tools

### 12. feedparser (RSS/Atom Parser)
**URL:** https://github.com/kurtmckee/feedparser  
**Stars:** -  
**Language:** Python  
**License:** MIT

**What it does:**
- Parse RSS and Atom feeds
- Extract article metadata
- Handle various feed formats

**Reusable for us:**
```python
import feedparser

# Parse historical RSS feeds from Wayback
d = feedparser.parse('https://wayback.archive.org/web/20190710000000/http://rss.cnn.com/rss/cnn_topstories.rss')
for entry in d.entries:
    if 'epstein' in entry.title.lower():
        print(entry.link, entry.title)
```

---

### 13. RSS-Bridge (RSS Feed Generator)
**URL:** https://github.com/RSS-Bridge/rss-bridge  
**Stars:** 3,000+  
**Language:** PHP  
**License:** Unlicense

**What it does:**
- Generate RSS feeds for sites that don't have them
- 300+ site bridges supported

**May not be needed** if we use Wayback archived RSS feeds directly

---

## Search & Discovery

### 14. commoncrawl-py (Common Crawl Python)
**URL:** https://github.com/commoncrawl/cc-pyspark  
**Stars:** 400+  
**Language:** Python  
**License:** Apache 2.0

**What it does:**
- Process Common Crawl WARC files with PySpark
- Extract specific domains/content

**Reusable for us:**
- Parse Common Crawl for news domains
- Filter by Epstein-related keywords

---

### 15. cdx-toolkit (Wayback CDX API)
**URL:** https://github.com/cocrawler/cdx-toolkit  
**Stars:** 100+  
**Language:** Python  
**License:** Apache 2.0

**What it does:**
- Access Wayback Machine CDX API
- Bulk URL discovery
- Index querying

**Reusable for us:**
```python
from cdx_toolkit import CDXFetcher

fetcher = CDXFetcher(source='cc')
for obj in fetcher.iter('cnn.com/epstein', from_ts='2019', to_ts='2025'):
    print(obj['url'], obj['timestamp'])
```

---

## Data Storage & Processing

### 16. newspaper4k (Fork with improvements)
**URL:** https://github.com/Integralist/newspaper4k  
**Stars:** -  
**Language:** Python  
**License:** MIT

**What it does:**
- Fork of newspaper3k with modern improvements
- Better text extraction

**Consider if newspaper3k has issues**

---

## Our Recommended Stack

Based on our needs, here's the **optimal reuse strategy**:

### For GDELT Data:
1. **gdeltPyR** - Bulk data retrieval
2. **gdelt-doc-api** - Specific article queries
3. **news-please** - Article text extraction

### For Wayback Machine:
1. **wayback-machine-downloader** - Bulk website downloads
2. **waybackpy** - Programmatic API access
3. **newspaper3k** - Article text extraction

### For RSS/Feeds:
1. **feedparser** - Parse archived RSS feeds
2. **BeautifulSoup** - Parse HTML (already have)

---

## Projects to Clone/Modify

| Priority | Project | Purpose | Modification Needed |
|----------|---------|---------|---------------------|
| 1 | gdeltPyR | GDELT data retrieval | Add Epstein keyword filters |
| 2 | wayback-machine-downloader | Archive downloads | Add news domain targeting |
| 3 | news-please | Article extraction | Integrate with our DB |
| 4 | waybackpy | Wayback API access | Add batch processing |

---

## Next Steps

1. **Clone gdeltPyR** and test Epstein queries
2. **Clone wayback-machine-downloader** for CNN/NYT test
3. **Install newspaper3k** for text extraction
4. **Create integration scripts** to load into PostgreSQL

---

*Document created as part of Epstein Files Analysis Project - Phase 21: News Data Acquisition*
