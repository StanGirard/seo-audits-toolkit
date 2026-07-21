from rankparse import RankParseClient


def fetch_backlink_audit(domain, api_key):
    """Call RankParse and return the merged backlinks + domain authority payload.

    Raises a rankparse.errors.RankParseError subclass (auth, rate limit, not
    found, etc) on failure — callers are responsible for catching it.
    """
    with RankParseClient(api_key=api_key) as client:
        return {
            "backlinks": client.backlinks(domain),
            "domain_authority": client.domain_authority(domain),
        }
