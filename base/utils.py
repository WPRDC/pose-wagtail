import requests
from django.conf import settings
from django.core.cache import cache


def get_featured_extension_slugs():
    """
    Fetch slugs of featured extensions from CKAN catalog API.
    Returns list of extension slugs where is_featured field is True.
    Falls back to empty list if API fails or no featured extensions exist.
    """
    cache_key = "featured_extensions_slugs"
    cached = cache.get(cache_key)
    
    if cached is not None:
        return cached
    
    try:
        response = requests.get(
            f"{settings.CATALOG_HOST}/api/3/action/package_search",
            headers={"Authorization": f"Bearer {settings.CATALOG_API_KEY}"},
            params={
                "fq": "is_featured:True AND type:extension",
                "rows": 100,
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("result", {}).get("results", [])
            slugs = [pkg["name"] for pkg in results]
            
            # Cache for 6 hours
            cache.set(cache_key, slugs, 60 * 60 * 6)
            return slugs
        
        # No results or error
        cache.set(cache_key, [], 60 * 60 * 1)
        return []
        
    except Exception as e:
        print(f"Error fetching featured extensions from API: {e}")
        cache.set(cache_key, [], 60 * 5)
        return []


def get_featured_site_slugs():
    """
    Fetch slugs of featured sites from CKAN catalog API.
    Returns list of site slugs where is_featured field is True.
    Falls back to empty list if API fails or no featured sites exist.
    """
    cache_key = "featured_sites_slugs"
    cached = cache.get(cache_key)
    
    if cached is not None:
        return cached
    
    try:
        response = requests.get(
            f"{settings.CATALOG_HOST}/api/3/action/package_search",
            headers={"Authorization": f"Bearer {settings.CATALOG_API_KEY}"},
            params={
                "fq": "is_featured:True AND type:site",
                "rows": 100,
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("result", {}).get("results", [])
            slugs = [pkg["name"] for pkg in results]
            
            
            cache.set(cache_key, slugs, 60 * 60 * 6)
            return slugs
        
        
        cache.set(cache_key, [], 60 * 60 * 1)
        return []
        
    except Exception as e:
        print(f"Error fetching featured sites from API: {e}")
        cache.set(cache_key, [], 60 * 5)
        return []