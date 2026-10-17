"""Adapters package for DramaApp scraper."""

from src.adapters.base import BaseAdapter
from src.adapters.demo_adapter import DemoAdapter
from src.adapters.registry import AdapterNotFoundError, AdapterRegistry

__all__ = [
    "BaseAdapter",
    "DemoAdapter",
    "AdapterRegistry",
    "AdapterNotFoundError",
]
