import feedparser
from abc import ABC, abstractmethod
from typing import List, Dict

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



PARSER_REGISTRY = {
    "bbc": BBCRSSParser,
    "techcrunch": TechCrunchRSSParser,
    "cnn": CNNRSSParser,
    "guardian": GuardianRSSParser,

}
