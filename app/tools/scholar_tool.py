import asyncio
import logging
import httpx
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Constants
CROSSREF_API = "https://api.crossref.org/works"
UA = "mcp-local-scholar/0.1 (+https://github.com/deniz-dalkilic/mcp-server)"

# Module-level logger
type_logger = logging.getLogger(__name__)

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
        Search CrossRef for peer-reviewed articles.

        Parameters
        ----------
        query: Free-text search string.
        max_results: Max number of items to return.
        since_year: Inclusive start year filter.
        until_year: Inclusive end year filter.

        Returns
        -------
        List of article metadata dicts.
        """
        rows = max_results or self._max_results

        # Construct filter list
        filters: List[str] = []
        if since_year:
            filters.append(f"from-pub-date:{since_year}-01-01")
        if until_year:
            filters.append(f"until-pub-date:{until_year}-12-31")

        params: Dict[str, Any] = {"query": query, "rows": rows}
        if filters:
            params["filter"] = ",".join(filters)

        headers = {"User-Agent": UA, "Accept": "application/json"}

        # Retry with exponential backoff
        for attempt in range(3):
            try:
                resp = await self._client.get(CROSSREF_API, params=params, headers=headers)
                resp.raise_for_status()
                break
            except httpx.HTTPError as exc:
                type_logger.warning(
                    "CrossRef request failed (attempt %d): %s", attempt + 1, exc
                )
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)

        data = resp.json()
        items = data.get("message", {}).get("items", [])

        results: List[Dict[str, Any]] = []
        for item in items:
            art = self._parse_item(item)
            results.append(art.to_dict())

        # Polite delay
        await asyncio.sleep(self._delay)
        return results

    def _parse_item(self, item: Dict[str, Any]) -> Article:
        # Parse item JSON into Article
        title_list = item.get("title", [])
        journal_list = item.get("container-title", [])
        authors = [
            f"{a.get('family', '')}, {a.get('given', '')}" for a in item.get("author", [])
        ]
        year = None
        issued = item.get("issued", {}).get("date-parts", [])
        if issued and issued[0]:
            year = issued[0][0]

        return Article(
            title=title_list[0] if title_list else "",
            authors=authors,
            journal=journal_list[0] if journal_list else "",
            year=year,
            doi=item.get("DOI", ""),
            url=item.get("URL", ""),
        )

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
