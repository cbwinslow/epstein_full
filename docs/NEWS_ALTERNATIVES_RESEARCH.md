# News Data Alternatives Research

## Executive Summary

After researching multiple alternatives for bulk news data acquisition, we have:

1. **Google News Scraper** (built) - Ready to use, no limits, free
2. **Hugging Face datasets** - Large historical datasets available
3. **Library of Congress** - Bulk OCR data for historical newspapers
4. **NewsData.io** - Better than NewsAPI.org but still limited

---

## 1. Google News Scraper (IMPLEMENTED)

**Status**: ✅ **Ready to use**

**Location**: `media_acquisition/agents/discovery/google_news.py`

**Features**:
- Uses Google News RSS feeds (more reliable than scraping HTML)
- No API key required
- No rate limits (just polite 2s delay between requests)
- Date range filtering supported
- Automatic redirect resolution
- Returns: URL, title, publish date, source domain, description

**Usage**:
```python
from media_acquisition.agents.discovery.google_news import GoogleNewsScraper

scraper = GoogleNewsScraper()
result = scraper.search(
    keywords=['Jeffrey Epstein', 'Ghislaine Maxwell'],
    date_range=('2019-01-01', '2025-12-31'),
    max_results=1000
)
```

**Limitations**:
- Only returns metadata (title, URL, snippet) - must scrape full article separately
- Subject to Google blocking if abused (use delays)

---

## 2. Hugging Face Datasets

### Available Large-Scale News Datasets

| Dataset | Size | Source | Notes |
|---------|------|--------|-------|
| **lil-lab/newsroom** | 1.3M articles | 38 major publications | Summarization dataset |
| **fancyzhx/ag_news** | 1M+ articles | 2,000+ sources | Academic news search engine |
| **rajistics/million-headlines** | 1M+ headlines | 18 years of data | Headlines only |
| **dell-research-harvard/newswire** | Large | Historical news | High-quality corpus |
| **alexfabbri/multi_news** | Medium | newser.com | Articles + summaries |
| **julien040/hacker-news-posts** | 4M stories | Hacker News | Tech-focused |

**Access**: `datasets` library or direct download from huggingface.co

**Example**:
```python
from datasets import load_dataset

# Load AG News dataset (1M articles)
dataset = load_dataset("fancyzhx/ag_news")
```

**Relevance for Epstein Research**: 
- AG News has general news but not specifically Epstein-related
- Newsroom dataset might have relevant articles from major publications
- Need to filter by date (2019-2025) and keywords

---

## 3. Library of Congress - Chronicling America

**Status**: ✅ **Available for bulk download**

**Website**: https://chroniclingamerica.loc.gov/

### Features
- **20+ million** digitized newspaper pages
- OCR text available for all pages
- Coverage: 1789-1963 (mostly pre-1963, but some later)
- **FREE** - No API key required
- Bulk data downloads available

### Access Methods

1. **API**: `https://chroniclingamerica.loc.gov/about/api/`
   - REST API for searching
   - JSON responses
   - Rate limits apply

2. **Bulk Download**: `https://chroniclingamerica.loc.gov/data/batches/`
   - Direct access to OCR text files
   - Organized by batch/state
   - Can download entire collections

3. **OCR Data**: `https://chroniclingamerica.loc.gov/ocr/`
   - Text extracted from all pages
   - Structured data format

### Relevance for Epstein Research
- **LIMITED** - Coverage mostly ends around 1963
- Epstein case (2019-present) would not be covered
- Useful for historical context on similar cases

---

## 4. NewsData.io API

**Status**: ⚠️ **Better than NewsAPI.org but still limited**

**Website**: https://newsdata.io/

### Free Tier
- **200 API credits/day** (vs NewsAPI.org's 100)
- 10 articles per credit = 2,000 articles/day max
- Still insufficient for 10,000 article goal

### Paid Tiers
- 20,000+ credits/day on paid plans
- Historical news access
- Better pricing than NewsAPI.org

### Comparison
| Feature | NewsData.io | NewsAPI.org |
|---------|-------------|-------------|
| Free daily requests | 200 | 100 |
| Free tier production use | ❌ No | ❌ No |
| Full article content | ❌ No | ❌ No |
| Paid plan cost | Lower | $449+/mo |

**Verdict**: Better than NewsAPI.org but still not viable for bulk collection without paying.

---

## 5. Other APIs Researched

### GNews.io
- Similar limitations to NewsAPI.org
- Free tier: 100 requests/day
- Full content requires paid plans

### WorldNewsAPI.com
- Free tier available
- Rate limited
- Commercial use requires paid plans

### Perigon API
- No free tier
- Enterprise-focused
- More expensive

---

## 6. Direct Web Scraping Options

### Reddit r/Epstein
- Active community with article links
- Could scrape posts for article URLs
- Free, but requires Reddit API (free tier available)

### Twitter/X Search
- Historical tweets with article links
- Requires Twitter API (expensive now)

### Archive.org Wayback Machine
- Already implemented in our system
- Very slow, times out on large queries
- Good for historical snapshots

---

## Recommended Strategy

### Primary: Google News Scraper (IMPLEMENTED)
- Use for current discovery
- No limits, no cost
- Combine with our article downloader for full content

### Secondary: Hugging Face Datasets
- Download AG News dataset (1M articles)
- Filter for Epstein-related keywords
- Use for training/analysis

### Tertiary: Manual URL Import
- Import known Epstein article lists
- Cross-reference with our system
- Community-curated lists available?

---

## Implementation Status

| Source | Status | Location |
|--------|--------|----------|
| Google News | ✅ Ready | `media_acquisition/agents/discovery/google_news.py` |
| GDELT | ✅ Implemented | `media_acquisition/agents/discovery/news.py` |
| Wayback Machine | ✅ Implemented | `media_acquisition/agents/discovery/news.py` |
| RSS Feeds | ✅ Implemented | `media_acquisition/agents/discovery/news.py` |
| Hugging Face | ⏭️ Can integrate | Use `datasets` library |
| Library of Congress | ⏭️ Historical only | Not relevant for 2019+ |

---

## Next Steps

1. **Test Google News scraper** - Run a quick test to verify it works
2. **Integrate into ingestion pipeline** - Add as primary discovery source
3. **Consider Hugging Face** - Download AG News for additional coverage
4. **Disable problematic sources** - Temporarily disable Wayback (too slow)
5. **Monitor results** - Track article discovery rates

---

## API Key Summary

| Service | Key | Status | Limits |
|---------|-----|--------|--------|
| NewsAPI.org | `367abe65b21647b69c54bfb8da20f27d` | ❌ Not viable | 100/day |
| NewsData.io | N/A | ⏭️ Could sign up | 200/day |
| Google News | Not needed | ✅ Using | No limits |
| Hugging Face | Not needed | ✅ Public datasets | No limits |
| Library of Congress | Not needed | ✅ Public | No limits |

---

*Research completed: April 8, 2026*
