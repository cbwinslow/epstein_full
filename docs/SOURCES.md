# Data Sources — Complete Reference

> **Last Updated:** March 26, 2026
> **Purpose:** Master list of all known data sources for the Epstein case files

---

## Overview

This document catalogs ALL known data sources for the Epstein case files, their acquisition status, and how to obtain them.

---

## 1. DOJ EFTA Releases (Primary Documents)

**Status:** ✅ 94% Downloaded (177GB, 1.3M files)

| Dataset | EFTA Range | Size | Status |
|---------|-----------|------|--------|
| DS1 | 00000001–00003158 | 1.3GB | ✅ |
| DS2 | 00003159–00003857 | 632MB | ✅ |
| DS3 | 00003858–00005586 | 598MB | ✅ |
| DS4 | 00005705–00008320 | 359MB | ✅ |
| DS5 | 00008409–00008528 | 62MB | ✅ |
| DS6 | 00008529–00008998 | 54MB | ✅ |
| DS7 | 00009016–00009664 | 99MB | ✅ |
| DS8 | 00009676–00039023 | 1.8GB | ✅ |
| DS9 | 00039025–01262781 | 76GB | ⚠️ 94% |
| DS10 | 01262782–02212882 | 68GB | ✅ |
| DS11 | 02212883–02730262 | 28GB | ✅ |
| DS12 | 02730265–02731783 | 127MB | ✅ |

**Sources:**
- RollCall CDN: `https://media-cdn.rollcall.com/epstein-files/EFTA{N}.pdf`
- Archive.org: Various mirrors
- DOJ: `https://www.justice.gov/epstein/files/DataSet%20{N}/EFTA{N}.pdf`

---

## 2. jmail.world (Primary Email Source)

**Status:** ❌ NOT DOWNLOADED

**URL:** `https://data.jmail.world/v1/`

| File | Size | Records | Description |
|------|------|---------|-------------|
| `emails-slim.parquet` | 38.8MB | 1,783,792 | All email data |
| `imessage_conversations.parquet` | 3.6KB | 4,509 | iMessage threads |
| `imessage_messages.parquet` | 168KB | Unknown | iMessage messages |
| `photos.parquet` | 1.0MB | 18,000 | Photos with metadata |
| `people.parquet` | 9.9KB | 473 | People in photos |
| `photo_faces.parquet` | 57.7KB | 975 | Face detections |

**Email Breakdown:**
- DOJ EFTA (VOL00009-12): 1,756,912 emails (same source as our 42K, but 42x better extraction)
- Epstein Yahoo inbox: 17,448 emails (NEW DATA)
- House Oversight: 8,374 emails (NEW DATA)
- Ehud Barak: 1,058 emails (NEW DATA)

**Ingest Script:** `Epstein-Pipeline/scripts/ingest-jmail.py`

---

## 3. HuggingFace Datasets

**Status:** 1 of 4 Downloaded

| Dataset | Size | Records | Status |
|---------|------|---------|--------|
| `qanon-research/epstein-documents` | 318GB | ~2.87M rows | ✅ Downloaded |
| `qanon-research/epstein-emails` | ~12MB | 5,258 | ❌ Missing |
| `qanon-research/epstein-flight-logs` | ~2.5MB | Unknown | ❌ Missing |
| `qanon-research/epstein-black-book` | ~1MB | Unknown | ❌ Missing |

**URL Pattern:** `https://huggingface.co/datasets/qanon-research/{name}`

---

## 4. Pre-built SQLite Databases

**Status:** ✅ All Downloaded & Migrated to PostgreSQL

| Database | Size | Key Content |
|----------|------|-------------|
| full_text_corpus.db | 7.0GB | 1.4M docs, 2.9M pages, FTS5 |
| redaction_analysis_v2.db | 940MB | 2.59M redactions |
| image_analysis.db | 389MB | 38,955 images |
| ocr_database.db | 68MB | 38,955 OCR results |
| communications.db | 30MB | 41,924 emails |
| transcripts.db | 4.8MB | 1,628 transcriptions |
| prosecutorial_query_graph.db | 2.5MB | 257 subpoenas |
| knowledge_graph.db | 892KB | 606 entities, 2,302 relationships |

**Source:** `https://github.com/rhowardstone/Epstein-research-data/releases`

---

## 5. epsteinexposed.com API

**Status:** ⚠️ Partially Downloaded

**Base URL:** `https://epsteinexposed.com/api/v2`
**Rate Limit:** 100 req/hr anonymous

