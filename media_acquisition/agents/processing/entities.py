"""
Entity Extractor Agent
Extracts named entities from media content using spaCy and GLiNER.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

# Import base classes
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.base import (
    ProcessingAgent, AgentConfig, TaskResult,
    StorageManager
)

logger = logging.getLogger(__name__)


class SpacyEntityExtractor:
    """Extract entities using spaCy NER."""
    
    def __init__(self, model: str = 'en_core_web_trf'):
        self.model_name = model
        self.nlp = None
        
    def load_model(self):
        """Lazy load spaCy model."""
        if self.nlp is None:
            import spacy
            logger.info(f"Loading spaCy model: {self.model_name}")
            try:
                self.nlp = spacy.load(self.model_name)
            except OSError:
                logger.warning(f"Model {self.model_name} not found, using en_core_web_sm")
                self.nlp = spacy.load('en_core_web_sm')
        return self.nlp
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text."""
        if not text or len(text) < 10:
            return []
        
        nlp = self.load_model()
        doc = nlp(text[:100000])  # Limit text length
        
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'source': 'spacy'
            })
        
        return entities


class GLiNEREntityExtractor:
    """Extract entities using GLiNER zero-shot NER."""
    
    def __init__(self, model: str = 'urchade/gliner_multi-v2.1'):
        self.model_name = model
        self.model = None
        self.labels = [
            "person", "organization", "location", "date", "money", 
            "phone number", "email", "website", "case number",
            "flight number", "address", "company"
        ]
    
    def load_model(self):
        """Lazy load GLiNER model."""
        if self.model is None:
            try:
                from gliner import GLiNER
                logger.info(f"Loading GLiNER model: {self.model_name}")
                self.model = GLiNER.from_pretrained(self.model_name)
            except ImportError:
                logger.error("GLiNER not installed. Run: pip install gliner")
                return None
        return self.model
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text using zero-shot NER."""
        if not text or len(text) < 10:
            return []
        
        model = self.load_model()
        if model is None:
            return []
        
        # GLiNER works best with shorter texts
        chunks = [text[i:i+5000] for i in range(0, len(text), 5000)]
        
        all_entities = []
        for chunk in chunks:
            try:
                entities = model.predict_entities(chunk, self.labels)
                for ent in entities:
                    all_entities.append({
                        'text': ent['text'],
                        'label': ent['label'],
                        'start': ent['start'],
                        'end': ent['end'],
                        'score': ent.get('score', 0.0),
                        'source': 'gliner'
                    })
            except Exception as e:
                logger.warning(f"GLiNER extraction failed for chunk: {e}")
        
        return all_entities


class RegexEntityExtractor:
    """Extract entities using regex patterns."""
    
    import re
    
    PATTERNS = {
        'date': [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # MM-DD-YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        ],
        'phone': [
            r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',  # (555) 123-4567
            r'\b\d{3}-\d{3}-\d{4}\b',  # 555-123-4567
            r'\b\+1\s*\d{3}[\s-]?\d{3}[\s-]?\d{4}\b',  # +1 555-123-4567
        ],
        'email': [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        ],
        'money': [
            r'\$[\d,]+(?:\.\d{2})?',  # $1,000 or $1,000.00
            r'\b\d{1,3}(?:,\d{3})+\s*(?:USD|dollars?)\b',
        ],
        'case_number': [
            r'\b(?:Case\s+)?(?:No\.?\s*)?\d{1,2}:\d{2}-[A-Za-z]{2,4}-\d{4,6}\b',  # 1:23-cv-12345
            r'\b(?:Case\s+)?(?:No\.?\s*)?\d{2}-\d{5}\b',  # 02-12345
        ],
        'flight_number': [
            r'\bN\d{1,5}[A-Z]{0,2}\b',  # Aircraft tail numbers (N12345, N123AB)
        ],
    }
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities using regex patterns."""
        import re
        
        entities = []
        
        for label, patterns in self.PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    entities.append({
                        'text': match.group(),
                        'label': label.upper(),
                        'start': match.start(),
                        'end': match.end(),
                        'source': 'regex'
                    })
        
        return entities


