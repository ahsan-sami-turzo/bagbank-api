import re
import unicodedata
from typing import Optional


def generate_slug(text: str, max_length: int = 120) -> str:
    """
    Generate a URL-friendly slug from text
    
    Args:
        text: The text to convert to slug
        max_length: Maximum length of the slug
    
    Returns:
        A URL-friendly slug
    """
    if not text:
        return ""
    
    # Convert to lowercase
    slug = text.lower()
    
    # Remove accents and special characters
    slug = unicodedata.normalize('NFKD', slug)
    slug = ''.join(c for c in slug if not unicodedata.combining(c))
    
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Truncate to max_length
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    
    return slug


def ensure_unique_slug(slug: str, existing_slugs: list, max_length: int = 120) -> str:
    """
    Ensure a slug is unique by appending a number if necessary
    
    Args:
        slug: The base slug
        existing_slugs: List of existing slugs to check against
        max_length: Maximum length of the slug
    
    Returns:
        A unique slug
    """
    if slug not in existing_slugs:
        return slug
    
    counter = 1
    base_slug = slug
    
    # If the slug is at max length, truncate it to make room for the counter
    if len(base_slug) >= max_length - 3:  # Leave room for "-XX"
        base_slug = base_slug[:max_length - 3].rstrip('-')
    
    while True:
        new_slug = f"{base_slug}-{counter}"
        if new_slug not in existing_slugs:
            return new_slug
        counter += 1
