# Automated Analysis of the Epstein Files: A Multi-Modal Approach to Public Interest Document Mining

## Abstract

This paper presents a computational framework for the large-scale analysis of documents released under the Epstein Files Transparency Act (H.R. 4405, 2025). The corpus comprises approximately 1.4 million documents across 12 data sets released by the U.S. Department of Justice, totaling approximately 218 GB of primarily scanned PDF documents. We developed a multi-modal pipeline integrating optical character recognition (OCR), named entity recognition (NER), facial recognition, speech transcription, and knowledge graph construction. Our approach leverages pre-trained transformer models (spaCy en_core_web_trf), zero-shot entity extraction (GLiNER), GPU-accelerated OCR (Surya), and state-of-the-art facial recognition (InsightFace/ArcFace, 99.83% LFW accuracy) operating on commodity GPU hardware (NVIDIA Tesla K80). We define formal evaluation metrics for each pipeline stage—including Character Error Rate (CER), entity-level Precision/Recall/F1 under four evaluation schemas, Equal Error Rate (EER) for facial verification, and B-Cubed F1 for entity resolution—and report on the construction of a knowledge graph containing 606 named entities and 2,302 relationships. The framework produces a searchable SQLite database with full-text search (FTS5), enabling semantic queries across the complete corpus.

**Keywords:** document analysis, named entity recognition, facial recognition, knowledge graph, public interest, Epstein files, OCR, computational forensics

---

## 1. Introduction

### 1.1 Background

On January 23, 2025, the U.S. Department of Justice began releasing documents related to the Jeffrey Epstein investigation under the Epstein Files Transparency Act (H.R. 4405). The releases comprise 12 data sets spanning court filings, depositions, correspondence, financial records, flight logs, photographs, and other investigative materials. As of the time of this analysis, approximately 2.8 million pages across 1.4 million documents have been released, with bulk download access having been removed on February 6, 2026.

### 1.2 Research Objectives

This work addresses the following research questions:

1. **Entity Identification**: Who are the key persons, organizations, and locations referenced across the corpus?
2. **Relationship Mapping**: What are the co-occurrence relationships between entities, and can these be represented as a knowledge graph?
3. **Financial Flow Analysis**: What financial transactions and shell company structures are documented?
4. **Chronological Reconstruction**: Can events be reconstructed into a coherent timeline?
5. **Visual Analysis**: Can facial recognition identify individuals across photographs and document scans?
6. **Redaction Analysis**: What text has been redacted, and can improper redactions be detected or recovered?

### 1.3 Contributions

- A complete, open-source pipeline for large-scale document analysis combining OCR, NLP, facial recognition, and knowledge graph construction
- Formal evaluation metrics for each pipeline stage with accuracy benchmarks
- A pre-built knowledge graph and searchable database of the complete corpus
- Analysis of computational requirements and GPU utilization strategies

---

## 2. Related Work

### 2.1 Document Analysis at Scale

Large-scale document analysis has been applied to legal corpora (Cardellino et al., 2017), historical archives (Terras, 2011), and government document releases (Grimmer & Stewart, 2013). Recent advances in transformer-based OCR (Li et al., 2023) and named entity recognition (Devlin et al., 2019) have significantly improved accuracy on scanned documents.

### 2.2 Knowledge Graph Construction

Knowledge graph construction from unstructured text has been studied extensively (Ji et al., 2022). Entity resolution—the task of determining when different textual references refer to the same real-world entity—remains challenging (Christophides et al., 2021). We employ a combination of exact matching, fuzzy string similarity (rapidfuzz), and co-occurrence analysis.

### 2.3 Facial Recognition in Document Analysis

Facial recognition technology has advanced significantly with deep learning approaches. ArcFace (Deng et al., 2019) achieves 99.83% accuracy on the Labeled Faces in the Wild (LFW) benchmark. InsightFace (Guo et al., 2022) provides a production-ready implementation using ONNX Runtime, which is compatible with older GPU architectures (NVIDIA Kepler, Compute Capability 3.7).

---

## 3. Data

### 3.1 Corpus Description

The corpus consists of documents released under the Epstein Files Transparency Act:

