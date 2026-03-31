# Supplementary Datasets — Cross-Referencing the Epstein Files

## Overview

The HF parquet dataset (AfricanKillshot/Epstein-Files, 634 files, 318GB)
contains **only DOJ EFTA data** — PDF text extractions and images from
the 12 DOJ data sets. It does NOT contain flight logs, emails, political
donations, financial records, or any supplementary sources.

The following datasets are **NOT covered by our current data** and must
be acquired separately to enable cross-referencing analysis.

### What We Already Have (Covered)

| Source | Status | Size |
|--------|--------|------|
| DOJ EFTA PDFs (DS1-12) | ✅ Downloaded (583K+ files) | ~106GB |
| HF Parquet (pre-extracted text) | ✅ Complete (634/634) | 318GB |
| Pre-built SQLite databases | ✅ Downloaded (8 DBs) → migrated to PG | 8.4GB |
| Epstein Exposed persons | ✅ Downloaded (1,578) | 733KB |
| Epstein Exposed flights | ✅ Downloaded (3,615) | 1.2MB |
| Epstein Exposed locations | ✅ Downloaded (83) | 47KB |
| Epstein Exposed organizations | ✅ Downloaded (55) | 18KB |
| Epstein Exposed nonprofits | ✅ Downloaded (33) | 19KB |
| Epstein Exposed emails | 🔄 Partial (100/11,280) | 28KB |
| FEC donations | ✅ Downloaded (400) | 1.8MB |
| FEC disbursements | ✅ Downloaded (3,600) | 16MB |
| Knowledge graph (606 entities) | ✅ Migrated to PG | 892KB |
| **kabasshouse entities** | ✅ **Imported (9,893,147)** | **~100MB** |
| **kabasshouse chunks** | ✅ **Imported (1,874,012)** | **~500MB** |
| **kabasshouse embeddings** | ✅ **Imported (1,505,618, 768-dim)** | **~12GB** |
| **kabasshouse financial** | ✅ **Imported (49,770)** | **~5MB** |
| **kabasshouse redactions** | ✅ **Imported (22,355)** | **~5MB** |
| **kabasshouse events** | ✅ **Imported (3,038)** | **~1MB** |
| **kabasshouse curated docs** | ✅ **Imported (1,398)** | **~2MB** |
| **House Oversight emails** | ✅ **Imported (5,082 threads)** | **~10MB** |
| **FBI Vault PDFs** | 🔄 **OCR running (16 PDFs)** | **35MB** |

### What We Still Need

| Source | Status | Priority |
|--------|--------|----------|
| Epstein Exposed emails (remaining 11,180) | 🔄 Pending (rate limited) | HIGH |
| Epstein Exposed network graph | 🔄 Pending | MEDIUM |
| Epstein Exposed DOJ audit data | 🔄 Pending | MEDIUM |
| Epstein Exposed stats | 🔄 Pending | LOW |
| SEC insider trading filings | ❌ Not acquired | MEDIUM |
| FBI Vault PDFs | 🔄 OCR running (16 PDFs) | MEDIUM |
| Court records (CourtListener) | ❌ Not queried | MEDIUM |
| Court records (structured) | ❌ Partial | MEDIUM |
| Epstein Web Tracker data | ❌ Not queried | MEDIUM |

This document catalogs all available supplementary datasets organized by category.

---

## 1. Flight Logs

### Primary Sources

| Source | Records | Period | Format | URL |
|--------|---------|--------|--------|-----|
| DOJ EFTA Datasets | Embedded in PDFs | 1991–2019 | PDF scans | justice.gov/epstein |
| Epstein Exposed API | 3,615 entries | 1991–2019 | REST API (JSON) | epsteinexposed.com/flights |
| Scribd (multiple uploads) | ~72 pages | 1995–2007 | PDF | scribd.com |
| Journal 425 | 72 pages | 1995–2007 | PDF | thejournal425.com |
| Giuffre v. Maxwell exhibits | Filed | Various | Court records | CourtListener |

### Aircraft Tracked

| Aircraft | Type | Tail Number | Period |
|----------|------|-------------|--------|
| Boeing 727-31 | "Lolita Express" | N908JE | 1995–2013 |
| Gulfstream II | Business jet | N120JE | Various |
| Gulfstream IV | Business jet | N212JE | Various |
| Helicopter(s) | Various | Various | Various |

