"""
Configuration package for the Inventory Management System.
"""

from .settings import load_config, save_config, get_credentials_path

__all__ = ['load_config', 'save_config', 'get_credentials_path']