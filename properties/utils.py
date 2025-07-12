from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

def get_all_properties():
    properties = cache.get('all_properties')

    if not properties:
        properties = list(Property.objects.all())
        cache.set('all_property', properties, timeout=3600)

    return properties


def get_redis_cache_metrics():
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")

        # Get Redis server INFO stats
        info = redis_conn.info()

        # Extract key metrics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else None

        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'cache_hit_ratio': round(hit_ratio, 4) if hit_ratio is not None else 'N/A'
        }

        # Optional logging
        logger = logging.getLogger(__name__)
        logger.info(f"Redis Cache Metrics: {metrics}")

        return metrics

    except Exception as e:
        logging.getLogger(__name__).error(f"Error getting Redis metrics: {e}")
        return {
            'error': str(e)
        }