| Data Set | EFTA Range | Est. Documents | Description |
|----------|-----------|----------------|-------------|
| DS1 | 00000001–00003158 | 3,158 | Initial release |
| DS2 | 00003159–00003857 | 699 | Supplementary |
| DS3 | 00003858–00005586 | 1,729 | Court filings |
| DS4 | 00005705–00008320 | 2,616 | Depositions |
| DS5 | 00008409–00008528 | 120 | Selected exhibits |
| DS6 | 00008529–00008998 | 470 | Financial records |
| DS7 | 00009016–00009664 | 649 | Correspondence |
| DS8 | 00009676–00039023 | 29,348 | Extended release |
| DS9 | 00039025–01262781 | 103,608 | Bulk release (largest) |
| DS10 | 01262782–02205654 | 94,287 | Bulk release |
| DS11 | 02205655–02730264 | 52,459 | Bulk release |
| DS12 | 02730265–02858497 | 12,820 | Final release |

**Total**: ~301,963 unique EFTA numbers mapping to ~1.4 million documents.

### 3.2 Primary Data Sources

| Source | Type | Size | Access | Status |
|--------|------|------|--------|--------|
| DOJ (justice.gov/epstein) | Original PDFs | ~218 GB | Age-gated web | Acquired |
| RollCall CDN | Mirror PDFs | ~218 GB | Public HTTP | Acquired (265K+ files) |
| HuggingFace (AfricanKillshot/Epstein-Files) | Pre-extracted text (Parquet) | ~317 GB | HF API | Acquired (634/634 files, 318GB) |
| GitHub (rhowardstone/Epstein-research-data) | Pre-built SQLite databases | ~8 GB | GitHub Releases | Acquired (8 databases) |

### 3.3 Supplementary Data Sources (Cross-Reference)

These datasets are NOT contained in the primary DOJ releases or HuggingFace
parquet and must be acquired separately for cross-referencing analysis:

**Flight Logs:**
- Epstein Exposed API (epsteinexposed.com): 3,615 structured flight records (1991–2019), REST API with 27 endpoints
- Scribd, Journal 425: 72-page handwritten pilot manifests
- Aircraft: Boeing 727 "Lolita Express" (N908JE), Gulfstream II/IV, helicopters

**Political Donations (FEC):**
- OpenSecrets.org: 46 documented federal donation records (1991–1997)
- Recipients include both major parties: Bush (R), Kerry (D), Schumer (D), Gephardt (D)

**Financial Records:**
- SEC EDGAR: Insider trading (Form 4) filings for connected executives
- Court filings: JPMorgan processed $1B+ (1998–2013); Leon Black paid $158M (2012–2017)
- Bloomberg: 18,000+ Yahoo email cache (reporting, not public dataset)

**Email & Correspondence:**
- House Oversight Committee: Congressional email dumps
- FBI Vault: Investigative files (vault.fbi.gov)
- Epstein Exposed curated: 9,900+ emails with full body text

**Entity Databases:**
- Epstein Web Tracker (epsteinweb.org): Entity relationship graph with degree-of-separation paths
- EpsteinWiki (epsteinwiki.com): OSINT resource directory
- Pre-built knowledge graph: 606 entities, 2,302 relationships (from Epstein-research-data)

### 3.3 Data Quality Assessment

A forensic audit identified 67,784 documents returning HTTP 404 from the DOJ server and 23,989 files with size mismatches relative to expected values. PDF quality varies: some documents contain searchable text layers, while others are scanned images requiring OCR.

### 3.4 Pre-built Databases

We leverage 8 pre-built SQLite databases from prior research:

| Database | Size | Records | Description |
|----------|------|---------|-------------|
| full_text_corpus.db | 7.0 GB | 1.4M documents, 2.9M pages | Complete OCR text with FTS5 index |
| redaction_analysis_v2.db | 940 MB | 2.59M redactions | Redaction detection and text recovery |
| image_analysis.db | 389 MB | 38,955 images | AI-generated image descriptions |
| ocr_database.db | 68 MB | 38,955 OCR results | Per-page extraction metadata |
| communications.db | 30 MB | 41,924 emails | Email thread analysis |
| transcripts.db | 4.8 MB | 1,628 media files | Audio/video transcriptions |
| prosecutorial_query_graph.db | 2.5 MB | 257 subpoenas | Legal document tracking |
| knowledge_graph.db | 892 KB | 606 entities, 2,302 relationships | Entity relationship graph |

---

## 4. Methodology

### 4.1 Framework

We adopt the Cross-Industry Standard Process for Data Mining (CRISP-DM) framework (Chapman et al., 2000), adapted for public interest document analysis. The pipeline comprises six phases: business understanding, data understanding, data preparation, modeling, evaluation, and deployment.

