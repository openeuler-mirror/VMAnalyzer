#!/usr/bin/env python3
"""Resource tagging system for categorizing VMs by metadata labels."""
import json
import os
from typing import Dict, List, Set, Optional

class ResourceTagger:
    """Manages tags for VM resources with persistence support."""

    def __init__(self, persist_path: Optional[str] = None):
        self._tags: Dict[str, Set[str]] = {}
        self._persist_path = persist_path
        if persist_path and os.path.exists(persist_path):
            self._load()

    def tag(self, resource_id: str, tags: List[str]) -> None:
        """Add tags to a resource."""
        if resource_id not in self._tags:
            self._tags[resource_id] = set()
        self._tags[resource_id].update(tags)
        self._save()

    def untag(self, resource_id: str, tag: str) -> bool:
        """Remove a specific tag from a resource."""
        if resource_id in self._tags and tag in self._tags[resource_id]:
            self._tags[resource_id].discard(tag)
            if not self._tags[resource_id]:
                del self._tags[resource_id]
            self._save()
            return True
        return False

    def get_tags(self, resource_id: str) -> List[str]:
        """Return all tags for a resource."""
        return list(self._tags.get(resource_id, []))

    def find_by_tag(self, tag: str) -> List[str]:
        """Find all resources that have the specified tag."""
        return [rid for rid, tags in self._tags.items() if tag in tags]

    def find_by_all_tags(self, tags: List[str]) -> List[str]:
        """Find resources that have all specified tags."""
        tag_set = set(tags)
        return [rid for rid, rtags in self._tags.items() if tag_set.issubset(rtags)]

    def find_by_any_tag(self, tags: List[str]) -> List[str]:
        """Find resources that have at least one of the specified tags."""
        tag_set = set(tags)
        return [rid for rid, rtags in self._tags.items() if rtags & tag_set]

    def remove_resource(self, resource_id: str) -> bool:
        """Remove all tags for a resource."""
        if resource_id in self._tags:
            del self._tags[resource_id]
            self._save()
            return True
        return False

    def list_resources(self) -> List[str]:
        """Return all tagged resource IDs."""
        return list(self._tags.keys())

    def get_tag_counts(self) -> Dict[str, int]:
        """Return a count of resources per tag."""
        counts: Dict[str, int] = {}
        for tags in self._tags.values():
            for tag in tags:
                counts[tag] = counts.get(tag, 0) + 1
        return counts

    def _save(self) -> None:
        """Persist tags to file."""
        if not self._persist_path:
            return
        data = {k: list(v) for k, v in self._tags.items()}
        with open(self._persist_path, "w") as f:
            json.dump(data, f)

    def _load(self) -> None:
        """Load tags from file."""
        with open(self._persist_path, "r") as f:
            data = json.load(f)
        self._tags = {k: set(v) for k, v in data.items()}
