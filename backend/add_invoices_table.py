"""
Script to add invoices table to existing database.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base, DB_PATH, InvoiceDB, StudentProfileDB
import os

def add_invoices_table():
    """Add invoices table to database."""
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Create only the invoices table
    InvoiceDB.__table__.create(engine, checkfirst=True)
    
    print(f"✓ Invoices table created successfully in {DB_PATH}")

if __name__ == "__main__":
    add_invoices_table()