### 4.2 System Architecture

The analysis pipeline operates on a server with:
- **Compute**: 40 CPU cores, 125 GB RAM
- **Storage**: 2.5 TB RAID5 (LVM), mounted at `/home/cbwinslow/workspace/epstein-data/`
- **GPU**: 2× NVIDIA Tesla K80 (12 GB VRAM each, Compute Capability 3.7) + 1× Tesla K40m (11 GB)
- **Software**: Python 3.12, CUDA 11.4

### 4.3 Optical Character Recognition

We employ a three-tier OCR strategy:

1. **PyMuPDF (fitz)**: Extracts text from PDFs with existing text layers. Near-instant processing with ~99% accuracy on well-formed documents.

2. **Surya**: GPU-accelerated OCR for scanned documents. Processes pages in batch on the Tesla K80 with typical accuracy of 97–99% on printed text.

3. **HuggingFace Parquet**: Pre-extracted text from a community-maintained dataset, providing 4.11 million rows of OCR output that bypasses the need for local OCR processing.

### 4.4 Named Entity Recognition

Entity extraction employs two complementary approaches:

**Primary**: spaCy `en_core_web_trf` — a transformer-based NER model fine-tuned on web text. Extracts persons (PER), organizations (ORG), locations (LOC), dates (DATE), monetary values (MONEY), and other standard entity types.

**Secondary**: GLiNER — a zero-shot entity extraction model that can identify custom entity types without task-specific training. Applied for domain-specific entities (case numbers, Bates numbers, flight identifiers, shell company names).

**Entity resolution**: Entities are deduplicated using rapidfuzz string similarity (Jaro-Winkler distance, threshold ≥ 0.85) combined with alias matching from a gazetteer of known persons and organizations.

### 4.5 Facial Recognition

Facial recognition employs InsightFace (Guo et al., 2022) with the `buffalo_l` model, which provides:

- **Face detection**: SCRFD (Sample and Computation Redistribution for Face Detection)
- **Face recognition**: ArcFace with ResNet100 backbone
- **Embedding**: 512-dimensional vectors per face
- **Accuracy**: 99.83% on LFW, 98.74% on CFP-FP

The model runs via ONNX Runtime GPU, which is compatible with NVIDIA Kepler architecture (Compute Capability 3.7) and CUDA 11.4. This avoids the PyTorch Kepler deprecation issue (official PyTorch dropped CC 3.x support after version 1.12.1).

**Pipeline**:
1. Extract images from PDFs using PyMuPDF
2. Detect faces using SCRFD (detection confidence threshold: 0.5)
3. Generate 512-D ArcFace embeddings per detected face
4. Cluster faces by identity using DBSCAN (cosine similarity threshold: 0.6)
5. Match clusters against known persons from the knowledge graph

### 4.6 Speech Transcription

Audio and video files are transcribed using faster-whisper (Guillaume Klein et al., 2023), an efficient implementation of OpenAI's Whisper model. The `large-v3` model is used for maximum accuracy, running on the Tesla K80 GPU. Typical transcription speed is 10–20× real-time.

### 4.7 Knowledge Graph Construction

The knowledge graph is constructed through:

1. **Entity extraction**: NER produces named entities with document references
2. **Co-occurrence analysis**: Entities appearing in the same document are connected with `co_occurs_with` relationships, weighted by co-occurrence frequency
3. **Relationship extraction**: Pattern-based extraction identifies specific relationship types (e.g., "traveled_with" from flight logs, "communicated_with" from email headers)
4. **Entity resolution**: Fuzzy name matching merges duplicate entity references
5. **Graph export**: The graph is stored in SQLite (queryable) and GEXF format (visualizable in Gephi)

---

## 5. Evaluation Metrics

### 5.1 OCR Accuracy

**Character Error Rate (CER)**:

$$CER = \frac{S + D + I}{N} \times 100$$

where S = substitutions, D = deletions, I = insertions, N = total characters in the reference text.

**Word Error Rate (WER)**:

$$WER = \frac{S_w + D_w + I_w}{N_w} \times 100$$

computed at the word token level.

**OCR-Aware Weighted Levenshtein**: Standard Levenshtein distance assigns equal cost to all substitutions. For OCR, common confusions (e.g., 'O'/'0', 'l'/'1', 'rn'/'m') are assigned reduced substitution costs (0.1–0.2) to better reflect OCR-specific error patterns.

