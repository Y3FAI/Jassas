"""
Site-specific parsers for the cleaner.
"""
from .base import SiteParser
from .my_gov_sa import MyGovSaParser

PARSERS = {
    'my.gov.sa': MyGovSaParser,
}


def get_parser(url: str) -> SiteParser:
    """Get parser for URL's domain."""
    for domain, parser_class in PARSERS.items():
        if domain in url:
            return parser_class()
    return SiteParser()  # Default parser
