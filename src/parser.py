# parser.py
import feedparser
from abc import ABC, abstractmethod
from typing import List, Dict
# from bs4 import BeautifulSoup
# from dateutil import parser as date_parser
import logging

logger = logging.getLogger(__name__)

class BaseParser(ABC):
    @abstractmethod
    def parse(self, html: str) -> List[Dict]:
        """
        Parse raw HTML and return a list of dicts with keys:
        'source', 'headline', 'url', 'published_at'.
        """
        pass
class BBCRSSParser(BaseParser):
    SOURCE = "bbc"

    def parse(self, xml: str) -> List[Dict]:
        # feedparser.parse can take a URL or raw XML;
        # here xml is the feed text fetched by AsyncFetcher
        feed = feedparser.parse(xml)
        records = []
        for entry in feed.entries:
            published = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
            records.append({
                "source": self.SOURCE,
                "headline": entry.title,
                "url": entry.link,
                "published_at": published,
            })
        return records

class TechCrunchRSSParser(BaseParser):
    SOURCE = "techcrunch"

    def parse(self, xml: str) -> List[Dict]:
        feed = feedparser.parse(xml)
        records = []
        for entry in feed.entries:
            # Some feeds use .published, others use .updated
            published = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
            records.append({
                "source": self.SOURCE,
                "headline": entry.title,
                "url": entry.link,
                "published_at": published,
            })
        return records
    
class CNNRSSParser(BaseParser):
    SOURCE = "cnn"

    def parse(self, xml: str) -> List[Dict]:
        feed = feedparser.parse(xml)
        records = []
        for entry in feed.entries:
            published = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
            records.append({
                "source": self.SOURCE,
                "headline": entry.title,
                "url": entry.link,
                "published_at": published,
            })
        return records


class GuardianRSSParser(BaseParser):
    SOURCE = "guardian"

    def parse(self, xml: str) -> List[Dict]:
        feed = feedparser.parse(xml)
        records = []
        for entry in feed.entries:
            published = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
            records.append({
                "source": self.SOURCE,
                "headline": entry.title,
                "url": entry.link,
                "published_at": published,
            })
        return records


# Registry so fetcher can pick the right parser
PARSER_REGISTRY = {
    "bbc": BBCRSSParser,
    "techcrunch": TechCrunchRSSParser,
    "cnn": CNNRSSParser,
    "guardian": GuardianRSSParser,

}