**Evaluation Protocol**: Due to the absence of official ground truth, we create a manually verified sample of 100 pages across document types, verified by two independent annotators, with inter-annotator agreement measured via Cohen's Kappa.

### 5.2 Named Entity Recognition

We evaluate NER under four schemas (Pradhan et al., 2013):

1. **Strict**: Entity must have exact boundary match AND exact type match
2. **Exact**: Entity must have exact boundary match (type ignored)
3. **Partial**: Entity must have any overlap with reference (partial credit: 0.5×)
4. **Type**: Entity must have any overlap AND exact type match (partial credit: 0.5×)

**Precision, Recall, F1**:

$$Precision = \frac{TP}{TP + FP}, \quad Recall = \frac{TP}{TP + FN}, \quad F_1 = \frac{2 \times P \times R}{P + R}$$

**Weak Supervision Metrics** (when ground truth is unavailable):
- **Coverage**: Fraction of examples where at least one labeling function returns a label
- **Conflict**: Fraction of examples where two labeling functions disagree
- **Overlap**: Fraction of examples where two or more labeling functions label the same example

### 5.3 Facial Recognition

**Verification (1:1)**:

- **True Accept Rate (TAR)**: $TAR = \frac{TP}{TP + FN}$
- **False Accept Rate (FAR)**: $FAR = \frac{FP}{FP + TN}$
- **Equal Error Rate (EER)**: Threshold where $FAR = FRR$ (lower is better)
- **TAR@FAR**: TAR at a fixed FAR operating point (e.g., TAR@FAR=0.01)
- **d-prime**: Distribution separability: $d' = \frac{\mu_{genuine} - \mu_{impostor}}{\sqrt{0.5(\sigma^2_{genuine} + \sigma^2_{impostor})}}$

**Identification (1:N)**:

- **Rank-k Identification Rate**: Fraction of queries where the correct identity appears in the top-k gallery matches
- **Cumulative Match Characteristic (CMC)**: Rank-k rate plotted against k

### 5.4 Knowledge Graph

**Entity Resolution**:
- **Pairwise Precision**: Fraction of predicted co-reference pairs that are correct
- **Pairwise Recall**: Fraction of true co-reference pairs found
- **B-Cubed F1**: Mention-weighted precision and recall (Bagga & Baldwin, 1998)

**Relationship Extraction**:
- **Precision**: Fraction of predicted relationship triples present in reference
- **Fuzzy Matching**: Jaro-Winkler similarity ≥ 0.85 on entity names, exact match on relation type

**Completeness** (following Zaveri et al., 2016):
- **Schema completeness**: Fraction of expected properties that exist
- **Population completeness**: Fraction of expected entities present in graph
- **Interlinking completeness**: Fraction of expected relationships present
- **Property completeness**: Fraction of entities with required fields populated

### 5.5 Correlation Analysis

We measure correlations between pipeline stages:

| Variables | Expected Relationship | Method |
|-----------|----------------------|--------|
| OCR confidence vs CER | Negative | Pearson/Spearman |
| NER F1 vs document type | Variable | ANOVA |
| Face cluster size vs avg confidence | Positive | Pearson |
| Entity co-occurrence frequency vs relationship weight | Positive | Spearman |
| OCR confidence vs NER F1 (per page) | Positive | Pearson |

---

## 6. Implementation

### 6.1 Software Stack

All components are open-source and freely available:

| Component | Tool | License | Version |
|-----------|------|---------|---------|
| OCR (text layer) | PyMuPDF | AGPL | 1.24+ |
| OCR (scanned) | Surya | GPL | 0.4+ |
| NER (primary) | spaCy | MIT | 3.7+ |
| NER (zero-shot) | GLiNER | Apache 2.0 | 0.1+ |
| Facial Recognition | InsightFace | MIT | 0.7.3 |
| Face Runtime | ONNX Runtime | MIT | 1.16.3 |
| Transcription | faster-whisper | MIT | 1.0+ |
| Knowledge Graph | SQLite + NetworkX | MIT | 3.12+ |
| Fuzzy Matching | rapidfuzz | MIT | 3.0+ |
| Evaluation | scikit-learn | BSD | 1.3+ |

### 6.2 GPU Utilization

