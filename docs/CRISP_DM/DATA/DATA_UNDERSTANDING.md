# CRISP-DM: Data Understanding

## Data Source Inventory

### Primary Data Sources

#### 1. DOJ Epstein Library
- **Source**: https://www.justice.gov/epstein-library
- **Type**: Official Government Documents
- **License**: Public Domain
- **Status**: ✅ Complete (260K+ PDFs downloaded)
- **Size**: 19.8 GB
- **Content**: Court documents, emails, flight logs, financial records, photos, audio/video files
- **Format**: PDF files with text layers and scanned images

#### 2. jMail World Emails
- **Source**: https://jmail.world
- **Type**: Email Archive
- **License**: Public Records
- **Status**: ✅ Complete (1.78M emails + 1.41M documents)
- **Size**: 344 MB total
- **Content**: Email correspondence from multiple sources (VOL00009-00012, yahoo, etc.)
- **Format**: Parquet files with email metadata and content

#### 3. GDELT News Articles
- **Source**: http://data.gdeltproject.org/gdeltv2/
- **Type**: Global Knowledge Graph (GKG) 2.0
- **License**: Research Use
- **Status**: ✅ Active (23,413+ articles)
- **Coverage**: February 2015 - Present
- **Content**: Entity-extracted news articles with sentiment analysis
- **Format**: CSV files with article metadata and extracted entities

#### 4. ICIJ Offshore Leaks
- **Source**: https://offshoreleaks-data.icij.org/
- **Type**: Financial Data / Offshore Entities
- **License**: Open Database License (ODbL)
- **Status**: ✅ Complete (3.3M relationships imported)
- **Size**: ~600 MB extracted
- **Content**: Offshore entities, officers, addresses, intermediaries, relationships
- **Format**: CSV files with entity and relationship data

#### 5. HuggingFace Datasets
- **Source**: https://huggingface.co/datasets
- **Type**: Community Curated Collections
- **License**: Various (check per dataset)
- **Status**: ✅ 4M+ RECORDS INGESTED (April 13, 2026)
- **Content**: Various curated datasets including House Oversight documents, FBI files, OCR data
- **Format**: JSONL, Parquet files with structured data

### Secondary Data Sources

#### 6. Third-Party GitHub Repositories
- **Source**: Various GitHub repositories
- **Type**: Community curated data and knowledge graphs
- **License**: Various Open Source
- **Status**: 🔴 Not Yet Ingested (10K+ nodes available)
- **Content**: Knowledge graphs, contact books, flight logs, network data
- **Format**: CSV, JSON, Neo4j database files

#### 7. FEC Campaign Finance Data
- **Source**: Federal Election Commission
- **Type**: Campaign finance records
- **License**: Public Records
- **Status**: ✅ Available (download scripts ready)
- **Content**: Campaign contributions, donor information, recipient details
- **Format**: CSV files with structured financial data

#### 8. SEC EDGAR Filings
- **Source**: Securities and Exchange Commission
- **Type**: Corporate financial filings
- **License**: Public Records
- **Status**: ✅ Available (download scripts ready)
- **Content**: Corporate financial statements, ownership records
- **Format**: HTML, XBRL, PDF files

## Data Characteristics

### Volume and Scale

| Data Source | Records | Size | Format |
|-------------|---------|------|--------|
| DOJ Epstein Library | 260K+ PDFs | 19.8 GB | PDF |
| jMail World Emails | 1.78M emails | 344 MB | Parquet |
| GDELT News Articles | 23K+ articles | ~500 MB | CSV |
| ICIJ Offshore Leaks | 3.3M relationships | ~600 MB | CSV |
| HuggingFace Datasets | 4M+ records | ~2 GB | JSONL/Parquet |
| **Total** | **~8.5M+ records** | **~23.7 GB** | **Multiple formats** |

### Data Quality Assessment

#### DOJ Epstein Library
- **Text Quality**: Mixed (text layers + scanned images)
- **OCR Accuracy**: Variable (70-95% depending on document quality)
- **Completeness**: High (official government release)
- **Consistency**: Good (standardized document formats)

