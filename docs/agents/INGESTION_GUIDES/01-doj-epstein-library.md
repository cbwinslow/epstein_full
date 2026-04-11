# Data Source: DOJ Epstein Library

> **Source:** https://www.justice.gov/epstein-library  
> **Type:** Official Government Documents  
> **License:** Public Domain  
> **Status:** ✅ Complete (260K+ PDFs downloaded)  
> **Size:** 19.8 GB  

---

## 📋 Data Overview

The DOJ Epstein Library contains the complete EFTA (Epstein Files Transparency Act) document release from the U.S. Department of Justice. This includes:

- Court documents
- Emails and correspondence
- Flight logs
- Financial records
- Photos and images
- Audio/video files

### Dataset Breakdown (data1-12)

| Dataset | Files | Size | Description |
|---------|-------|------|-------------|
| data1 | ~47K | ~3.5 GB | General documents |
| data2 | ~411 | ~467 MB | Legal filings |
| data3 | ~29 | ~2.1 MB | Financial records |
| data4 | ~103 | ~103 MB | Correspondence |
| data5 | ~120 | ~62 MB | Images |
| data6 | ~14 | ~245 MB | Videos/Audio |
| data7 | ~18 | ~320 MB | Special collections |
| data8 | ~3,485 | ~3.2 GB | Flight logs, emails |
| data9 | ~1 | ~2.1 GB | Combined PDF |
| data10 | - | - | Additional releases |
| data11 | ~260K | ~19.8 GB | Bulk documents |
| data12 | ~102 | ~2.1 GB | Recent releases |

---

## 🔧 Ingestion Pipeline

### Tool: epstein-ripper

**Location:** `/home/cbwinslow/workspace/epstein/epstein-ripper/`

**Main Script:** `auto_ep_rip.py`

**Features:**
- Playwright browser automation
- Handles DOJ age gate
- Scrapes paginated dataset pages
- Validates PDF signatures (rejects HTML poison)
- Resume capability with state files
- Rate limiting: 0.75s between downloads

---

## 📥 Download Procedure

### Step 1: Navigate to ripper directory

```bash
cd /home/cbwinslow/workspace/epstein/epstein-ripper
```

### Step 2: Download specific dataset

```bash
# Download data1 (example)
python3 auto_ep_rip.py --dataset data1

# Resume interrupted download
python3 auto_ep_rip.py --dataset data1 --resume
```

### Step 3: Validate downloads

```bash
python3 corruption_scan.py /home/cbwinslow/workspace/epstein-data/raw-files/data1/
```

---

## 🗄️ Database Schema

### PostgreSQL Tables (Already Created)

| Table | Records | Description |
|-------|---------|-------------|
| `exposed_persons` | 1,578 | Named individuals |
| `exposed_flights` | 3,615 | Flight records |
| `exposed_locations` | 83 | Physical locations |
| `exposed_organizations` | 55 | Companies/entities |
| `exposed_nonprofits` | 33 | Nonprofit orgs |

### Key Files

- **Black Book:** Contact directory with addresses/phones
- **Flight Logs:** Passenger manifests 1991-2019
- **Emails:** Correspondence from various accounts
- **Photos:** Images from events, properties

---

## 🔄 Processing Pipeline

### 1. OCR Extraction

```bash
# Extract text from all PDFs
epstein-pipeline ocr ./raw-pdfs/ -o ./ocr_output/
```

### 2. Entity Extraction

```bash
# Extract named entities
epstein-pipeline extract-entities ./ocr_output/
```

### 3. Image Extraction

```bash
# Extract images from PDFs
epstein-pipeline extract-images ./raw-pdfs/
```

---

## 📊 Quality Metrics

| Metric | Value | Target |
|--------|-------|--------|
| PDFs Downloaded | 260,000+ | 100% |
| OCR Coverage | 1.4M pages | 100% |
| Entities Extracted | 5.7M | - |
| Embeddings | 230,931 | 7.98% |

---

## ⚠️ Known Issues

1. **Data11 Large Files:** Some PDFs in data11 are 50MB+ (OCR takes 15-30 min each)
2. **Corrupted PDFs:** ~100 files have corruption issues (tracked in `recovered_corrupted_pdfs/`)
3. **HTML Poison:** Some downloads return HTML instead of PDF (validation catches these)

---

## 🔗 Related Sources

- **jMail World:** Overlapping email content
- **GitHub/dleerdefi:** Black Book + Flight Log extractions
- **HuggingFace:** House Oversight additional documents

---

## 📝 For AI Agents

### When Working with This Data:

1. **Check existing downloads** before starting new ones
2. **Use resume capability** for interrupted downloads
3. **Validate PDFs** after download (signature check)
4. **Update inventory** when adding new datasets
5. **Respect rate limits** (0.75s between downloads)

### File Locations:

- Downloads: `/home/cbwinslow/workspace/epstein-data/raw-files/data{1-12}/`
- OCR Output: `/home/cbwinslow/workspace/epstein-data/processed/ocr/`
- Entities: `/home/cbwinslow/workspace/epstein-data/processed/entities/`

---

*Last Updated: April 10, 2026*
