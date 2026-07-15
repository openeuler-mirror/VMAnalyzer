#!/usr/bin/env python3
"""Simple string template engine with variable substitution."""
import re
from typing import Any, Dict

class StringTemplate:
    """Renders templates with {{variable}} placeholders."""

    PATTERN = re.compile(r"\{\{(\w+)\}\}")

    def __init__(self, template: str):
        self._template = template

    def render(self, context: Dict[str, Any]) -> str:
        """Render the template with given context."""
        def replace(match):
            key = match.group(1)
            if key in context:
                return str(context[key])
            return match.group(0)
        return self.PATTERN.sub(replace, self._template)

    def extract_vars(self) -> list:
        """Extract all variable names from template."""
        return list(set(self.PATTERN.findall(self._template)))

    def validate(self, context: Dict[str, Any]) -> list:
        """Return list of missing required variables."""
        needed = set(self.extract_vars())
        provided = set(context.keys())
        return list(needed - provided)

    @staticmethod
    def render_string(template: str, context: Dict[str, Any]) -> str:
        """Quick render a template string."""
        return StringTemplate(template).render(context)
