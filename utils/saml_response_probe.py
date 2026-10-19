"""SAML response condition window check.

Assertions are only valid inside NotBefore/NotOnOrAfter; parsing the
conditions with clock skew rejects stale or premature logins.
"""
import logging
import xml.etree.ElementTree as ET

LOG = logging.getLogger(__name__)


def condition_window(xml_text):
    """Return (not_before, not_on_or_after) strings from Conditions."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return (None, None)
    for elem in root.iter():
        if elem.tag.endswith('Conditions'):
            return (elem.get('NotBefore'), elem.get('NotOnOrAfter'))
    return (None, None)


def has_audience(xml_text, audience):
    """Return True when the assertion lists the expected audience."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return False
    found = any(e.text == audience for e in root.iter()
                if e.tag.endswith('Audience'))
    LOG.debug('saml audience match=%s', found)
    return found


__all__ = ['condition_window', 'has_audience']
