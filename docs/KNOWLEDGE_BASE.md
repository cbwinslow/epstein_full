# Knowledge Base — Epstein Files Analysis

> Compiled from upstream repos, external research sites, and community projects.
> Sources: Epstein-Pipeline, Epstein-research-data, epsteinexposed.com, epsteinweb.org,
> epsteinwiki.com, jmail.world, epsteinsinbox.com, epstein-data.com, and community projects.

---

## 1. Processing Pipelines (From Existing Projects)

### Epstein-Pipeline (stonesalltheway1) — 10-Step Pipeline

```
1. Download    DOJ, Kaggle, HuggingFace, Archive.org
2. OCR         PyMuPDF → Surya → olmOCR 2 → Docling (fallback chain)
3. Entities    spaCy NER + GLiNER + regex patterns
4. Person Link rapidfuzz fuzzy matching → canonical person IDs
5. Classify    BART-large-mnli zero-shot (12 categories)
6. Dedup       SHA-256 → MinHash/LSH → Semantic similarity
7. Chunk       Semantic paragraph-aware splitting (512 tokens)
8. Embed       nomic-embed-text-v2-moe (768-dim)
9. Validate    Schema checks, cross-reference integrity
10. Export     JSON, CSV, SQLite, Neon Postgres
```

### Key Configuration Values

| Parameter | Value | Notes |
|-----------|-------|-------|
| OCR confidence threshold | 0.7 | Pages below this are flagged |
| NER confidence threshold | 0.5 | spaCy/GLiNER minimum |
| Dedup title fuzzy match | 0.90 | rapidfuzz threshold |
| Dedup Jaccard (MinHash) | 0.80 | Near-duplicate detection |
| Dedup semantic cosine | 0.95 | Embedding similarity |
| MinHash shingle size | 5 | n-gram size |
| MinHash permutations | 128 | Hash function count |
| Chunk size | 3200 chars (~800 tokens) | With 800 char overlap |
| Classifier threshold | 0.6 | BART confidence |
| Embedding dimensions | 768 (or 256 Matryoshka) | nomic-embed-text-v2-moe |

### Three-Pass Deduplication

1. **SHA-256 hash** — catches exact duplicates (O(1) per doc)
2. **MinHash/LSH** — Locality-sensitive hashing finds near-duplicates (O(n))
3. **Semantic embeddings** — Cosine similarity catches OCR-variant duplicates

### Person-Entity Match Confidence Scores

| Match Type | Confidence |
|------------|-----------|
| Exact canonical name | 1.00 |
| Exact alias | 0.95 |
| Fuzzy > 95% | 0.85 |
| Fuzzy > 90% | 0.75 |
| Substring | 0.60 |

### Document Classification Categories (12 types)

legal, financial, travel, communications, investigation, media, government, personal, medical, property, corporate, other

---

## 2. Analysis Techniques (From All Sources)

### Knowledge Graph Construction

**Three edge types from three data sources:**
1. **Co-occurrence edges** — Entities in same document
2. **Co-passenger edges** — From flight log data
3. **Correspondence edges** — Email sender/recipient pairs

**Additional edge types from research-data tools:**
- `traveled_with` (1,449 edges) — Flight co-occurrence
- `associated_with` (589 edges) — General association
- `communicated_with` (215 edges) — Email communication
- `owned_by` (23 edges) — Property/entity ownership
- `victim_of` (13 edges) — Victim-perpetrator links
- `employed_by` (7 edges) — Employment relationships
- `paid_by` (1 edge) — Financial transactions
- `recruited_by` (1 edge) — Recruitment

### Graph Algorithms Used Across Projects

| Algorithm | Purpose | Tool |
|-----------|---------|------|
| Louvain Community Detection | Find distinct social circles | NetworkX |
| Degree Centrality | Most connected individuals | NetworkX |
| Betweenness Centrality | Bridge nodes / brokers | NetworkX |
| Eigenvector Centrality | Influence measurement | NetworkX |
| PageRank | Importance ranking | NetworkX |
| Shortest Path (BFS/Dijkstra) | Degrees of separation | NetworkX |
| Force-directed layout | Visualization | D3.js, Sigma.js, vis.js |

**Tim Smith's Graph-Aware RAG approach:**
- 714 entities, 8,604 weighted relationships, 12 Louvain communities
- Six centrality metrics per entity
- Graph-walk from detected entities following weighted edges
- Hybrid: FTS5 keyword → vector cosine re-ranking
- Entire platform as single 75MB SQLite file

**Alexander Shereshevsky's Community Detection:**
- Built from 25,800 documents
- Louvain found 5 distinct social circles
- Focus: "Who knew each other through him" (structural analysis)

### Redaction Analysis

**Three classifications:**
- `proper` — No text found under redaction
- `bad_overlay` — Garbled OCR of black bars (false positive for DS9-11)
- `recoverable` — Text extractable from under redaction