### Data Fields Available
- Date, departure airport, arrival airport
- Passenger names (sometimes first-name only)
- Flight crew (Larry Visoski, David Rodgers)
- Routes: New York ↔ Palm Beach ↔ New Mexico ↔ USVI ↔ International

### Analysis Opportunities
- **Temporal clustering**: Which passengers flew together?
- **Route patterns**: Frequency of visits to specific properties
- **Co-traveler networks**: Who traveled with whom?
- **Post-conviction flights**: Continued activity after 2008 plea

---

## 2. Emails & Correspondence

### Sources

| Source | Count | Period | Format |
|--------|-------|--------|--------|
| DOJ EFTA (full_text_corpus.db) | 41,924 emails | Various | SQLite |
| Bloomberg Yahoo cache | 18,000+ emails | Various | Reporting |
| House Oversight Committee | Thousands | Various | PDF/CSV |
| Epstein Exposed curated | 9,900+ | Various | API |
| JMail.World | Various | Various | Web interface |

### Data Fields
- From/To addresses, date, subject, body text
- Attachments (references to documents, images)
- Thread chains (conversations)

### Analysis Opportunities
- **Temporal correlation**: Emails before/after stock trades by recipients
- **Network analysis**: Communication frequency, response times
- **Topic modeling**: What subjects dominated Epstein's correspondence?
- **Sentiment analysis**: Tone changes over time (pre/post arrest)

---

## 3. Political Donations (FEC Data)

### Source: OpenSecrets / FEC

Epstein's documented political donations (1991–1997):

| Date | Amount | Recipient | Party |
|------|--------|-----------|-------|
| 1992-08-12 | $1,000 | George Bush | R |
| 1991-09-24 | $1,000 | John Kerry | D |
| 1997-12-12 | $1,000 | Freedom Project | R |
| 1992-1997 | $7,000 | Chuck Schumer (7 × $1,000) | D |
| 1998-10 | $10,000 | Victory in NY (Schumer/DSCC) | D |
| 1998-10 | $5,000 | Win NY / Liberal Party | D |
| 2002-04-30 | $1,000 | Richard Gephardt | D |

**Total documented: 46 records**

### Data Source
- URL: https://www.opensecrets.org/donor-lookup/results?name=EPSTEIN%2C+JEFFREY+E
- Format: Searchable web table (scrapeable)

### Analysis Opportunities
- **Party distribution**: Epstein donated to both parties (D and R)
- **Timing**: Donations relative to legal proceedings
- **Recipient network**: Who received Epstein money and what happened next?

---

## 4. Financial / Stock Market Data

### Potential Cross-References

| Source | Data Available | Access |
|--------|---------------|--------|
| SEC EDGAR | Insider trading filings (Form 4) | edgar.sec.gov (free API) |
| OpenSecrets | Lobbying expenditures | opensecrets.org |
| FEC | Campaign finance (donations, PACs) | fec.gov/data |
| Federal Reserve | Large bank transaction reports | (limited public access) |
| JPMorgan settlement docs | $1B+ in transactions | Court filings |

### Key Entities to Track

Based on reporting:
- **JPMorgan Chase**: Processed $1B+ for Epstein (1998–2013)
- **Apollo Global Management**: Leon Black paid $158M to Epstein (2012–2017)
- **Bear Stearns**: Epstein's former employer, investment fund disputes
- **Barclays**: Jes Staley (1,200+ emails with Epstein)

### Analysis Approach
1. Identify persons in Epstein's network who are officers/directors of public companies
2. Pull their SEC Form 4 (insider trading) filings
3. Cross-reference trade dates with Epstein email dates
4. **Statistical test**: Is there a temporal correlation between Epstein contact and subsequent trades?

**Important caveat**: Correlation ≠ causation. Any findings must be framed as exploratory, not accusatory.

---

## 5. Property Records

### Epstein Properties

| Property | Location | Status |
|----------|----------|--------|
| 9 East 71st Street | New York, NY | Sold 2021 ($51M) |
| Little St. James | USVI | "Pedophile Island" |
| Great St. James | USVI | Purchased 2016 |
| Zorro Ranch | Stanley, NM | 33,000 acres |
| Palm Beach estate | Palm Beach, FL | Original location |

### Data Sources
- County property records (public, searchable)
- FAA aircraft registry
- Corporate filings (shell companies)
- USVI corporate registry

---

## 6. Known-Entity Databases