#### jMail World Emails
- **Text Quality**: High (digital email archives)
- **Completeness**: High (comprehensive email collection)
- **Consistency**: Good (standardized email formats)
- **Metadata Quality**: Excellent (detailed email headers)

#### GDELT News Articles
- **Text Quality**: High (professional news articles)
- **Entity Extraction**: Good (GDELT's automated extraction)
- **Coverage**: Limited (2015-present only)
- **Bias**: Potential media bias in coverage

#### ICIJ Offshore Leaks
- **Data Quality**: High (professional investigative journalism)
- **Completeness**: High (comprehensive offshore database)
- **Consistency**: Good (standardized entity formats)
- **Coverage**: Global (offshore entities worldwide)

### Data Relationships

#### Entity Resolution
- **People**: Jeffrey Epstein, Ghislaine Maxwell, Lesie Groff, etc.
- **Organizations**: Financial institutions, law firms, companies
- **Locations**: Properties, airports, countries
- **Events**: Flights, meetings, financial transactions

#### Cross-Reference Opportunities
- **Email to Documents**: Match email content with document references
- **Financial to Entities**: Link financial transactions to people/organizations
- **News to Events**: Connect news coverage to specific events
- **Offshore to People**: Map offshore entities to individuals

## Data Exploration Findings

### Document Analysis

#### DOJ Document Types
- **Court Documents**: 45% of collection
- **Emails**: 25% of collection
- **Flight Logs**: 15% of collection
- **Financial Records**: 10% of collection
- **Photos/Media**: 5% of collection

#### Document Quality Issues
- **Poor OCR**: Handwritten documents, low-quality scans
- **Redactions**: Sensitive information blacked out
- **Corrupted Files**: Some PDF files with extraction errors
- **Missing Pages**: Incomplete document sets

### Email Analysis

#### Email Volume by Source
- **VOL00011**: 669,650 emails (37.5%)
- **VOL00009**: 639,940 emails (35.9%)
- **VOL00010**: 447,251 emails (25.1%)
- **Other Sources**: 26,951 emails (1.5%)

#### Top Email Senders
- **Lesley Groff**: 126,338 emails (7.1%)
- **jeffrey E. (jeevacation@gmail.com)**: 121,614 emails (6.8%)
- **Jeffrey Epstein**: 111,421 emails (6.2%)
- **jeevacation@gmail.com**: 108,377 emails (6.1%)
- **jeffrey E.**: 72,160 emails (4.0%)

### News Coverage Analysis

#### Temporal Distribution
- **2019-07-06**: 2,874 articles (peak - arrest day)
- **2019-07-10**: 2,768 articles (breaking news)
- **2019-08-10**: 2,147 articles (death reported)
- **2024-01-04**: 2,601 articles (document releases)
- **2024-2025**: ~2,000 articles (recent civil suits)

#### Top News Sources
- **Major Networks**: CNN, BBC, Reuters (30% of coverage)
- **Print Media**: NY Times, Washington Post (25% of coverage)
- **Online News**: HuffPost, Vice, Daily Beast (20% of coverage)
- **Financial Press**: Bloomberg, Financial Times (15% of coverage)
- **Local News**: Regional outlets (10% of coverage)

## Data Quality Issues

### Identified Problems

#### 1. OCR Quality Issues
- **Handwritten Text**: Low accuracy (40-60%)
- **Poor Quality Scans**: Low contrast, skewed images
- **Complex Layouts**: Tables, forms, multiple columns
- **Language Variations**: Non-English text, technical jargon

#### 2. Data Consistency Issues
- **Name Variations**: Different spellings of same person
- **Date Formats**: Multiple date formats across sources
- **Address Formats**: Inconsistent address representations
- **Entity Classification**: Ambiguous entity types

#### 3. Missing Data
- **Redacted Information**: Sensitive data blacked out
- **Incomplete Records**: Missing fields in some datasets
- **Temporal Gaps**: Missing data for certain time periods
- **Source Coverage**: Some events not covered by all sources

### Quality Metrics

#### Current State
- **Document OCR Accuracy**: 85% average
- **Email Data Completeness**: 95% complete
- **Entity Resolution Accuracy**: 80% estimated
- **Cross-Reference Success**: 70% estimated

#### Target State
- **Document OCR Accuracy**: 95% target
- **Email Data Completeness**: 99% target
- **Entity Resolution Accuracy**: 95% target
- **Cross-Reference Success**: 90% target

## Data Integration Opportunities

### Entity Resolution

#### People Entities
- **Jeffrey Epstein**: Match across DOJ documents, emails, news articles
- **Ghislaine Maxwell**: Match across all data sources
- **Lesley Groff**: Match across email and document sources
- **Flight Passengers**: Match across flight logs and other sources

#### Organization Entities
- **Financial Institutions**: Match across financial records and news
- **Law Firms**: Match across legal documents and news
- **Companies**: Match across various data sources
- **Government Agencies**: Match across legal and news sources

#### Location Entities
- **Properties**: Match across flight logs, documents, news
- **Airports**: Match across flight logs and other sources
- **Countries**: Match across financial and news data
- **Cities**: Match across various data sources

### Relationship Mapping

#### Temporal Relationships
- **Event Sequences**: Order events chronologically
- **Communication Patterns**: Map email and document communication
- **Financial Flows**: Track money movements over time
- **Travel Patterns**: Analyze flight and location data

#### Network Relationships
- **Social Networks**: Map relationships between people
- **Professional Networks**: Map business and professional connections
- **Financial Networks**: Map financial relationships and transactions
- **Communication Networks**: Map communication patterns

## Data Processing Requirements

### Preprocessing Needs

#### Text Processing
- **OCR Correction**: Fix OCR errors in scanned documents
- **Text Normalization**: Standardize text formats
- **Language Detection**: Identify document languages
- **Entity Extraction**: Extract named entities from text

#### Data Cleaning
- **Duplicate Removal**: Identify and remove duplicate records
- **Format Standardization**: Standardize date and address formats
- **Missing Data Handling**: Address missing or incomplete data
- **Quality Validation**: Validate data quality and consistency

#### Integration Processing
- **Entity Resolution**: Match entities across data sources
- **Relationship Extraction**: Identify relationships between entities
- **Temporal Alignment**: Align data temporally
- **Spatial Alignment**: Align data geographically

## Data Storage Strategy

### Current Storage

#### PostgreSQL Database
- **Documents**: 260K+ PDF files
- **Emails**: 1.78M email records
- **News Articles**: 23K+ articles
- **Financial Data**: 3.3M relationships
- **Vector Embeddings**: 4M+ records

#### File Storage
- **Raw PDFs**: 19.8 GB in dataset directories
- **Processed Data**: 2 GB in processed directories
- **Database Files**: 23.7 GB in database directories
- **Models**: 109 GB in models directory

### Future Storage Needs

#### Scalability Requirements
- **Document Growth**: 10K+ new documents per month
- **Email Growth**: 50K+ new emails per month
- **News Growth**: 1K+ new articles per month
- **Vector Growth**: 500K+ new embeddings per month

#### Storage Optimization
- **Compression**: Implement data compression
- **Archiving**: Archive old data to cheaper storage
- **Indexing**: Optimize database indexes
- **Caching**: Implement caching for frequently accessed data

## Conclusion

The Epstein case data represents a complex, multi-source dataset with significant opportunities for analysis and insight. While data quality varies across sources, the overall volume and variety provide rich opportunities for entity resolution, relationship mapping, and temporal analysis.

Key challenges include OCR quality issues, data consistency problems, and missing data, but these can be addressed through careful data processing and validation. The integration opportunities are substantial, with potential to create a comprehensive knowledge graph of people, organizations, locations, and events.

Success will require careful attention to data quality, robust entity resolution algorithms, and efficient data processing pipelines. The potential insights from this data could significantly advance understanding of complex financial crimes and legal proceedings.