class TextAnalyzer:
    """Analyze text for sentiment and key topics."""
    
    def __init__(self):
        self.sentiment_analyzer = None
    
    def load_sentiment_model(self):
        """Lazy load sentiment model."""
        if self.sentiment_analyzer is None:
            try:
                from textblob import TextBlob
                self.sentiment_analyzer = TextBlob
            except ImportError:
                logger.warning("TextBlob not installed, sentiment analysis disabled")
                return None
        return self.sentiment_analyzer
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text."""
        analyzer = self.load_sentiment_model()
        if analyzer is None or not text:
            return {'polarity': 0.0, 'subjectivity': 0.0}
        
        blob = analyzer(text[:10000])  # Limit length
        return {
            'polarity': blob.sentiment.polarity,  # -1 to 1
            'subjectivity': blob.sentiment.subjectivity  # 0 to 1
        }
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """Extract keywords using TF-IDF or simple frequency."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Fit on single document (not ideal but works for quick extraction)
            tfidf = vectorizer.fit_transform([text])
            
            # Get feature names and scores
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf.toarray()[0]
            
            # Sort by score
            top_indices = scores.argsort()[-top_n:][::-1]
            keywords = [feature_names[i] for i in top_indices if scores[i] > 0]
            
            return keywords
            
        except ImportError:
            # Fallback to simple frequency
            import re
            from collections import Counter
            
            words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
            stopwords = {'this', 'that', 'with', 'from', 'they', 'have', 'were', 'been', 'their', 'would', 'there', 'could', 'should'}
            words = [w for w in words if w not in stopwords]
            
            return [word for word, _ in Counter(words).most_common(top_n)]
    
    def classify_topic(self, text: str) -> Tuple[str, float]:
        """Classify text into predefined topics."""
        topics = {
            'legal_proceeding': ['court', 'lawsuit', 'trial', 'hearing', 'judge', 'attorney', 'defendant', 'plaintiff'],
            'investigation': ['investigation', 'probe', 'inquiry', 'evidence', 'witness', 'testimony', 'deposition'],
            'financial': ['money', 'payment', 'transaction', 'account', 'bank', 'wire', 'transfer', 'loan'],
            'travel': ['flight', 'airport', 'passport', 'travel', 'island', 'palm beach', 'new york', 'london'],
            'abuse_allegation': ['abuse', 'assault', 'victim', 'minor', 'underage', 'trafficking', 'exploitation'],
            'political': ['politician', 'president', 'senator', 'congress', 'election', 'campaign', 'donation'],
        }
        
        text_lower = text.lower()
        topic_scores = {}
        
        for topic, keywords in topics.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            topic_scores[topic] = score / len(keywords)
        
        # Get best topic
        best_topic = max(topic_scores, key=topic_scores.get)
        best_score = topic_scores[best_topic]
        
        return best_topic, best_score


