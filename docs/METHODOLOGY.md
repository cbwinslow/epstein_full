# Research Methodology — Epstein Files Analysis

## Framework: CRISP-DM (Adapted)

We follow the Cross-Industry Standard Process for Data Mining, adapted for
public interest document analysis with NLP, OCR, facial recognition, and
knowledge graph construction.

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: BUSINESS UNDERSTANDING                                │
├─────────────────────────────────────────────────────────────────┤
│  Research Questions:                                            │
│  1. Who are the key entities (people, orgs, locations)?        │
│  2. What are the relationships between entities?               │
│  3. What financial flows and shell company structures exist?   │
│  4. What events can be reconstructed chronologically?         │
│  5. Who appears in images and documents together?             │
│  6. What redactions exist and can they be recovered?          │
├─────────────────────────────────────────────────────────────────┤
│  Success Criteria:                                              │
│  - Knowledge graph with >600 entities, >2000 relationships     │
│  - OCR accuracy >95% (CER <5%) on standard documents          │
│  - NER F1 >0.85 on entity extraction                          │
│  - Facial recognition EER <5% on extracted images             │
│  - Searchable database of all 1.4M documents                  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│  PHASE 2: DATA UNDERSTANDING                                    │
├─────────────────────────────────────────────────────────────────┤
│  Data Sources:                                                  │
│  - DOJ website: 12 datasets, ~1.4M PDFs, ~218GB               │
│  - RollCall CDN: byte-identical copies, no auth               │
│  - HuggingFace: 4.11M rows parquet, pre-extracted text        │
│  - Pre-built DBs: 8 SQLite databases, ~8GB                    │
│  - Archive.org: bulk archives for DS9, DS11, FBI Vault        │
│                                                                 │
│  Data Types:                                                    │
│  - PDF documents (court filings, depositions, correspondence)  │
│  - Images (photos, ID documents, property images)             │
│  - Email communications (sender, recipient, date, body)       │
│  - Financial records (wire transfers, account statements)      │
│  - Flight logs (passengers, dates, routes)                    │
│  - Audio/video (BOP recordings, Maxwell proffer)              │
│                                                                 │
│  Quality Assessment:                                            │
│  - ~67,784 documents confirmed removed (404)                  │
│  - ~23,989 files with size mismatches                         │
│  - PDF quality varies: some are scans, some have text layer   │
│  - Redaction analysis: 2.59M redaction records identified     │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│  PHASE 3: DATA PREPARATION                                      │
├─────────────────────────────────────────────────────────────────┤
│  Pipeline:                                                      │
│  1. Download raw PDFs via CDN (RollCall, aria2c)               │
│  2. Download HF parquet (pre-extracted text)                   │
│  3. Validate PDF signatures (reject HTML/corrupt)              │
│  4. Deduplicate (SHA-256 → MinHash → semantic)                │
│  5. Extract text: PyMuPDF (text layer) → Surya (scanned)     │
│  6. Extract images from PDFs (embedded graphics, photos)      │
│  7. Normalize text (encoding, whitespace, redaction markers)  │
│  8. Split documents into logical units (pages, sections)      │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│  PHASE 4: MODELING                                              │
├─────────────────────────────────────────────────────────────────┤
│  4a. Named Entity Recognition (spaCy + GLiNER)                │
│      - Extract: people, orgs, locations, dates, amounts       │
│      - Model: en_core_web_trf (transformer, GPU)              │
│      - Fallback: GLiNER zero-shot for custom entity types     │
│                                                                 │
│  4b. Facial Recognition (InsightFace + ONNX)                  │
│      - Detect faces in extracted images                       │
│      - Generate 512-D embeddings (ArcFace)                    │
│      - Cluster by identity (cosine similarity + DBSCAN)       │
│      - Match against known persons                            │
│                                                                 │
│  4c. Knowledge Graph Construction                              │
│      - Entity resolution (rapidfuzz name matching)            │
│      - Relationship extraction (co-occurrence, patterns)      │
│      - Graph building (entities + relationships + weights)    │
│                                                                 │
│  4d. Transcription (faster-whisper)                            │
│      - Audio/video files → text + timestamps                  │
│      - Speaker diarization (pyannote)                         │
│                                                                 │
│  4e. Embeddings & Classification                               │
│      - nomic-embed-text-v2-moe (768-D vectors)               │
│      - BART-large-mnli (zero-shot document classification)   │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│  PHASE 5: EVALUATION                                            │
├─────────────────────────────────────────────────────────────────┤
│  OCR Metrics:                                                   │
│  - Character Error Rate (CER) = (S+D+I)/N                    │
│  - Word Error Rate (WER) = (S_w+D_w+I_w)/N_w                │
│  - Weighted Levenshtein (OCR-aware: O/0, l/1 costs)          │
│  - Confidence score from OCR engine                           │
│                                                                 │
│  NER Metrics:                                                   │
│  - Strict F1 (exact boundary + exact type)                    │
│  - Partial F1 (overlapping spans, 0.5× credit)               │
│  - Weak supervision: coverage, conflict, overlap              │
│                                                                 │
│  Facial Recognition Metrics:                                   │
│  - TAR@FAR (True Accept Rate at Fixed False Accept Rate)     │
│  - EER (Equal Error Rate: where FAR = FRR)                   │
│  - AUROC (Area Under ROC Curve)                               │
│  - Rank-1/5/10 identification rate                            │
│  - d-prime (separability of genuine vs impostor distributions)│
│                                                                 │
│  Knowledge Graph Metrics:                                      │
│  - Entity resolution: pairwise P/R, B-Cubed F1               │
│  - Relationship precision (exact + fuzzy match)              │
│  - Completeness: schema, property, population, interlinking  │
│                                                                 │
│  Correlation Analysis:                                         │
│  - OCR confidence vs CER (should be inversely correlated)     │
│  - NER F1 vs document type (some types harder than others)   │
│  - Face embedding distance vs human agreement                │
│  - Entity co-occurrence frequency vs relationship strength   │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│  PHASE 6: DEPLOYMENT                                            │
├─────────────────────────────────────────────────────────────────┤
│  Outputs:                                                       │
│  - SQLite database with FTS5 full-text search                 │
│  - Knowledge graph (GEXF for Gephi, JSON for programmatic)   │
│  - Entity registry (person → documents → relationships)      │
│  - Facial recognition database (face → identity → docs)      │
│  - Timeline reconstruction (chronological events)            │
│  - Financial flow analysis (shell companies, transfers)      │
│  - Visualization dashboards (graph, timeline, geographic)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Model

