"""
Sample data initialization script
Creates sample product attributes, suppliers, and products
"""
import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.product_attributes import (
    ProductCategory, ProductMaterial, ProductStyle, 
    ProductBrand, ProductColor, CountryOfOrigin
)
from app.models.supplier import Supplier, SupplierType
from app.models.product import Product, ProductVariation, OwnershipStatus
from app.utils.slug import generate_slug, ensure_unique_slug
from app.utils.sku import generate_sku


def create_sample_data():
    """Create sample data for the inventory system"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_categories = db.query(ProductCategory).count()
        if existing_categories > 0:
            print("Sample data already exists in the database")
            return
        
        print("Creating sample product attributes...")
        
        # Create product categories
        categories_data = [
            "Handbags", "Backpacks", "Tote Bags", "Clutch Bags", 
            "Crossbody Bags", "Shoulder Bags", "Messenger Bags"
        ]
        categories = []
        for name in categories_data:
            slug = ensure_unique_slug(generate_slug(name), [])
            category = ProductCategory(name=name, slug=slug)
            db.add(category)
            categories.append(category)
        
        # Create product materials
        materials_data = [
            "Leather", "Canvas", "Nylon", "Polyester", "Cotton", 
            "Suede", "Faux Leather", "Denim", "Jute", "Rattan"
        ]
        materials = []
        for name in materials_data:
            slug = ensure_unique_slug(generate_slug(name), [])
            material = ProductMaterial(name=name, slug=slug)
            db.add(material)
            materials.append(material)
        
        # Create product styles
        styles_data = [
            "Casual", "Formal", "Vintage", "Modern", "Bohemian", 
            "Minimalist", "Sporty", "Elegant", "Chic", "Classic"
        ]
        styles = []
        for name in styles_data:
            slug = ensure_unique_slug(generate_slug(name), [])
            style = ProductStyle(name=name, slug=slug)
            db.add(style)
            styles.append(style)
        
        # Create product brands
        brands_data = [
            "Gucci", "Louis Vuitton", "Chanel", "Prada", "Hermès",
            "Coach", "Michael Kors", "Kate Spade", "Tory Burch", "Fossil"
        ]
        brands = []
        for name in brands_data:
            slug = ensure_unique_slug(generate_slug(name), [])
            brand = ProductBrand(name=name, slug=slug)
            db.add(brand)
            brands.append(brand)
        
        # Create product colors
        colors_data = [
            ("Black", "#000000", "rgb(0,0,0)"),
            ("White", "#FFFFFF", "rgb(255,255,255)"),
            ("Brown", "#8B4513", "rgb(139,69,19)"),
            ("Red", "#FF0000", "rgb(255,0,0)"),
            ("Blue", "#0000FF", "rgb(0,0,255)"),
            ("Green", "#008000", "rgb(0,128,0)"),
            ("Pink", "#FFC0CB", "rgb(255,192,203)"),
            ("Gray", "#808080", "rgb(128,128,128)"),
            ("Navy", "#000080", "rgb(0,0,128)"),
            ("Beige", "#F5F5DC", "rgb(245,245,220)")
        ]
        colors = []
        for name, hex_code, rgb_code in colors_data:
            slug = ensure_unique_slug(generate_slug(name), [])
            color = ProductColor(name=name, slug=slug, hex_code=hex_code, rgb_code=rgb_code)
            db.add(color)
            colors.append(color)
        
        # Create countries of origin
        countries_data = [
            "Italy", "France", "Spain", "Germany", "United States",
            "China", "India", "Brazil", "Mexico", "Turkey"
        ]
        countries = []
        for name in countries_data:
            slug = ensure_unique_slug(generate_slug(name), [])
            country = CountryOfOrigin(name=name, slug=slug)
            db.add(country)
            countries.append(country)
        
        # Create suppliers
        suppliers_data = [
            # Factories
            ("Milan Leather Factory", SupplierType.FACTORY, "Via Roma 123, Milan, Italy", "Marco Rossi", "+39 02 1234567", "+39 333 1234567", "marco@milanleather.it", "https://facebook.com/milanleather"),
            ("Paris Fashion House", SupplierType.FACTORY, "Champs-Élysées 456, Paris, France", "Marie Dubois", "+33 1 2345678", "+33 6 12345678", "marie@parisfashion.fr", "https://facebook.com/parisfashion"),
            ("Madrid Craft Co.", SupplierType.FACTORY, "Gran Vía 789, Madrid, Spain", "Carlos Mendez", "+34 91 2345678", "+34 612 345678", "carlos@madridcraft.es", "https://facebook.com/madridcraft"),
            
            # Wholesalers
            ("Global Bags Wholesale", SupplierType.WHOLESALER, "123 Business Ave, New York, USA", "John Smith", "+1 555 1234567", "+1 555 9876543", "john@globalbags.com", "https://facebook.com/globalbags"),
            ("Asian Imports Ltd", SupplierType.WHOLESALER, "456 Trade St, Shanghai, China", "Li Wei", "+86 21 12345678", "+86 138 12345678", "liwei@asianimports.cn", "https://facebook.com/asianimports"),
            ("European Distributors", SupplierType.WHOLESALER, "789 Commerce Blvd, London, UK", "James Wilson", "+44 20 12345678", "+44 7700 123456", "james@eurodist.com", "https://facebook.com/eurodist")
        ]
        suppliers = []
        for name, supplier_type, address, contact, phone, whatsapp, email, facebook in suppliers_data:
            supplier = Supplier(
                supplier_type=supplier_type,
                name=name,
                address=address,
                contact_person=contact,
                phone_number=phone,
                whatsapp_number=whatsapp,
                email_address=email,
                facebook_profile_url=facebook
            )
            db.add(supplier)
            suppliers.append(supplier)
        
        # Flush to get IDs
        db.flush()
        
        print("Creating sample products...")
        
        # Create sample products
        products_data = [
            {
                "name": "Classic Leather Handbag",
                "category": categories[0],  # Handbags
                "material": materials[0],   # Leather
                "brand": brands[0],        # Gucci
                "style": styles[0],        # Casual
                "country": countries[0],   # Italy
                "ownership_status": OwnershipStatus.OWNED,
                "supplier": suppliers[0],  # Milan Leather Factory
                "purchase_price": 150.00,
                "selling_price": 299.99,
                "description": "A timeless leather handbag perfect for everyday use. Made with premium Italian leather.",
                "keywords": "leather, handbag, classic, italian, premium",
                "variations": [
                    (colors[0], 10),  # Black
                    (colors[1], 5),   # White
                    (colors[2], 8)    # Brown
                ]
            },
            {
                "name": "Canvas Backpack",
                "category": categories[1],  # Backpacks
                "material": materials[1],   # Canvas
                "brand": brands[5],        # Coach
                "style": styles[6],        # Sporty
                "country": countries[4],   # United States
                "ownership_status": OwnershipStatus.NOT_OWNED,
                "supplier": suppliers[3],  # Global Bags Wholesale
                "purchase_price": 45.00,
                "selling_price": 89.99,
                "description": "Durable canvas backpack ideal for travel and daily commuting.",
                "keywords": "canvas, backpack, travel, durable, casual",
                "variations": [
                    (colors[0], 15),  # Black
                    (colors[4], 12),  # Blue
                    (colors[5], 8)    # Green
                ]
            },
            {
                "name": "Elegant Clutch Bag",
                "category": categories[3],  # Clutch Bags
                "material": materials[0],   # Leather
                "brand": brands[2],        # Chanel
                "style": styles[1],        # Formal
                "country": countries[1],   # France
                "ownership_status": OwnershipStatus.OWNED,
                "supplier": suppliers[1],  # Paris Fashion House
                "purchase_price": 200.00,
                "selling_price": 399.99,
                "description": "An elegant clutch bag perfect for evening events and special occasions.",
                "keywords": "clutch, elegant, formal, evening, luxury",
                "variations": [
                    (colors[0], 6),   # Black
                    (colors[3], 4),   # Red
                    (colors[6], 3)    # Pink
                ]
            }
        ]
        
        for product_data in products_data:
            # Generate slug
            slug = ensure_unique_slug(generate_slug(product_data["name"]), [])
            
            # Create product
            product = Product(
                name=product_data["name"],
                slug=slug,
                category_id=product_data["category"].id,
                material_id=product_data["material"].id,
                brand_id=product_data["brand"].id,
                style_id=product_data["style"].id,
                country_id=product_data["country"].id,
                ownership_status=product_data["ownership_status"],
                supplier_id=product_data["supplier"].id,
                purchase_price=product_data["purchase_price"],
                selling_price=product_data["selling_price"],
                description=product_data["description"],
                keywords=product_data["keywords"]
            )
            db.add(product)
            db.flush()  # Get product ID
            
            # Create variations
            for color, stock in product_data["variations"]:
                sku = generate_sku(
                    product_name=product.name,
                    color_name=color.name,
                    brand_name=product_data["brand"].name,
                    category_name=product_data["category"].name,
                    product_id=product.id
                )
                
                variation = ProductVariation(
                    product_id=product.id,
                    color_id=color.id,
                    sku=sku,
                    stock_quantity=stock
                )
                db.add(variation)
        
        db.commit()
        print("Sample data created successfully!")
        print(f"- {len(categories)} categories")
        print(f"- {len(materials)} materials")
        print(f"- {len(styles)} styles")
        print(f"- {len(brands)} brands")
        print(f"- {len(colors)} colors")
        print(f"- {len(countries)} countries")
        print(f"- {len(suppliers)} suppliers")
        print(f"- {len(products_data)} products with variations")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


async def main():
    """Main function to initialize database and create sample data"""
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")
    
    print("Creating sample data...")
    create_sample_data()


if __name__ == "__main__":
    asyncio.run(main())