class EntityExtractor(ProcessingAgent):
    """
    Agent for extracting entities from media content.
    
    Uses multiple NER approaches:
    1. spaCy NER (fast, reliable for common entities)
    2. GLiNER (zero-shot, for custom entity types)
    3. Regex patterns (dates, phones, emails, money, case numbers)
    
    Also performs text analysis:
    - Sentiment analysis
    - Keyword extraction
    - Topic classification
    """
    
    AGENT_ID = 'entity-extractor-v2'
    VERSION = '2.0.0'
    
    def __init__(self, config: Optional[AgentConfig] = None, storage: Optional[StorageManager] = None):
        super().__init__(config, storage)
        
        # Initialize extractors
        self.spacy_extractor = SpacyEntityExtractor()
        self.gliner_extractor = GLiNEREntityExtractor()
        self.regex_extractor = RegexEntityExtractor()
        self.text_analyzer = TextAnalyzer()
    
    def _validate_config(self):
        """Validate agent configuration."""
        pass
    
    async def process_news_article(self, article_id: int, content: str) -> Dict[str, Any]:
        """
        Process a news article and extract entities.
        
        Args:
            article_id: Database ID of article
            content: Article text content
            
        Returns:
            Dict with extracted entities and analysis
        """
        logger.info(f"Processing article {article_id} ({len(content)} chars)")
        
        # Run extractions in parallel
        loop = asyncio.get_event_loop()
        
        spacy_task = loop.run_in_executor(None, self.spacy_extractor.extract, content)
        gliner_task = loop.run_in_executor(None, self.gliner_extractor.extract, content)
        regex_task = loop.run_in_executor(None, self.regex_extractor.extract, content)
        sentiment_task = loop.run_in_executor(None, self.text_analyzer.analyze_sentiment, content)
        keywords_task = loop.run_in_executor(None, self.text_analyzer.extract_keywords, content)
        topic_task = loop.run_in_executor(None, self.text_analyzer.classify_topic, content)
        
        # Wait for all tasks
        spacy_results = await spacy_task
        gliner_results = await gliner_task
        regex_results = await regex_task
        sentiment = await sentiment_task
        keywords = await keywords_task
        topic, topic_confidence = await topic_task
        
        # Combine and deduplicate entities
        all_entities = self._combine_entities(spacy_results + gliner_results + regex_results)
        
        result = {
            'article_id': article_id,
            'entities': all_entities,
            'entity_count': len(all_entities),
            'sentiment': sentiment,
            'keywords': keywords,
            'primary_topic': topic,
            'topic_confidence': topic_confidence,
            'processed_at': datetime.now().isoformat()
        }
        
        # Store in database
        if self.storage:
            try:
                self.storage.update_news_article_analysis(
                    article_id=article_id,
                    entities_mentioned={'entities': all_entities},
                    sentiment_score=sentiment['polarity'],
                    subjectivity_score=sentiment['subjectivity'],
                    keywords=keywords,
                    primary_topic=topic,
                    topic_confidence=topic_confidence
                )
            except Exception as e:
                logger.error(f"Failed to store analysis: {e}")
        
        self.metrics['items_processed'] += 1
        
        return result
    
    def _combine_entities(self, entities: List[Dict]) -> List[Dict]:
        """Combine and deduplicate entities from multiple sources."""
        # Group by text
        by_text = {}
        
        for ent in entities:
            text = ent['text'].lower().strip()
            if text not in by_text:
                by_text[text] = ent
            else:
                # Keep the one with higher score or more specific label
                existing = by_text[text]
                if ent.get('score', 0) > existing.get('score', 0):
                    by_text[text] = ent
        
        return list(by_text.values())
    
    async def process_video_transcript(self, video_id: int, transcript: str) -> Dict[str, Any]:
        """Process a video transcript and extract entities."""
        logger.info(f"Processing transcript for video {video_id}")
        
        # Similar to news article processing
        result = await self.process_news_article(video_id, transcript)
        result['video_id'] = video_id
        del result['article_id']
        
        return result
    
    async def process_document(self, document_id: int, text: str) -> Dict[str, Any]:
        """Process a document and extract entities."""
        logger.info(f"Processing document {document_id}")
        
        result = await self.process_news_article(document_id, text)
        result['document_id'] = document_id
        del result['article_id']
        
        return result
    
    async def process_unprocessed_media(self, batch_size: int = 100) -> List[Dict[str, Any]]:
        """
        Process a batch of unprocessed media items.
        
        Args:
            batch_size: Number of items to process
            
        Returns:
            List of processing results
        """
        if not self.storage:
            raise ValueError("Storage manager required")
        
        # Get unprocessed news articles
        articles = self.storage.get_unprocessed_news_articles(limit=batch_size)
        
        results = []
        
        for article in articles:
            try:
                result = await self.process_news_article(
                    article['id'],
                    article['content']
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process article {article['id']}: {e}")
                self.metrics['errors'] += 1
        
        return results
    
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute processing task."""
        media_type = task.get("media_type", "news")
        media_id = task.get("media_id")
        content = task.get("content")
        
        if not content:
            return TaskResult(
                status="failure",
                error="No content provided"
            )
        
        try:
            if media_type == "news":
                result = await self.process_news_article(media_id, content)
            elif media_type == "video":
                result = await self.process_video_transcript(media_id, content)
            elif media_type == "document":
                result = await self.process_document(media_id, content)
            else:
                return TaskResult(
                    status="failure",
                    error=f"Unknown media type: {media_type}"
                )
            
            return TaskResult(
                status="success",
                output=result,
                metrics=self.metrics
            )
            
        except Exception as e:
            return TaskResult(
                status="failure",
                error=str(e),
                retry_allowed=True
            )


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Entity Extractor Agent')
    parser.add_argument('text', help='Text to analyze')
    parser.add_argument('--detailed', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create agent
    agent = EntityExtractor()
    
    # Process
    print(f"Analyzing text ({len(args.text)} chars)...")
    print("-" * 60)
    
    result = asyncio.run(agent.process_news_article(0, args.text))
    
    print(f"\n✅ ANALYSIS COMPLETE")
    print(f"Entities found: {result['entity_count']}")
    print(f"Sentiment: {result['sentiment']['polarity']:.2f} (polarity)")
    print(f"Subjectivity: {result['sentiment']['subjectivity']:.2f}")
    print(f"Primary topic: {result['primary_topic']} ({result['topic_confidence']:.2f})")
    print(f"Keywords: {', '.join(result['keywords'][:10])}")
    
    if args.detailed and result['entities']:
        print(f"\nEntities:")
        for ent in result['entities'][:20]:
            print(f"  - {ent['text']} ({ent['label']}) [{ent['source']}]")
