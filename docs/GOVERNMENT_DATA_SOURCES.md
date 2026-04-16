# Government Datasets for People/Event Linking

## Priority Datasets for Epstein Investigation

### 1. ✅ FEC Campaign Finance (ALREADY HAVE)
- **What:** Individual contributions, committee donations, candidate filings
- **Source:** fec.gov / bulk data downloads
- **Have:** 1990-2024 (~5.4M records)
- **Need:** 2025 cycle data (indiv25.zip)
- **Value:** Shows political connections, donation patterns

### 2. 🎯 SEC EDGAR - HIGH PRIORITY
- **What:** Insider trading, Form 4 (insider transactions), 13F (institutional holdings)
- **Source:** sec.gov/cgi-bin/browse-edgar?action=getcurrent
- **API:** EDGAR Search API (free, no key needed)
- **Value:** 
  - Board memberships (Form 3/4/5)
  - Financial ties between individuals
  - Company ownership structures
  - Insider transactions
- **Tables:** sec_filings, sec_insider_transactions, sec_13f_holdings

### 3. 🎯 Congress.gov Legislative Data
- **What:** Bills, votes, committee memberships, financial disclosures
- **API:** Congress.gov API (free, requires key)
- **Value:**
  - Voting records on relevant legislation
  - Committee memberships (Judiciary, Oversight)
  - Financial disclosure reports
- **Tables:** congressional_votes, committee_memberships, financial_disclosures

### 4. 🎯 GovInfo.gov - Federal Register & Court Docs
- **What:** Federal Register, Congressional Record, Court opinions
- **API:** GovInfo API (free)
- **Value:**
  - FOIA releases related to Epstein
  - Federal court decisions
  - Rulemaking comments
- **Tables:** federal_register_entries, court_opinions

### 5. 🎯 White House Visitor Logs
- **What:** Who visited the White House, when, who they met with
- **Source:** whitehouse.gov/disclosures/vistor-logs
- **Value:**
  - Direct connections to administration officials
  - Meeting patterns
- **Tables:** whitehouse_visitors

### 6. 🎯 Foreign Agent Registration Act (FARA)
- **What:** Foreign lobbying disclosures, foreign principal relationships
- **Source:** fara.gov / Justice Department
- **Value:**
  - Foreign connections
  - Lobbying relationships
- **Tables:** fara_registrations, fara_documents

### 7. ✅ GDELT News (ALREADY HAVE ~23K articles)
- **What:** News articles mentioning Epstein
- **Source:** GDELT Project
- **Have:** Pre-collected ~23K articles
- **Value:** Media timeline, sentiment analysis, entity co-mentions
- **Need:** Entity extraction, sentiment analysis, cross-reference with other datasets

### 8. 🎯 FOIA Release Documents
- **What:** FBI Vault, State Dept, DOJ releases
- **Source:** vault.fbi.gov, foia.state.gov
- **Value:**
  - Direct case documents
  - Investigation details
  - Communications

### 9. 🎯 USA Spending (Federal Contracts)
- **What:** Federal contracts, grants, loans
- **Source:** usaspending.gov
- **API:** Free API available
- **Value:**
  - Business relationships with government
  - Contract patterns

### 10. 🎯 Lobbying Disclosure Database
- **What:** Lobbying registrations, quarterly reports
- **Source:** senate.gov/legislative/lobbying
- **Value:**
  - Lobbying firm connections
  - Issue areas lobbied

---

## Recommended Priority Order

### Phase 1: Immediate (Today)
1. **2025 FEC data** - Easy, bulk download available
2. **SEC EDGAR insider trading** - High value for financial connections

### Phase 2: This Week
3. **GDELT entity extraction** - Process the 23K articles we have
4. **White House Visitor Logs** - Download available
5. **FARA data** - Justice Department site

### Phase 3: Next
6. **Congress.gov API** - Requires API key request
7. **GovInfo court docs** - Search for relevant cases
8. **FOIA collections** - FBI Vault deep dive

---

## Technical Notes

### FEC 2025 Data
```
URL: https://www.fec.gov/files/bulk-downloads/2025/indiv25.zip
Size: ~2-3 GB (growing as cycle progresses)
Update: Weekly during election cycle
```

### SEC EDGAR API
```
Base: https://www.sec.gov/Archives/edgar/daily-index/
Form 4 (Insider): https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4
13F (Institutional): https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=13F-HR
Rate Limit: 10 requests/second (be polite!)
```

### Congress.gov API
```
URL: https://api.congress.gov/v3/
Key: Free registration required
Endpoints: /bill, /member, /committee, /nomination
```

### GDELT Analysis
```
We have: 23K+ articles in GDELT collection
Need to: Extract entities, sentiment, cross-reference
Tools: spaCy NER, sentiment analysis, co-occurrence
```

---

## Connection Strategy

**How These Link People/Events:**

1. **FEC + SEC EDGAR:** Donor is also insider trader, board member of company X
2. **Congress + FEC:** Legislator received donations from company Y, voted on Z
3. **White House + FEC:** Visitor donated $X, then got meeting with official
4. **GDELT + All:** News mentions person in context of event, date aligns with other data
5. **FARA + SEC:** Foreign agent also board member of US company
6. **Flight Logs + All:** Person flew on Epstein plane, also appears in FEC/SEC/Congress

**Cross-Reference Keys:**
- Name matching (fuzzy)
- Date ranges
- Geographic locations
- Organization names
- Event mentions