**Detection thresholds (redaction_detector_v2.py):**
- `BLACK_PIXEL_THRESHOLD`: 30
- `MIN_RECT_WIDTH_PX`: 30
- `MIN_RECT_HEIGHT_PX`: 5
- `ROW_BLACK_RATIO`: 0.15
- `COL_BLACK_RATIO`: 0.5

**Important caveat**: For DS9-11, DOJ files are scanned with redaction bars baked into JPEG pixels. The "recovered" text is garbled OCR of black bars, NOT original content.

### Document Scoring (Congressional Priority)

```
REVEAL_SCORE = estimated_redacted_names × crime_severity × novelty_factor
```

Severity tiers:
- Severe (×3): rape, CSAM, child trafficking, minor, underage, molest
- Moderate (×2): assault, trafficking, prostitution, abuse, victim
- Financial (×1): wire transfer, shell company, money laundering, obstruction, settlement

### Person Integrity Auditor (5-phase data quality)

1. **Dedup** — rapidfuzz name similarity + alias cross-check
2. **Wikidata** — Cross-reference occupation, dates, nationality
3. **Fact-Check** — Decompose bios into atomic claims, verify against 2M+ docs
4. **Coherence** — Sample linked docs, detect merged identities
5. **Score** — Composite severity (0-100), create leads for review

### External Data Cross-References

| Source | What It Provides | API |
|--------|-----------------|-----|
| OpenSanctions | OFAC SDN, EU, UN sanctions, PEP registries | API key |
| ICIJ Offshore Leaks | Panama Papers, Paradise Papers, Pandora Papers (810K+ entities) | CSV files |
| FEC | Political donation records (55K+) | Free API |
| IRS 990 | Nonprofit officer names, grants | ProPublica API (free) |
| Wikidata | Person fact-checking, headshot images | Free |

---

## 3. External Project Architectures

### Epstein Exposed (epsteinexposed.com)

**Scale**: 2.15M documents, 1,568 persons, 3,615 flights, 51,254 auto-generated connections

**Stack**: Next.js + Prisma + Neon PostgreSQL + HNSW vector index (2.67M embeddings)

**Key innovations:**
1. **Connection auto-generation** — Algorithm surfaced 51K relationships automatically
2. **DOJ removal monitoring** — Weekly automated comparison, detected 892 removed docs
3. **MCP Server** — 9 tools, 5 resources, 3 prompts for AI assistant integration
4. **Financial forensics** — Sankey diagrams for $6.3B in traced flows
5. **Codename decoder** — 63 pseudonyms decoded from 2.77M pages
6. **Forensic calendar** — 5-tab tool for Epstein's schedule documents
7. **iMessage viewer** — 4,509 text messages with virtual scrolling
8. **Anti-abuse** — 6-layer system (honeypot traps, behavioral scoring, fingerprinting)

**API**: 28 REST endpoints + MCP server

### Jmail.world

**Built in 5 hours**, reached 18.4M visits. Gmail-cloned interface for browsing Epstein emails.

**Email accounts indexed**: 7,499 + 2,228 + 4,648 = 14,375 emails

**Expanded into**: JPhotos, JFlights, Jamazon, Jacebook, Jeddit, Jotify, JTube, VR Videos, Jemini AI

**Lesson**: Familiar UI paradigms dramatically lower the barrier. One data source (emails) can be re-skinned into multiple interfaces.

### EpsteinWiki.com — OSINT Resource Directory

Catalogs 50+ tools/databases organized by category:
- OSINT databases (12+)
- Communication records (5+)
- Photographic evidence (3+)
- US government databases (4+)
- Investigation tools (10+)
- Evidence labs (5+)

### Epstein Emails Knowledge Graph (kev-hu/epstein-emails)

**Tech**: Python, Neo4j 5.x, Graphiti (Zep), OpenAI GPT, Pydantic, NetworkX, Jupyter

**Approach**:
- Custom Pydantic entity schemas: Person, Organization, Location, Event, Document
- Custom relationships: REPRESENTS, ALLEGED_VICTIM_OF, INVESTIGATED_BY, EMPLOYED_BY
- Temporal episodes model for time-aware graph queries
- Date normalization across 20+ formats including multi-language (French, Slovak)
- LLM-powered entity extraction with configurable provider

### Academic Research (Laszlo Pokorny dissertation)

**Methodology**: Social Network Analysis (SNA)
- Epstein network: n = 84 nodes
- Metrics: Degree Centrality, Eigenvector Centrality, Betweenness Centrality
- Community Detection results
- Structural analysis of high-betweenness broker roles
- Recommendations for law enforcement disruption strategies

---

## 4. Data Formats (From Pipeline)

### Core Document Model