### Entity Types

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class EntityType(Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    SHELL_COMPANY = "shell_company"
    PROPERTY = "property"
    AIRCRAFT = "aircraft"
    DATE = "date"
    FINANCIAL_AMOUNT = "financial_amount"
    CASE_NUMBER = "case_number"
    BATES_NUMBER = "bates_number"
    FLIGHT_ID = "flight_id"

class RelationshipType(Enum):
    TRAVELED_WITH = "traveled_with"
    ASSOCIATED_WITH = "associated_with"
    COMMUNICATED_WITH = "communicated_with"
    OWNED_BY = "owned_by"
    EMPLOYED_BY = "employed_by"
    REPRESENTED_BY = "represented_by"
    VICTIM_OF = "victim_of"
    CO_OCCURS_WITH = "co_occurs_with"
    LOCATED_IN = "located_in"
    TRANSFERRED_TO = "transferred_to"

class DocumentType(Enum):
    COURT_FILING = "court_filing"
    DEPOSITION = "deposition"
    CORRESPONDENCE = "correspondence"
    FINANCIAL_RECORD = "financial_record"
    FLIGHT_LOG = "flight_log"
    PHOTOGRAPH = "photograph"
    PROPERTY_RECORD = "property_record"
    MEDIA_TRANSCRIPT = "media_transcript"
    OTHER = "other"
```

### Core Data Structures

```python
@dataclass
class Document:
    """A single document (PDF page or logical document unit)."""
    efta_number: str              # "EFTA00000001"
    dataset_id: int               # 1-12
    file_name: str                # "EFTA00000001.pdf"
    file_type: str                # "pdf", "image", "audio", "video"
    page_count: int = 1
    ocr_text: Optional[str] = None
    ocr_confidence: float = 0.0   # 0.0-1.0
    document_type: Optional[DocumentType] = None
    classification_confidence: float = 0.0
    redaction_count: int = 0
    source_url: str = ""
    sha256_hash: str = ""
    file_size_bytes: int = 0
    created_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Entity:
    """A named entity extracted from documents."""
    id: str                       # unique identifier
    name: str                     # canonical name
    entity_type: EntityType
    aliases: List[str] = field(default_factory=list)
    mention_count: int = 0        # number of documents mentioning this entity
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    confidence: float = 0.0       # extraction confidence
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Source tracking
    source_documents: List[str] = field(default_factory=list)  # EFTA numbers
    source_pages: List[int] = field(default_factory=list)

@dataclass
class Relationship:
    """A relationship between two entities."""
    id: str                       # unique identifier
    source_entity_id: str         # entity.id
    target_entity_id: str         # entity.id
    relationship_type: RelationshipType
    weight: float = 1.0           # strength / frequency
    confidence: float = 0.0       # extraction confidence
    context: str = ""             # text context where relationship was found
    source_document: str = ""     # EFTA number
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FaceDetection:
    """A face detected in an image."""
    id: str                       # unique identifier
    source_document: str          # EFTA number
    source_page: int
    bounding_box: tuple           # (x1, y1, x2, y2)
    embedding: Optional[list] = None  # 512-D ArcFace vector
    identity_label: Optional[str] = None  # matched person name
    confidence: float = 0.0       # detection confidence
    similarity_score: float = 0.0 # match confidence
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Transcription:
    """Audio/video transcription result."""
    source_file: str
    duration_seconds: float
    text: str
    segments: List[Dict] = field(default_factory=list)  # {start, end, text, speaker}
    language: str = "en"
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Redaction:
    """A detected redaction in a document."""
    document_id: str              # EFTA number
    page_number: int
    bbox: tuple                   # (x1, y1, x2, y2) of redacted region
    redaction_type: str           # "proper", "improper", "partial"
    recovered_text: Optional[str] = None  # if recoverable
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## Analysis Stack

### Layer 1: Download & Storage

| Tool | Purpose | GPU? | Install |
|------|---------|------|---------|
| aria2c | Parallel HTTP downloads | No | `apt install aria2` |
| Playwright | DOJ age-gate bypass | No | `pip install playwright` |
| huggingface_hub | HF dataset download | No | `pip install huggingface_hub` |
| SQLite | Primary database | No | Built-in Python |
| PyArrow | Parquet processing | No | `pip install pyarrow` |

### Layer 2: OCR & Text Extraction

| Tool | Purpose | GPU? | VRAM | Accuracy |
|------|---------|------|------|----------|
| PyMuPDF (fitz) | Text-layer extraction | No | - | ~99% (if text exists) |
| Surya | GPU OCR (scanned pages) | Yes | 4-8GB | ~97-99% |
| Docling | IBM fallback OCR | No | - | ~95-97% |
| jiwer | CER/WER measurement | No | - | Reference |
| python-Levenshtein | Edit distance | No | - | Reference |

### Layer 3: NLP & Entity Extraction

| Tool | Purpose | GPU? | VRAM | Install |
|------|---------|------|------|---------|
| spaCy (en_core_web_trf) | NER (transformer) | Yes | 2-4GB | `pip install spacy` |
| GLiNER | Zero-shot NER | No | - | `pip install gliner` |
| rapidfuzz | Fuzzy name matching | No | - | `pip install rapidfuzz` |
| nervaluate | NER evaluation | No | - | `pip install nervaluate` |
| seqeval | Sequence labeling eval | No | - | `pip install seqeval` |

### Layer 4: Facial Recognition

| Tool | Purpose | GPU? | VRAM | Accuracy (LFW) | Install |
|------|---------|------|------|-----------------|---------|
| **InsightFace** | Face detection + embedding | Yes (ONNX) | 500MB-1.5GB | **99.83%** | `pip install insightface onnxruntime-gpu` |
| DeepFace | Multi-model wrapper | Partial | 500MB-2GB | 96.7-98.4% | `pip install deepface` |
| OpenCV (headless) | Image I/O, preprocessing | No | - | - | `pip install opencv-python-headless` |
| sklearn | Clustering, metrics | No | - | - | `pip install scikit-learn` |

**Why InsightFace:**
- Highest accuracy (99.83% LFW)
- Runs via ONNX Runtime (no PyTorch needed — avoids Kepler issues)
- 512-D ArcFace embeddings
- Works on CUDA 11.4 with Tesla K80

### Layer 5: Transcription

| Tool | Purpose | GPU? | VRAM | Install |
|------|---------|------|------|---------|
| faster-whisper | Speech-to-text | Yes | 4-8GB | `pip install faster-whisper` |
| pyannote-audio | Speaker diarization | Yes | 2-4GB | `pip install pyannote.audio` |

### Layer 6: Knowledge Graph

| Tool | Purpose | GPU? | Install |
|------|---------|------|---------|
| SQLite + FTS5 | Graph storage + search | No | Built-in |
| NetworkX | Graph analysis | No | `pip install networkx` |
| pyvis | Interactive visualization | No | `pip install pyvis` |
| Gephi | Desktop graph visualization | No | Desktop app |

### Layer 7: Embeddings & Classification

| Tool | Purpose | GPU? | VRAM | Install |
|------|---------|------|------|---------|
| sentence-transformers | Embedding generation | Yes | 2-4GB | `pip install sentence-transformers` |
| BART-large-mnli | Zero-shot classification | Yes | 2-4GB | Via transformers |

### Layer 8: Evaluation & Metrics

| Tool | Purpose | Install |
|------|---------|---------|
| sklearn | ROC/AUC, clustering metrics | `pip install scikit-learn` |
| scipy | Statistical tests, interpolation | `pip install scipy` |
| jiwer | OCR evaluation (CER, WER) | `pip install jiwer` |
| nervaluate | NER evaluation | `pip install nervaluate` |
| snorkel | Weak supervision | `pip install snorkel` |
| matplotlib | Metric visualization | `pip install matplotlib` |
| seaborn | Statistical plots | `pip install seaborn` |

---

## GPU Allocation Strategy

```
Tesla K80 (0) — 12GB VRAM
├── InsightFace (face detection + embedding): ~1.5GB
├── Surya OCR (batch processing): ~4-8GB
└── Remaining: ~3-6GB buffer

Tesla K80 (1) — 12GB VRAM
├── faster-whisper (transcription): ~4-8GB
├── spaCy transformer NER: ~2-4GB
└── Remaining: ~0-6GB buffer

Tesla K40m (2) — 11GB VRAM
├── sentence-transformers (embeddings): ~2-4GB
├── BART classification: ~2-4GB
└── Remaining: ~3-7GB buffer
```

---

## Processing Strategy

### Parallel Execution Plan

```
Phase 1: Download (all CPUs + network)
├── aria2c CDN: 8 instances × 10 connections = 80 concurrent HTTP
├── HF parquet: 1 aria2c instance × 8 connections
└── Expected: 2-4 hours

Phase 2: OCR (GPU-bound)
├── Worker 1 (K80-0): DS9, DS10 (largest datasets)
├── Worker 2 (K80-1): DS8, DS11, DS12
├── CPU fallback: DS1-7 (small, fast)
└── Expected: 4-8 hours (with HF parquet, OCR is optional)

Phase 3: NER + Classification (GPU + CPU)
├── GPU Worker (K80-1): spaCy transformer NER
├── CPU Workers (4x): GLiNER zero-shot, regex patterns
├── GPU Worker (K40m): BART classification
└── Expected: 2-4 hours

Phase 4: Facial Recognition (GPU-bound)
├── Worker (K80-0): InsightFace batch processing
├── Process all 38,955 images from image_analysis.db
├── Generate 512-D embeddings per face
├── Cluster by identity (DBSCAN + cosine similarity)
└── Expected: 1-2 hours

Phase 5: Knowledge Graph Building
├── Entity resolution (rapidfuzz name matching)
├── Relationship extraction (co-occurrence, patterns)
├── Graph construction (NetworkX → SQLite + GEXF)
└── Expected: 1-2 hours

Phase 6: Evaluation & Validation
├── OCR: CER/WER on sampled pages (if ground truth available)
├── NER: Precision/Recall/F1 on entity extraction
├── Face: EER/AUROC on clustering quality
├── KG: Completeness metrics across all dimensions
└── Expected: 30 minutes
```

---

## Accuracy Measurement Approach

### OCR Accuracy (CER/WER)
- **Challenge**: No official ground truth exists for DOJ documents
- **Approach**: 
  1. Sample 100 pages across document types
  2. Manual ground truth creation (2 independent transcribers)
  3. Compute inter-annotator agreement (Cohen's Kappa)
  4. Calculate CER/WER against reconciled ground truth
  5. Weighted Levenshtein for OCR-specific confusions (O/0, l/1)
- **Target**: CER < 5%, WER < 10%

### NER Accuracy (F1)
- **Challenge**: No labeled NER corpus exists for Epstein documents
- **Approach**:
  1. Create small labeled sample (50 documents, ~500 entities)
  2. Evaluate under Strict, Exact, Partial, and Type schemas
  3. Weak supervision for remainder (coverage, conflict metrics)
  4. Cross-validate with known entities from knowledge_graph.db
- **Target**: Strict F1 > 0.85, Partial F1 > 0.92

### Facial Recognition Accuracy (EER/AUROC)
- **Challenge**: No labeled face identities in the dataset
- **Approach**:
  1. Generate embeddings for all detected faces
  2. Cluster using DBSCAN (cosine similarity threshold)
  3. Evaluate cluster purity (intra-cluster vs inter-cluster distance)
  4. Compute d-prime (separability metric)
  5. Manual verification on top clusters
- **Target**: EER < 5%, d-prime > 3.0

### Knowledge Graph Accuracy
- **Challenge**: No complete ground truth relationship graph
- **Approach**:
  1. Cross-reference with known relationships from research literature
  2. Entity resolution accuracy against person_registry.json
  3. Relationship precision on high-confidence edges (weight > 5)
  4. Completeness audit across 7 dimensions (schema, property, etc.)
- **Target**: Entity resolution F1 > 0.90, Relationship precision > 0.80

### Correlation Analysis
- **OCR confidence vs CER**: Expect negative correlation (higher confidence → lower error)
- **NER F1 vs document type**: Court filings should have higher F1 than depositions
- **Face cluster size vs confidence**: Larger clusters should have higher avg confidence
- **Entity co-occurrence vs relationship weight**: Positive correlation expected

---

## Tools Summary

### Core Stack (All Free)
```
Python 3.12
├── aria2c (downloads)
├── Playwright (web scraping)
├── PyMuPDF (PDF processing)
├── spaCy (NLP/NER)
├── GLiNER (zero-shot NER)
├── InsightFace + ONNX Runtime (face recognition)
├── faster-whisper (transcription)
├── sentence-transformers (embeddings)
├── scikit-learn (metrics, clustering)
├── NetworkX (graph analysis)
├── SQLite (storage)
├── PyArrow (parquet)
├── Rich (terminal UI)
├── jiwer (OCR evaluation)
├── nervaluate (NER evaluation)
├── rapidfuzz (fuzzy matching)
├── scipy (statistics)
├── matplotlib (visualization)
└── snorkel (weak supervision)
```

### GPU Requirements
- CUDA 11.4 compatible
- 12GB VRAM minimum per GPU
- ONNX Runtime GPU preferred (avoids PyTorch Kepler issues)
- Batch processing for efficiency

### Storage Requirements
- Raw PDFs: ~218GB
- HF Parquet: ~317GB
- Pre-built DBs: ~8GB
- Processed output: ~50GB estimated
- **Total: ~600GB** (2.3TB available)

---

## Community Analysis Techniques (From External Projects)

### Louvain Community Detection

Used by multiple projects to find distinct social circles in the Epstein network:
- Shereshevsky: Found 5 communities in 25,800 documents
- Tim Smith: Found 12 communities with 714 entities, 8,604 relationships
- Academic research: Structural analysis of broker roles

```python
from networkx.algorithms.community import louvain_communities
communities = louvain_communities(G, resolution=1.0)
```

### Six Centrality Metrics

Tim Smith's approach (Graph-Aware RAG paper):
1. **Degree Centrality** — Number of direct connections
2. **Betweenness Centrality** — How often this node lies on shortest paths (identifies brokers)
3. **Closeness Centrality** — Average distance to all other nodes
4. **Eigenvector Centrality** — Influence (connected to other influential nodes)
5. **PageRank** — Importance ranking (Google's algorithm)
6. **Clustering Coefficient** — How connected are this node's neighbors to each other

```python
import networkx as nx
degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
pagerank = nx.pagerank(G)
clustering = nx.clustering(G)
```

### Graph-Aware RAG

Tim Smith's innovative retrieval approach:
1. Detect entities in query via FTS5 keyword search
2. Walk the knowledge graph outward from detected entities
3. Follow weighted edges to discover intermediary entities
4. Re-rank results using vector cosine similarity
5. Entire platform ships as single 75MB SQLite file

### Congressional Document Scoring

From `congressional_scorer.py`:
```
REVEAL_SCORE = estimated_redacted_names × crime_severity × novelty_factor
```

- Layer 1A: Crime keywords (3 severity tiers with weights ×3/×2/×1)
- Layer 1B: Redaction density per page
- Layer 1C: Name entity density
- Name-proximity patterns: redactions near "Mr. [", "trafficked to", "raped by", etc.

### Person Integrity Auditor (5-Phase)

From `build_person_registry.py` and Epstein-Pipeline:
1. **Dedup**: rapidfuzz name similarity + alias cross-check
2. **Wikidata**: Cross-reference occupation, dates, nationality
3. **Fact-Check**: Decompose bios into atomic claims, verify against corpus
4. **Coherence**: Sample linked docs, detect merged identities
5. **Score**: Composite severity (0-100), create leads for review

### DOJ Document Removal Monitoring

Epstein Exposed's automated approach:
- Weekly comparison against DOJ website
- Detected 892 removed documents
- GitHub Actions CI for automation
- Status codes: LIVE (200+PDF), REMOVED (404), AGE_GATE (200+HTML), RATE_LIMITED (401), FORBIDDEN (403)

### External Cross-References (Available via Pipeline)

| Source | Dataset | Records | Pipeline Command |
|--------|---------|---------|-----------------|
| OpenSanctions | OFAC SDN, EU, UN | Variable | `check-sanctions` |
| ICIJ Offshore Leaks | Panama/Paradise/Pandora Papers | 810K entities | `check-icij` |
| FEC Donations | Political contributions | 55K+ | `check-fec` |
| IRS 990 | Nonprofit officers/grants | Variable | `check-nonprofits` |
| Wikidata | Person fact-checking | Free API | Built into auditor |
