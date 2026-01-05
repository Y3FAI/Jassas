"""
Site configurations for the crawler.
Each site has its own config defining crawl behavior.
"""
from .base import SiteConfig
from .my_gov_sa import MyGovSaConfig

# Registry of site configs
SITES = {
    'my.gov.sa': MyGovSaConfig,
}


def get_site_config(domain: str) -> SiteConfig:
    """Get config for a domain."""
    if domain in SITES:
        return SITES[domain]()
    raise ValueError(f"No config for domain: {domain}. Available: {list(SITES.keys())}")