| Endpoint | Records | Status |
|----------|---------|--------|
| `/export/persons` | 1,578 | ✅ Downloaded |
| `/export/flights` | 3,615 | ✅ Downloaded |
| `/export/locations` | 83 | ✅ Downloaded |
| `/export/organizations` | 55 | ✅ Downloaded |
| `/emails` | 100/11,280 | ⚠️ Partial |
| `/documents` | 0/2.1M | ❌ Not viable (9+ days) |

---

## 6. Kaggle Datasets

**Status:** ❌ NOT DOWNLOADED

| Dataset | Records | Description |
|---------|---------|-------------|
| Epstein Ranker | ~23,700 | AI-analyzed documents with summaries |

**URL:** `https://www.kaggle.com/datasets/jamesgrantz/epstein-ranker`
**Download:** Requires kaggle CLI + API token

---

## 7. Archive.org Collections

**Status:** ⚠️ Partial

| Collection | Status | Description |
|------------|--------|-------------|
| epstein-files (DOJ) | ✅ Downloaded | DS1-12 releases |
| jeffrey-epstein-court-documents | ❌ Not downloaded | Court filings |
| epstein-maxwell-documents | ❌ Not downloaded | Maxwell trial docs |
| jeffrey-epstein-photos | ❌ Not downloaded | FBI raid photos |
| epstein-flight-logs | ❌ Not downloaded | Flight log scans |

---

## 8. FBI Vault

**Status:** ❌ NOT DOWNLOADED

**URL:** `https://vault.fbi.gov/jeffrey-epstein/`
**Content:** 22 PDF parts of FBI investigative files
**Mirror:** Available on Archive.org

---

## 9. CourtListener

**Status:** ❌ NOT DOWNLOADED

**URL:** `https://courtlistener.com`
**Content:** Court records for Giuffre v. Maxwell, US v. Maxwell, etc.
**Access:** Free API

---

## 10. House Oversight Committee

**Status:** ⚠️ Partial

**Content:** Email dumps, schedules, depositions
**URL:** `https://docs.house.gov`
**Note:** Some data included in jmail.world emails (8,374 records)

---

## 11. ICIJ Offshore Leaks

**Status:** ❌ NOT DOWNLOADED

**URL:** `https://offshoreleaks.icij.org/pages/database`
**Content:** Panama Papers, Paradise Papers, Pandora Papers
**Access:** Free bulk CSV download

---

## 12. OpenSanctions

**Status:** ❌ NOT DOWNLOADED (API key needed)

**URL:** `https://www.opensanctions.org`
**Content:** Sanctions lists, PEP registries, OFAC SDN
**Requires:** `EPSTEIN_OPENSANCTIONS_API_KEY`

---

## 13. FEC Political Donations

**Status:** ⚠️ Partial (400 donations, 3,600 disbursements)

**URL:** `https://api.open.fec.gov/v1/`
**Requires:** `EPSTEIN_FEC_API_KEY`

---

## 14. IRS Form 990 Nonprofits

**Status:** ❌ NOT DOWNLOADED

**URL:** `https://projects.propublica.org/nonprofits/api/v2/`
**Content:** Nonprofit financials, officers, grants

---

## 15. SEC EDGAR

**Status:** ❌ NOT DOWNLOADED

**URL:** `https://edgar.sec.gov`
**Content:** Form 4 insider trading filings
**Access:** Free API

---

## Priority Acquisition Order

| # | Source | Effort | Value | Action |
|---|--------|--------|-------|--------|
| 1 | jmail.world emails | Easy | CRITICAL | Download 38.8MB parquet |
| 2 | jmail.world iMessages | Easy | HIGH | Download 168KB parquet |
| 3 | jmail.world photos | Easy | MEDIUM | Download 1MB parquet |
| 4 | HF epstein-emails | Easy | MEDIUM | Download parquet |
| 5 | HF epstein-flight-logs | Easy | MEDIUM | Download parquet |
| 6 | HF epstein-black-book | Easy | MEDIUM | Download parquet |
| 7 | ICIJ Offshore Leaks | Medium | HIGH | Download bulk CSVs |
| 8 | FBI Vault | Medium | MEDIUM | Download from Archive.org |
| 9 | CourtListener | Medium | HIGH | Query API |
| 10 | OpenSanctions | Easy | MEDIUM | Get API key |
| 11 | IRS Form 990 | Medium | MEDIUM | Run ProPublica API |
| 12 | Kaggle Ranker | Medium | LOW | Download via kaggle CLI |
| 13 | SEC EDGAR | Medium | MEDIUM | Query SEC API |

---

*This document should be updated as new data sources are identified or acquired.*
