# Government Data Acquisition Plan
**Date:** April 13, 2026

## Summary

All government datasets have been verified as **FREE** and **ready for acquisition**.

- **Total Datasets:** 11 government data sources
- **Total Estimated Records:** ~85+ million records
- **Total Estimated Size:** ~50-60 GB
- **API Keys Secured:** 3 keys (Congress.gov, GovInfo.gov, FEC.gov)
- **SEC EDGAR:** No key required (requires User-Agent with contact email)

---

## Data Sources

### Phase 1: No API Key Required (Immediate Start)

| # | Dataset | Records | Size | Priority | GitHub Issue |
|---|---------|---------|------|----------|--------------|
| 1 | FEC 2025 Individual Contributions | ~20M | 3 GB | HIGH | #88 |
| 2 | SEC EDGAR Form 4 (Insider) | ~8M | 5 GB | HIGH | #89 |
| 3 | SEC EDGAR Form 13F (Institutional) | ~500K | 2 GB | MEDIUM | #89 |
| 4 | White House Visitor Logs | ~5M | 1 GB | HIGH | #90 |
| 5 | FARA Registrations | ~50K | 200 MB | MEDIUM | #93 |
| 6 | Lobbying Disclosures | ~200K | 500 MB | MEDIUM | #94 |
| 7 | USA Spending | ~50M | 25 GB | MEDIUM | #94 |

### Phase 2: API Key Required

| # | Dataset | Records | Size | Priority | GitHub Issue |
|---|---------|---------|------|----------|--------------|
| 8 | Congress.gov Bills & Legislation | ~200K | 500 MB | MEDIUM | #91 |
| 9 | Congress.gov Members & Votes | ~10K | 100 MB | MEDIUM | #91 |
| 10 | GovInfo Federal Register | ~100K | 500 MB | MEDIUM | #92 |
| 11 | GovInfo Court Opinions | ~50K | 200 MB | MEDIUM | #92 |

---

## API Keys Secured

All API keys stored in:
- `.env` file (project root)
- `.bash_secrets` file (project root)

### Keys Obtained:

| Source | Key Name | Key Value (truncated) | Rate Limit |
|--------|----------|----------------------|------------|
| Congress.gov | CONGRESS_API_KEY | U71JFZEqNs...l18cIJc2 | 5000/day |
| GovInfo.gov | GOVINFO_API_KEY | oiihWFbDA...2LiJmN | Varies |
| FEC.gov | FEC_API_KEY | FpB5TzG4h...MKRLDXFm | 1000/hour |
| SEC EDGAR | N/A | No key required | 10/sec |

---

## Multi-Agent Ingestion Strategy

### Recommended Approach: Orchestrator + Worker Agents

```
Orchestrator Agent
├── Download Worker 1: FEC Data
├── Download Worker 2: SEC EDGAR
├── Download Worker 3: White House
├── Download Worker 4: FARA + Lobbying
├── Download Worker 5: Congress.gov
└── Download Worker 6: GovInfo + USA Spending
```

### Parallel Processing
- **Phase 1 datasets:** Can run in parallel (no API key dependencies)
- **Phase 2 datasets:** Coordinate API key usage to respect rate limits
- **Database loading:** Single writer to prevent locks

### Coordination Mechanism
- SQLite queue for download tasks
- PostgreSQL `data_inventory` for status tracking
- Lock files to prevent duplicate downloads
- Resume capability via state files

---

## Timeframe Coverage

All datasets target **2000-2025** (25-year window):

- **FEC:** 2000-2025 (bulk download available)
- **SEC EDGAR:** 2000-2025 (daily filings from 1994)
- **White House:** 2009-2025 (Obama onwards)
- **Congress:** 2000-2025 (full coverage)
- **GovInfo:** 2000-2025 (varies by collection)
- **FARA:** 2000-2025 (digital from ~2000)
- **Lobbying:** 2000-2025 (available from 1999)
- **USA Spending:** 2007-2025 (digital from 2007)

---

## Cross-Reference Potential

These datasets enable powerful entity linking:

| Connection | Datasets | Value |
|------------|----------|-------|
| **Financial → Political** | SEC EDGAR ↔ FEC | Insider trader also donates |
| **Corporate → Government** | SEC ↔ White House | Board member meets official |
| **Foreign → Domestic** | FARA ↔ ICIJ | Foreign agent has offshore entity |
| **Legislative → Financial** | Congress ↔ Lobbying ↔ FEC | Legislator votes on bill, lobbied by X, received donations from Y |
| **News → All** | GDELT ↔ All datasets | Person mentioned in news also appears in official records |
| **Flight Logs → All** | Flight logs ↔ FEC/SEC/ICIJ | Person flew on plane, also donor/board member/offshore officer |

---

## GitHub Issues Created

All datasets tracked in GitHub:

1. #88 - FEC Campaign Finance 2025
2. #89 - SEC EDGAR Insider Trading
3. #90 - White House Visitor Logs
4. #91 - Congress.gov Legislative Data
5. #92 - GovInfo.gov Federal Documents
6. #93 - FARA Foreign Agent Registrations
7. #94 - Lobbying Disclosure Database
8. #95 - USA Spending Federal Contracts

Each issue contains:
- Full source details
- Database schema
- Ingestion strategy
- Validation requirements
- Cross-reference potential

---

## Next Steps

### Immediate (Today)
1. ✅ API keys secured
2. ✅ GitHub issues created
3. ✅ Data inventory SQL prepared
4. ⏳ Run SQL to update inventory
5. ⏳ Start downloading Phase 1 datasets

### This Week
1. ⏳ Complete Phase 1 downloads
2. ⏳ Validate and load to PostgreSQL
3. ⏳ Begin Phase 2 API downloads
4. ⏳ Create ingestion logs

### Next Week
1. ⏳ Complete all downloads
2. ⏳ Cross-validate entities
3. ⏳ Generate data quality reports
4. ⏳ Update master inventory

---

## Compliance & Ethics

- ✅ All datasets are **public records**
- ✅ No paid tiers required
- ✅ Rate limits respected
- ✅ User-Agent headers with contact info
- ✅ Data acquisition rule created (`.windsurf/rules/data_acquisition.md`)
- ✅ Detailed logging requirements established
- ✅ Reproducibility ensured (GitHub, documentation)

---

## Total Data Volume Estimate

| Category | Records | Size |
|------------|---------|------|
| **Existing Data** | ~20M | ~100 GB |
| **New Gov Data** | ~85M | ~50-60 GB |
| **Grand Total** | **~105M** | **~150-160 GB** |

This represents a comprehensive dataset for investigative analysis.
