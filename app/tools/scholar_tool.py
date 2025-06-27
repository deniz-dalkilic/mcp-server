import asyncio
import logging
import httpx
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Constants
CROSSREF_API = "https://api.crossref.org/works"
UA = "mcp-local-scholar/0.1 (+https://github.com/deniz-dalkilic/mcp-server)"

# Data model
@dataclass
class Article:
    title: str
    authors: List[str]
    journal: str
    year: Optional[int]
    doi: str
    url: str

    def to_dict(self) -> Dict[str, Any]:
        # Convert to JSON-serializable dict
        return {
            "title": self.title,
            "authors": self.authors,
            "journal": self.journal,
            "year": self.year,
            "doi": self.doi,
            "url": self.url,
        }

class ScholarTool:
    METHOD = "scholar.search_articles"

    def __init__(
        self,
        max_results: int = 10,
        polite_delay_ms: int = 1000,
        timeout_s: float = 10.0,
    ):
        # max_results: maximum number of articles to return
        # polite_delay_ms: delay between requests (ms)
        # timeout_s: HTTP request timeout (seconds)
        self._max_results = max_results
        self._delay = polite_delay_ms / 1000.0
        self._client = httpx.AsyncClient(timeout=timeout_s)

    async def __call__(
        self,
        query: str,
        max_results: Optional[int] = None,
        since_year: Optional[int] = None,
        until_year: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        RPC entrypoint: delegates to search_articles
        """
        return await self.search_articles(
            query, max_results=max_results, since_year=since_year, until_year=until_year
        )

    async def search_articles(
        self,
        query: str,
        max_results: Optional[int] = None,
        since_year: Optional[int] = None,
        until_year: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Stub implementation: just return an empty list.
        """
        return []

    async def shutdown(self) -> None:
        # Close HTTP client on shutdown
        await self._client.aclose()

def create(config: Dict[str, Any]) -> ScholarTool:
    """
    Factory used by load_tools() to instantiate the tool.
    """
    return ScholarTool(
        max_results=config.get("max_results", 10),
        polite_delay_ms=config.get("polite_delay_ms", 1000),
        timeout_s=config.get("timeout_s", 10.0),
    )
