"""
Database initialization script
Creates default users for the system
"""
import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.user import User, UserRole
from app.utils.security import get_password_hash


def create_default_users():
    """Create default users in the database"""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Users already exist in the database")
            return
        
        # Create superadmin user
        superadmin = User(
            username="superadmin",
            password_hash=get_password_hash("bbsuperadmin"),
            role=UserRole.SUPERADMIN,
            is_active=True
        )
        
        # Create admin users (multiple)
        admin1 = User(
            username="admin",
            password_hash=get_password_hash("bbadmin"),
            role=UserRole.ADMIN,
            is_active=True
        )
        
        admin2 = User(
            username="admin2",
            password_hash=get_password_hash("bbadmin"),
            role=UserRole.ADMIN,
            is_active=True
        )
        
        # Create moderator users (multiple)
        moderator1 = User(
            username="bbmoderator",
            password_hash=get_password_hash("bbmoderator"),
            role=UserRole.MODERATOR,
            is_active=True
        )
        
        moderator2 = User(
            username="moderator2",
            password_hash=get_password_hash("bbmoderator"),
            role=UserRole.MODERATOR,
            is_active=True
        )
        
        # Add users to database
        db.add(superadmin)
        db.add(admin1)
        db.add(admin2)
        db.add(moderator1)
        db.add(moderator2)
        
        db.commit()
        print("Default users created successfully:")
        print("- superadmin (password: bbsuperadmin)")
        print("- admin (password: bbadmin)")
        print("- admin2 (password: bbadmin)")
        print("- bbmoderator (password: bbmoderator)")
        print("- moderator2 (password: bbmoderator)")
        
    except Exception as e:
        print(f"Error creating users: {e}")
        db.rollback()
    finally:
        db.close()


async def main():
    """Main function to initialize database and create users"""
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")
    
    print("Creating default users...")
    create_default_users()


if __name__ == "__main__":
    asyncio.run(main())

