import re
from typing import Optional


def generate_sku(
    product_name: str,
    color_name: str,
    brand_name: str,
    category_name: str,
    product_id: Optional[int] = None
) -> str:
    """
    Generate a SKU for a product variation
    
    SKU Format: [CATEGORY][BRAND][PRODUCT][COLOR][ID]
    Example: BAG-NIKE-AIRMAX-RED-001
    
    Args:
        product_name: Name of the product
        color_name: Name of the color
        brand_name: Name of the brand
        category_name: Name of the category
        product_id: Optional product ID to append
    
    Returns:
        A generated SKU
    """
    # Clean and format each component
    category_code = _extract_code(category_name, 3)
    brand_code = _extract_code(brand_name, 3)
    product_code = _extract_code(product_name, 4)
    color_code = _extract_code(color_name, 3)
    
    # Build SKU
    sku_parts = [category_code, brand_code, product_code, color_code]
    
    # Add product ID if provided
    if product_id:
        sku_parts.append(f"{product_id:03d}")
    
    # Join with hyphens and convert to uppercase
    sku = "-".join(sku_parts).upper()
    
    return sku


def _extract_code(text: str, max_length: int) -> str:
    """
    Extract a code from text by taking the first letters of each word
    
    Args:
        text: The text to extract code from
        max_length: Maximum length of the code
    
    Returns:
        A code string
    """
    if not text:
        return "UNK"
    
    # Split into words and take first letter of each
    words = text.split()
    code = "".join(word[0] for word in words if word)
    
    # If no words or code is too short, take first characters
    if not code or len(code) < 3:
        # Remove special characters and take first characters
        clean_text = re.sub(r'[^a-zA-Z0-9]', '', text)
        code = clean_text[:max_length] if clean_text else "UNK"
    
    # Truncate to max_length
    return code[:max_length]


def validate_sku_format(sku: str) -> bool:
    """
    Validate if a SKU follows the expected format
    
    Args:
        sku: The SKU to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Pattern: CAT-BRA-PROD-COL-ID (where ID is optional)
    pattern = r'^[A-Z0-9]{2,4}-[A-Z0-9]{2,4}-[A-Z0-9]{2,4}-[A-Z0-9]{2,4}(-\d{3})?$'
    return bool(re.match(pattern, sku))