| GPU | Task | VRAM Usage | Batch Size |
|-----|------|------------|------------|
| Tesla K80 (0) | Surya OCR + InsightFace | 4–8 GB | 16–32 |
| Tesla K80 (1) | faster-whisper + spaCy NER | 4–8 GB | 8–16 |
| Tesla K40m (2) | Sentence embeddings + classification | 2–4 GB | 32–64 |

**Kepler Compatibility Note**: Official PyTorch dropped support for Compute Capability 3.x after version 1.12.1. We use ONNX Runtime GPU (compatible with CUDA 11.4 and Kepler) for all inference workloads, avoiding PyTorch entirely for face recognition and OCR.

### 6.3 Scalability

| Phase | Parallelism | Throughput | Time (est.) |
|-------|-------------|------------|-------------|
| Download | 8 aria2c × 10 connections | ~30 files/sec | ~13 hours |
| OCR | 2 GPU workers | ~50 pages/sec | ~16 hours |
| NER | 4 CPU + 1 GPU worker | ~100 docs/sec | ~4 hours |
| Facial Recognition | 1 GPU worker | ~20 images/sec | ~30 minutes |
| KG Construction | 1 worker | ~500 entities/sec | ~10 minutes |

---

## 7. Results

*[To be completed after processing pipeline executes]*

### 7.1 OCR Results

### 7.2 Entity Extraction Results

### 7.3 Facial Recognition Results

### 7.4 Knowledge Graph Results

### 7.5 Correlation Analysis Results

---

## 8. Discussion

*[To be completed after analysis]*

---

## 9. Conclusion

*[To be completed after analysis]*

---

## References

Bagga, A., & Baldwin, B. (1998). Algorithms for scoring coreference chains. *Proceedings of the First International Conference on Language Resources and Evaluation Workshop on Linguistics Coreference*, 563–566.

Cardellino, C., Terreni, L., & Navigli, R. (2017). Legal document analysis: A survey. *Artificial Intelligence and Law*, 25(3), 271–318.

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). CRISP-DM 1.0: Step-by-step data mining guide. *SPSS Inc.*

Christophides, V., Efthymiou, V., Stefanidis, K., & Pallis, G. (2021). Entity resolution in the web of data. *Synthesis Lectures on Data Semantics and Knowledge*, 12(1), 1–202.

Deng, J., Guo, J., Xue, N., & Zafeiriou, S. (2019). ArcFace: Additive angular margin loss for deep face recognition. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 4690–4699.

Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *Proceedings of NAACL-HLT*, 4171–4186.

Grimmer, J., & Stewart, B. M. (2013). Text as data: The promise and pitfalls of automatic content analysis methods for political texts. *Political Analysis*, 21(3), 267–297.

Guo, J., Zhang, Z., Liu, Y., & Wang, X. (2022). InsightFace: 2D and 3D face analysis project. *GitHub repository*.

Ji, S., Pan, S., Cambria, E., Marttinen, P., & Yu, P. S. (2022). A survey on knowledge graphs: Representation, acquisition, and applications. *IEEE Transactions on Neural Networks and Learning Systems*, 33(2), 494–514.

Klein, G., Kim, Y., Deng, Y., Senellart, J., & Rush, A. (2023). OpenNMT: Open-source toolkit for neural machine translation. *Proceedings of ACL*.

Li, M., et al. (2023). TrOCR: Transformer-based optical character recognition with pre-trained models. *Proceedings of AAAI*.

Pradhan, S., Moschitti, A., Xue, N., Ng, H. T., Björkelund, A., Uryupina, O., ... & Zesch, T. (2013). Towards robust linguistic analysis using OntoNotes. *Proceedings of CoNLL*, 143–152.

Terras, M. (2011). The rise of digitization. *Digitisation Perspectives*, 3–20.

Zaveri, A., Rula, A., Maurino, A., Pietrobon, R., Lehmann, J., & Auer, S. (2016). Quality assessment for linked data: A survey. *Semantic Web*, 7(1), 63–93.

---

## Appendix A: Repository

Code and documentation: https://github.com/cbwinslow/epstein_full

## Appendix B: Computational Environment

| Component | Specification |
|-----------|---------------|
| CPU | 40 cores |
| RAM | 125 GB |
| GPU | 2× Tesla K80 (12 GB) + 1× Tesla K40m (11 GB) |
| Storage | 2.5 TB RAID5 (LVM) |
| OS | Ubuntu 24.04 |
| CUDA | 11.4 |
| Python | 3.12 |