```python
Document:
    id: str
    title: str
    date: str | None              # YYYY-MM-DD
    source: DocumentSource        # 20+ source types
    category: DocumentCategory    # 12 categories
    summary: str | None
    personIds: list[str]
    tags: list[str]
    pdfUrl: str | None
    pageCount: int | None
    batesRange: str | None        # "EFTA00039025-EFTA00039030"
    ocrText: str | None
    verificationStatus: verified | unverified | disputed | redacted
```

### Person Registry Format

```json
{
    "name": "Jeffrey Epstein",
    "slug": "jeffrey-epstein",
    "aliases": ["JE"],
    "category": "key-figure",
    "description": "Convicted sex trafficker",
    "search_terms": ["Jeffrey Epstein"],
    "sources": ["epstein-pipeline", "la-rana-chicana"],
    "metadata": {"occupation": "financier", "legal_status": "deceased"}
}
```

### Three Bates Numbering Systems

1. **EFTA########** — Public DOJ identifier
2. **SDNY_GM_########** — SDNY prosecution internal
3. **DB-SDNY-########** — Deutsche Bank internal production

### Person Categories

perpetrator, enabler, victim, associate, business, celebrity, academic, politician, legal, socialite, royalty, intelligence, staff, mentioned, other

---

## 5. Upstream Tools Available

### research-data/tools/ (38 scripts)

| Tool | Purpose |
|------|---------|
| `build_knowledge_graph.py` | Entity relationship graph from evidence DB |
| `build_person_registry.py` | Unified person registry from 9 sources |
| `person_search.py` | FTS5 cross-reference with co-occurrence |
| `redaction_detector_v2.py` | Spatial redaction analysis |
| `transcribe_media.py` | GPU transcription (faster-whisper large-v3) |
| `document_classifier.py` | 14-type rule-based classification |
| `congressional_scorer.py` | Priority scoring for congressional reading |
| `extract_subpoena_riders.py` | Grand Jury subpoena catalog |
| `search_gov_officials.py` | Government official search |
| `search_judicial.py` | Federal judge search |
| `mirror_coverage.py` | CDN mirror coverage map |
| `populate_evidence_db.py` | Populate evidence DB from multiple sources |
| `find_missing_efta.py` | Gap detection across EFTA numbering |

### Pipeline CLI Commands

```
download doj/kaggle/huggingface/archive
ocr <dir> -o <out> --backend surya
extract-entities <dir>
classify --input-dir <out>
dedup <out> --mode all
embed <out> -o <emb/>
build-graph <out> --format both
export json/csv/sqlite/neon
analyze-redactions <pdfs>
extract-images <pdfs> --describe
transcribe <media> --model large-v3
check-sanctions / check-icij / check-fec / check-nonprofits
validate <out> / stats <out> / audit-persons
import sea-doughnut --data-dir <path>
sync-site --site-dir <path>
```

---

## 6. What We Can Learn & Apply

### Techniques to Adopt Immediately

1. **Louvain community detection** — Run on our 606-entity knowledge graph
2. **Six centrality metrics** — degree, betweenness, closeness, eigenvector, PageRank, clustering coefficient
3. **Graph-Aware RAG** — Walk graph from entities in queries, not just vector similarity
4. **Person integrity auditor** — 5-phase data quality pipeline
5. **Congressional scorer** — Multi-layer document prioritization
6. **DOJ removal monitoring** — Weekly automated comparison

### Data Sources to Acquire

| Source | Size | Value |
|--------|------|-------|
| ICIJ Offshore Leaks | 810K entities | Shell company cross-reference |
| FEC donations | 55K records | Political connection mapping |
| IRS 990 data | Variable | Nonprofit officer/grant mapping |
| HuggingFace datasets | 20K+25.8K docs | Additional document collections |
| DOJ alteration analysis | 212,730 changes | Track document modifications |

### Architectural Patterns to Consider

1. **Datasette** — Quick visual interface over SQLite (used by epstein-data.com)
2. **Sigma.js WebGL** — Network visualization at scale (Epstein Exposed switched from D3 SVG)
3. **MCP Server** — Make database queryable by AI assistants
4. **HNSW vector index** — For semantic search at scale (Epstein Exposed: 2.67M embeddings)
5. **Single-file deployment** — 75MB SQLite containing entire platform (Tim Smith's approach)
6. **DeepSeek** — Cost-effective large-scale document analysis ($1 for hundreds of docs)
7. **Reducto** — PDF text extraction (used by Jmail)

### Key Insights

1. **No single OCR engine handles all types** → Use fallback chain
2. **Three dedup passes are necessary** → Hash + MinHash + Semantic
3. **Person registry is critical** → 1,538+ known persons enable consistent cross-referencing
4. **DS9-11 redaction recovery is false positive** → Garbled OCR, not hidden content
5. **Familiar UI paradigms matter** → Gmail clone got 18.4M visits
6. **Speed of execution matters** → 5 hours to build Jmail, 40 days for Epstein Exposed
7. **Community detection reveals structure** → Louvain finds distinct social circles
8. **Graph centrality identifies brokers** → Betweenness centrality finds bridge nodes
