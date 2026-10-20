"""gRPC health checking summary.

The health protocol reports SERVING per service; aggregating responses
shows whether the whole server should stay in the load balancer.
"""
import logging

LOG = logging.getLogger(__name__)


def overall_status(service_statuses):
    """Return SERVING only when every service reports SERVING."""
    for service, status in (service_statuses or {}).items():
        if status != 'SERVING':
            LOG.debug('service %s is %s', service, status)
            return 'NOT_SERVING'
    return 'SERVING' if service_statuses else 'UNKNOWN'


def unhealthy_services(service_statuses):
    """Return service names not currently SERVING."""
    return sorted(s for s, v in (service_statuses or {}).items()
                  if v != 'SERVING')


__all__ = ['overall_status', 'unhealthy_services']
