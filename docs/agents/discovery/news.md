# News Discovery Agent

## Overview

The `NewsDiscoveryAgent` discovers Epstein-related news articles from multiple sources including GDELT Project, Wayback Machine, and RSS feeds.

## Location

`media_acquisition/agents/discovery/news.py`

## Keywords

The agent uses 50+ comprehensive keywords for exhaustive search:

### Primary Names
- Jeffrey Epstein, Epstein, Ghislaine Maxwell, Virginia Giuffre
- Virginia Roberts, Sarah Ransome, Maria Farmer, Annie Farmer

### Case References
- Epstein case, Epstein investigation, Epstein trial
- Epstein indictment, Epstein plea deal, Acosta Epstein
- SDNY Epstein, Southern District Epstein

### Locations
- Little Saint James, Epstein Island, Great St James
- Palm Beach Epstein, Manhattan Epstein, Zorro Ranch
- New Mexico Epstein, US Virgin Islands Epstein

### Organizations
- Mossack Fonseca Epstein, Epstein VI, Southern Trust
- Gratitude America, J Epstein & Co, Epstein Foundation
- Epstein Associates

### Legal Terms
- sex trafficking Epstein, sex offender Epstein
- non-prosecution agreement Epstein, Epstein plea
- civil lawsuit Epstein, Epstein criminal case

### Associated Figures
- Trump Epstein, Clinton Epstein, Prince Andrew Epstein
- Alan Dershowitz Epstein, Bill Gates Epstein
- Leslie Wexner Epstein, Leon Black Epstein
- Alexander Acosta, Cy Vance, Barry Krischer

### Related Topics
- Lolita Express, Epstein flight logs, Epstein black book
- Epstein client list, Epstein associates
- Epstein network, Epstein conspiracy

### Document Types
- Epstein court documents, Epstein court filings
- Epstein deposition, Epstein lawsuit

### Case Numbers
- 1:08-cr-00808, 1:15-cv-07433, Epstein docket

### Aftermath
- Epstein death, Epstein autopsy, Epstein jail death
- Epstein documentary, Epstein investigation aftermath

### Financial
- Epstein finances, Epstein money laundering
- Epstein tax evasion, Epstein offshore accounts

### International
- Epstein France, Epstein UK, Epstein Caribbean

## RSS Feeds

The agent monitors 43 RSS feeds across multiple categories:

### Mainstream US (19 feeds)
- CNN: top stories, world, US
- NYT: home, world, US, NY region
- Washington Post: national, world, politics
- BBC: general, world, US/Canada
- Guardian: US, world, US news
- Reuters: business-finance, world, domestic
- AP: hub, top news, US news

### Business (5 feeds)
- WSJ, Bloomberg, Forbes, Financial Times, CNBC

### Investigative (4 feeds)
- ProPublica, BuzzFeed News, Miami Herald, Miami New Times

### Legal (3 feeds)
- Law360, Above the Law, SCOTUSblog

### Tabloids (3 feeds)
- NY Post, Daily Mail, The Sun

### International (5 feeds)
- Le Monde (France), Der Spiegel (Germany), El País (Spain)
- Sydney Morning Herald (Australia), Globe and Mail (Canada)

### Tech (3 feeds)
- TechCrunch, The Verge, Wired

### Politics (3 feeds)
- Politico, The Hill, Roll Call

### Opinion/Analysis (3 feeds)
- The Atlantic, Vox, Slate

### Local (2 feeds)
- Palm Beach Post, Santa Fe New Mexican

## Discovery Methods

### 1. GDELT Project
- **Purpose**: Bulk historical data (100M+ articles)
- **API**: GDELT Doc API
- **Rate Limit**: 250 records per query
- **Coverage**: Global news monitoring
- **Status**: Available but rate-limited (429 errors)

### 2. Wayback Machine
- **Purpose**: Historical snapshots of articles
- **API**: CDX API
- **Coverage**: Archived versions of 30+ domains
- **Rate Limit**: 1 second delay between requests
- **Status**: Available but returns limited results

### 3. RSS Feeds
- **Purpose**: Real-time and recent articles
- **Coverage**: 43 feeds from major outlets
- **Rate Limit**: None (but polite delays recommended)
- **Status**: Currently primary discovery method

## Usage

### Command Line

```bash
python3 scripts/run_news_ingestion.py \
    --keywords "Jeffrey Epstein" "Epstein" \
    --start-date 2019-01-01 \
    --end-date 2025-12-31 \
    --max-results 10000 \
    --batch-size 20
```

### Python API

```python
from media_acquisition.agents.discovery.news import NewsDiscoveryAgent
from media_acquisition.base import AgentConfig

config = AgentConfig(
    agent_id='news-discovery',
    database_url='postgresql://user:pass@localhost:5432/epstein',
    storage_path='/path/to/storage'
)

agent = NewsDiscoveryAgent(config)
results = await agent.search(
    keywords=['Jeffrey Epstein', 'Epstein'],
    date_range=('2019-01-01', '2025-12-31'),
    max_results=10000
)
```

## Output

The agent returns a list of `NewsArticleURL` objects containing:
- `url`: Article URL
- `title`: Article title
- `source_domain`: Domain name
- `publish_date`: Publication date
- `discovery_method`: 'gdelt', 'wayback', or 'rss'
- `priority`: 1 (high) to 10 (low)
- `keywords_matched`: List of matched keywords
- `metadata`: Additional discovery context

## Performance

- **Discovery Speed**: ~100-500 articles per minute (RSS)
- **Memory Usage**: ~100MB for 10,000 results
- **Rate Limiting**: Built-in delays to prevent blocking

## Troubleshooting

### GDELT 429 Errors
- **Cause**: Rate limit exceeded
- **Solution**: Add longer delays between queries
- **Workaround**: Skip GDELT and use RSS feeds

### Wayback Machine Returns 0 Results
- **Cause**: URL patterns don't match archived content
- **Solution**: Try different URL patterns or domains
- **Workaround**: Use RSS feeds for recent content

### RSS Feed Parsing Errors
- **Cause**: Invalid RSS XML or network issues
- **Solution**: Add try-catch with logging
- **Workaround**: Skip problematic feeds

## Future Enhancements

- [ ] Add NewsAPI.org integration (150K+ sources)
- [ ] Add Common Crawl integration (billions of pages)
- [ ] Add social media monitoring (Twitter/X, Reddit)
- [ ] Add court docket monitoring (CourtListener, PACER)
- [ ] Add press release monitoring
- [ ] Implement real-time monitoring with webhooks
