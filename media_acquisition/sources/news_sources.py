#!/usr/bin/env python3
"""
Comprehensive news source registry for Epstein research.
100+ sources covering major outlets, regional news, and specialized publishers.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class NewsSource:
    """News source configuration."""
    name: str
    domain: str
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key_required: bool = False
    requires_proxy: bool = False
    rate_limit_seconds: float = 1.0
    priority: int = 5  # 1-10, lower = higher priority
    active: bool = True
    search_url_template: Optional[str] = None  # For site-specific search
    date_range_supported: bool = True
    reliability_score: float = 0.8  # 0-1


# Tier 1: Major International Outlets (High Priority)
TIER_1_SOURCES = [
    NewsSource("New York Times", "nytimes.com",
               rss_url="https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
               rate_limit_seconds=2.0, priority=1, reliability_score=0.95),
    NewsSource("Washington Post", "washingtonpost.com",
               rss_url="https://feeds.washingtonpost.com/rss/national",
               rate_limit_seconds=2.0, priority=1, reliability_score=0.95),
    NewsSource("The Guardian", "theguardian.com",
               rss_url="https://www.theguardian.com/us/rss",
               rate_limit_seconds=1.5, priority=1, reliability_score=0.95),
    NewsSource("BBC News", "bbc.com",
               rss_url="http://feeds.bbci.co.uk/news/rss.xml",
               rate_limit_seconds=1.5, priority=1, reliability_score=0.95),
    NewsSource("Reuters", "reuters.com",
               rss_url="https://www.reutersagency.com/feed/?best-topics=rss",
               rate_limit_seconds=1.0, priority=1, reliability_score=0.95),
    NewsSource("Associated Press", "apnews.com",
               rss_url="https://apnews.com/hub/rss",
               rate_limit_seconds=1.0, priority=1, reliability_score=0.95),
    NewsSource("CNN", "cnn.com",
               rss_url="http://rss.cnn.com/rss/edition.rss",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),
    NewsSource("NBC News", "nbcnews.com",
               rss_url="https://feeds.nbcnews.com/nbcnews/public/news",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),
    NewsSource("ABC News", "abcnews.go.com",
               rss_url="https://abcnews.go.com/abcnews/usheadlines",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),
    NewsSource("CBS News", "cbsnews.com",
               rss_url="https://www.cbsnews.com/latest/rss/main",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),
    NewsSource("Fox News", "foxnews.com",
               rss_url="http://feeds.foxnews.com/foxnews/latest",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.75),
    NewsSource("Wall Street Journal", "wsj.com",
               rss_url="https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
               rate_limit_seconds=2.0, priority=1, reliability_score=0.95),
    NewsSource("Financial Times", "ft.com",
               rate_limit_seconds=2.0, priority=2, reliability_score=0.9),
    NewsSource("Bloomberg", "bloomberg.com",
               rate_limit_seconds=2.0, priority=2, reliability_score=0.9),
    NewsSource("Economist", "economist.com",
               rss_url="https://www.economist.com/latest/rss.xml",
               rate_limit_seconds=2.0, priority=2, reliability_score=0.95),
]

# Tier 2: Major Regional & Metropolitan (High Volume)
TIER_2_SOURCES = [
    NewsSource("LA Times", "latimes.com",
               rss_url="https://www.latimes.com/world-nation/rss2.0.xml",
               rate_limit_seconds=1.5, priority=3, reliability_score=0.9),
    NewsSource("Chicago Tribune", "chicagotribune.com",
               rate_limit_seconds=1.5, priority=3, reliability_score=0.9),
    NewsSource("Miami Herald", "miamiherald.com",
               rate_limit_seconds=1.5, priority=3, reliability_score=0.85),
    NewsSource("Palm Beach Post", "palmbeachpost.com",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),  # Critical for Epstein
    NewsSource("Palm Beach Daily News", "palmbeachdailynews.com",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),
    NewsSource("New York Post", "nypost.com",
               rss_url="https://nypost.com/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.7),
    NewsSource("Daily Mail", "dailymail.co.uk",
               rss_url="https://www.dailymail.co.uk/ushome/index.rss",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.6),
    NewsSource("Daily Beast", "thedailybeast.com",
               rss_url="https://feeds.thedailybeast.com/rss/articles",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.75),
    NewsSource("HuffPost", "huffpost.com",
               rss_url="https://www.huffpost.com/section/front-page/feed",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.75),
    NewsSource("Politico", "politico.com",
               rss_url="https://www.politico.com/rss/politics08.xml",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.9),
    NewsSource("Axios", "axios.com",
               rss_url="https://api.axios.com/feed/politics",
               rate_limit_seconds=1.0, priority=2, reliability_score=0.85),
    NewsSource("Vox", "vox.com",
               rss_url="https://www.vox.com/rss/index.xml",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
    NewsSource("Slate", "slate.com",
               rss_url="https://feeds.slate.com/slate",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
    NewsSource("Salon", "salon.com",
               rss_url="https://www.salon.com/feed/",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.75),
    NewsSource("Intercept", "theintercept.com",
               rss_url="https://theintercept.com/feed/",
               rate_limit_seconds=1.0, priority=2, reliability_score=0.85),
    NewsSource("ProPublica", "propublica.org",
               rss_url="https://feeds.propublica.org/propublica/main",
               rate_limit_seconds=1.5, priority=1, reliability_score=0.95),
    NewsSource("Mother Jones", "motherjones.com",
               rss_url="https://www.motherjones.com/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
    NewsSource("The Atlantic", "theatlantic.com",
               rss_url="https://www.theatlantic.com/feed/all/",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.9),
    NewsSource("New Yorker", "newyorker.com",
               rss_url="https://www.newyorker.com/feed/news",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.95),
    NewsSource("Vanity Fair", "vanityfair.com",
               rss_url="https://www.vanityfair.com/feed/rss",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
]

# Tier 3: Investigative & Legal News (Critical for Epstein)
TIER_3_SOURCES = [
    NewsSource("Law & Crime", "lawandcrime.com",
               rss_url="https://lawandcrime.com/feed/",
               rate_limit_seconds=1.0, priority=1, reliability_score=0.85),
    NewsSource("Courthouse News", "courthousenews.com",
               rss_url="https://www.courthousenews.com/feed/",
               rate_limit_seconds=1.0, priority=1, reliability_score=0.9),
    NewsSource("CourtListener", "courtlistener.com",
               rate_limit_seconds=2.0, priority=1, reliability_score=0.95),
    NewsSource("Above the Law", "abovethelaw.com",
               rss_url="https://abovethelaw.com/feed/",
               rate_limit_seconds=1.0, priority=2, reliability_score=0.8),
    NewsSource("Legal Times", "legaltimes.com",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.85),
    NewsSource("Law360", "law360.com",
               rate_limit_seconds=2.0, priority=1, reliability_score=0.9),
    NewsSource("National Law Journal", "law.com",
               rate_limit_seconds=2.0, priority=2, reliability_score=0.9),
    NewsSource("Legal Insurrection", "legalinsurrection.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.7),
    NewsSource("SCOTUSblog", "scotusblog.com",
               rss_url="https://www.scotusblog.com/feed/",
               rate_limit_seconds=1.0, priority=2, reliability_score=0.95),
    NewsSource("Reason", "reason.com",
               rss_url="https://reason.com/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
]

# Tier 4: International Sources
TIER_4_SOURCES = [
    NewsSource("Times of London", "thetimes.co.uk",
               rate_limit_seconds=2.0, priority=3, reliability_score=0.9),
    NewsSource("Telegraph", "telegraph.co.uk",
               rate_limit_seconds=1.5, priority=3, reliability_score=0.85),
    NewsSource("Le Monde", "lemonde.fr",
               rate_limit_seconds=2.0, priority=3, reliability_score=0.9),
    NewsSource("Der Spiegel", "spiegel.de",
               rate_limit_seconds=2.0, priority=3, reliability_score=0.9),
    NewsSource("Sydney Morning Herald", "smh.com.au",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.85),
    NewsSource("Globe and Mail", "theglobeandmail.com",
               rate_limit_seconds=2.0, priority=4, reliability_score=0.9),
    NewsSource("Haaretz", "haaretz.com",
               rate_limit_seconds=2.0, priority=4, reliability_score=0.85),
    NewsSource("Jerusalem Post", "jpost.com",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.8),
    NewsSource("Al Jazeera", "aljazeera.com",
               rss_url="https://www.aljazeera.com/xml/rss/all.xml",
               rate_limit_seconds=1.5, priority=3, reliability_score=0.85),
    NewsSource("France 24", "france24.com",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.85),
    NewsSource("Deutsche Welle", "dw.com",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.85),
    NewsSource("BBC US & Canada", "bbc.com",
               rss_url="http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
               rate_limit_seconds=1.5, priority=2, reliability_score=0.95),
    NewsSource("Canada CBC", "cbc.ca",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.85),
    NewsSource("Australian ABC", "abc.net.au",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.85),
]

# Tier 5: Business & Financial News (Epstein financial connections)
TIER_5_SOURCES = [
    NewsSource("Forbes", "forbes.com",
               rss_url="https://www.forbes.com/news/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.85),
    NewsSource("Fortune", "fortune.com",
               rss_url="https://fortune.com/feed/",
               rate_limit_seconds=1.5, priority=3, reliability_score=0.85),
    NewsSource("Business Insider", "businessinsider.com",
               rss_url="https://www.businessinsider.com/rss",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
    NewsSource("CNBC", "cnbc.com",
               rss_url="https://www.cnbc.com/id/100003114/device/rss/rss.html",
               rate_limit_seconds=1.0, priority=2, reliability_score=0.85),
    NewsSource("MarketWatch", "marketwatch.com",
               rss_url="http://feeds.marketwatch.com/marketwatch/topstories/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.85),
    NewsSource("Barron's", "barrons.com",
               rate_limit_seconds=2.0, priority=3, reliability_score=0.9),
    NewsSource("Investment News", "investmentnews.com",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.8),
    NewsSource("Institutional Investor", "institutionalinvestor.com",
               rate_limit_seconds=2.0, priority=4, reliability_score=0.85),
    NewsSource("Private Equity International", "peimedia.com",
               rate_limit_seconds=2.0, priority=4, reliability_score=0.8),
    NewsSource("Hedge Fund Alert", "hfalert.com",
               rate_limit_seconds=2.0, priority=4, reliability_score=0.8),
    NewsSource("DealBook NYT", "nytimes.com",
               rss_url="https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
               rate_limit_seconds=2.0, priority=2, reliability_score=0.95),
    NewsSource("Financial Post", "financialpost.com",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.85),
]

# Tier 6: Alternative & Independent Media
TIER_6_SOURCES = [
    NewsSource("Democracy Now", "democracynow.org",
               rss_url="https://www.democracynow.org/rss",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
    NewsSource("Common Dreams", "commondreams.org",
               rss_url="https://www.commondreams.org/rss",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.75),
    NewsSource("Truthout", "truthout.org",
               rss_url="https://truthout.org/feed/",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.75),
    NewsSource("Truthdig", "truthdig.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.75),
    NewsSource("MintPress News", "mintpressnews.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.7),
    NewsSource("Grayzone", "thegrayzone.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.7),
    NewsSource("Consortium News", "consortiumnews.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.75),
    NewsSource("Shadowproof", "shadowproof.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.7),
    NewsSource("The Nation", "thenation.com",
               rss_url="https://www.thenation.com/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.85),
    NewsSource("Jacobin", "jacobinmag.com",
               rss_url="https://jacobin.com/feed",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.8),
    NewsSource("Current Affairs", "currentaffairs.org",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.8),
]

# Tier 7: Right-leaning & Conservative Media
TIER_7_SOURCES = [
    NewsSource("National Review", "nationalreview.com",
               rss_url="https://www.nationalreview.com/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.8),
    NewsSource("Washington Examiner", "washingtonexaminer.com",
               rss_url="https://www.washingtonexaminer.com/feed/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.75),
    NewsSource("Washington Times", "washingtontimes.com",
               rss_url="https://www.washingtontimes.com/rss/headlines/news/",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.75),
    NewsSource("Daily Caller", "dailycaller.com",
               rss_url="https://dailycaller.com/feed/",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.65),
    NewsSource("Daily Wire", "dailywire.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.7),
    NewsSource("Newsmax", "newsmax.com",
               rate_limit_seconds=1.0, priority=3, reliability_score=0.7),
    NewsSource("American Thinker", "americanthinker.com",
               rate_limit_seconds=1.0, priority=5, reliability_score=0.6),
    NewsSource("Federalist", "thefederalist.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.75),
    NewsSource("Spectator", "spectator.org",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.8),
    NewsSource("New York Sun", "nysun.com",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.8),
    NewsSource("Epoch Times", "theepochtimes.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.6),
    NewsSource("Breitbart", "breitbart.com",
               rss_url="http://feeds.feedburner.com/breitbart",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.55),
]

# Tier 8: Tabloid & Entertainment (High traffic, lower priority)
TIER_8_SOURCES = [
    NewsSource("TMZ", "tmz.com",
               rss_url="https://www.tmz.com/rss.xml",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.6),
    NewsSource("Page Six", "pagesix.com",
               rss_url="https://pagesix.com/feed/",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.65),
    NewsSource("Radar Online", "radaronline.com",
               rate_limit_seconds=1.0, priority=5, reliability_score=0.55),
    NewsSource("National Enquirer", "nationalenquirer.com",
               rate_limit_seconds=1.0, priority=5, reliability_score=0.5),
    NewsSource("People Magazine", "people.com",
               rss_url="https://people.com/feed/",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.7),
    NewsSource("Us Weekly", "usmagazine.com",
               rate_limit_seconds=1.0, priority=4, reliability_score=0.65),
    NewsSource("Entertainment Tonight", "etonline.com",
               rate_limit_seconds=1.0, priority=5, reliability_score=0.6),
    NewsSource("Hollywood Reporter", "hollywoodreporter.com",
               rss_url="https://www.hollywoodreporter.com/t/news/feed/",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.8),
    NewsSource("Variety", "variety.com",
               rss_url="https://variety.com/feed/",
               rate_limit_seconds=1.5, priority=4, reliability_score=0.8),
]

# Combine all sources
ALL_SOURCES = (
    TIER_1_SOURCES + TIER_2_SOURCES + TIER_3_SOURCES + TIER_4_SOURCES +
    TIER_5_SOURCES + TIER_6_SOURCES + TIER_7_SOURCES + TIER_8_SOURCES
)


def get_sources_by_priority(min_priority: int = 1, max_priority: int = 10) -> List[NewsSource]:
    """Get sources filtered by priority range."""
    return [s for s in ALL_SOURCES if min_priority <= s.priority <= max_priority and s.active]


def get_sources_with_rss() -> List[NewsSource]:
    """Get sources that have RSS feeds."""
    return [s for s in ALL_SOURCES if s.rss_url and s.active]


def get_sources_by_tier(tier: int) -> List[NewsSource]:
    """Get sources by tier number (1-8)."""
    tiers = {
        1: TIER_1_SOURCES,
        2: TIER_2_SOURCES,
        3: TIER_3_SOURCES,
        4: TIER_4_SOURCES,
        5: TIER_5_SOURCES,
        6: TIER_6_SOURCES,
        7: TIER_7_SOURCES,
        8: TIER_8_SOURCES,
    }
    return [s for s in tiers.get(tier, []) if s.active]


def get_high_reliability_sources(min_score: float = 0.85) -> List[NewsSource]:
    """Get sources with high reliability scores."""
    return [s for s in ALL_SOURCES if s.reliability_score >= min_score and s.active]


def get_sources_by_domain(domains: List[str]) -> List[NewsSource]:
    """Get sources matching specific domains."""
    return [s for s in ALL_SOURCES if s.domain in domains]


def get_source_stats() -> Dict:
    """Get statistics about configured sources."""
    total = len(ALL_SOURCES)
    with_rss = len(get_sources_with_rss())
    by_tier = {i: len(get_sources_by_tier(i)) for i in range(1, 9)}
    high_rel = len(get_high_reliability_sources(0.85))

    return {
        'total_sources': total,
        'with_rss': with_rss,
        'by_tier': by_tier,
        'high_reliability': high_rel,
        'tier_names': {
            1: 'Major International',
            2: 'Regional & Metro',
            3: 'Investigative & Legal',
            4: 'International',
            5: 'Business & Financial',
            6: 'Alternative & Independent',
            7: 'Right-leaning',
            8: 'Tabloid & Entertainment'
        }
    }


if __name__ == "__main__":
    # Print source statistics
    stats = get_source_stats()
    print(f"Total sources: {stats['total_sources']}")
    print(f"With RSS feeds: {stats['with_rss']}")
    print(f"High reliability (≥0.85): {stats['high_reliability']}")
    print("\nBy tier:")
    for tier, count in stats['by_tier'].items():
        print(f"  Tier {tier} ({stats['tier_names'][tier]}): {count}")