### Pre-Indexed Resources

| Resource | URL | What It Contains |
|----------|-----|------------------|
| Epstein Exposed | epsteinexposed.com | 1,463+ persons, 3,615 flights, 9,900 emails, REST API |
| Epstein Web Tracker | epsteinweb.org | Entity relationship graph, degree-of-separation paths |
| Epstein's Inbox | epsteinsinbox.com | Flight logs, document archive |
| EpsteinWiki | epsteinwiki.com | OSINT resource directory, timelines |
| JMail.World | jmail.world | Searchable email/document browser |

### Epstein Exposed API (Free, Public)
```
Base URL: https://epsteinexposed.com/api/v2
Endpoints: /persons, /documents, /flights, /emails, /locations, /entities
Search: semantic + full-text hybrid
```

### Epstein Web Tracker
- Entity resolution with degree-of-separation paths
- Example: "Shortest path to Jeffrey Epstein: 1 degree(s)"
- Categories: Persons, Organizations, Locations, Properties, Aircraft

---

## 7. Court Records

### Key Cases

| Case | Court | Documents |
|------|-------|-----------|
| Giuffre v. Maxwell | S.D.N.Y. | Depositions, exhibits, flight logs |
| US v. Maxwell | S.D.N.Y. | Criminal trial exhibits |
| US v. Epstein | S.D.N.Y. (2019) | Indictment, evidence |
| Doe v. Epstein | S.D. Fla. | Victim depositions |
| USVI v. JPMorgan | S.D.N.Y. | Banking relationship docs |
| Victims' Compensation Fund | Independent | Claims, awards |

### Access
- CourtListener (free): courtlistener.com
- PACER (paid): pacer.uscourts.gov
- DocumentCloud (free): documentcloud.org

---

## 8. FBI & Government Records

| Source | Content | Access |
|--------|---------|--------|
| FBI Vault | Investigative files | vault.fbi.gov (free) |
| House Oversight Committee | Email dumps, schedules | docs.house.gov |
| DOJ EFTA (our data) | 1.4M documents | Downloaded |
| BOP records | Jail/death records | In DOJ EFTA |

---

## 9. Recommended Analysis Workflow

### Phase 1: Entity Extraction (Current)
- OCR → NER → Entity registry from DOJ documents

### Phase 2: Cross-Reference
- Match extracted entities against:
  - FEC donation records
  - SEC insider trading filings
  - Flight log passenger lists
  - Epstein Exposed API person index
  - Pre-built knowledge graph (606 entities)

### Phase 3: Temporal Correlation
- Build timeline: [Email date] → [Stock trade date] → [Legal event date]
- Statistical analysis: Do trades cluster after Epstein contact?
- **Null hypothesis**: No temporal relationship between contact and trades

### Phase 4: Network Analysis
- Build multi-source graph: DOJ entities + FEC donors + flight passengers + email correspondents
- Identify high-centrality nodes (people connected across multiple data sources)
- Compute betweenness centrality (who are the "bridges"?)

### Phase 5: Validation
- Cross-validate findings against known reporting (Reuters, Bloomberg, CNN)
- Manual verification of high-confidence patterns
- Statistical significance testing

---

## 10. Data Acquisition Priority

| Priority | Dataset | Size | Difficulty | Value |
|----------|---------|------|------------|-------|
| 1 | FEC/OpenSecrets donations | Small (46 records) | Easy (scrape) | High |
| 2 | Epstein Exposed API | Medium | Easy (REST API) | Very High |
| 3 | SEC EDGAR insider trades | Large | Medium (API) | Medium |
| 4 | Flight logs (structured) | Small (3,615 records) | Medium (parse) | Very High |
| 5 | Epstein Web Tracker data | Medium | Medium (scrape) | High |
| 6 | Court records (CourtListener) | Large | Medium (API) | High |
| 7 | Property records | Small | Easy (public) | Low |
| 8 | Lobbying records | Medium | Medium (API) | Medium |

---

## 11. Legal & Ethical Considerations

1. **Public domain**: FEC data, SEC filings, court records are public
2. **Named individuals**: Document inclusion ≠ accusation of wrongdoing
3. **Victims**: Never publish identifying information about victims
4. **DOJ disclaimer**: "Material may include fake images or untrue allegations"
5. **Correlation vs Causation**: Temporal patterns are exploratory, not proof
6. **Responsible framing**: "Documented association" not "implicated in"
