import pandas as pd
from .database import SessionLocal, engine
from . import models

def seed_data():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        df = pd.read_excel("products.xlsx")
        
        # Clear existing products to avoid duplicates or mixed data
        db.query(models.Product).delete()
        db.commit()

        for index, row in df.iterrows():
            # Construct a name from available columns if 'name' doesn't exist
            if "name" not in df.columns and "TIPO_PRENDA" in df.columns:
                name = f"{row['TIPO_PRENDA']} {row.get('COLOR', '')} {row.get('TALLA', '')}".strip()
            else:
                name = row.get("name", "Unknown Product")

            # Map other columns
            description = row.get("DESCRIPCIÓN") if "DESCRIPCIÓN" in df.columns else row.get("description", "")
            
            # Use PRECIO_50_U as price if price is missing
            if "price" not in df.columns and "PRECIO_50_U" in df.columns:
                price = float(row["PRECIO_50_U"])
            else:
                price = float(row.get("price", 0.0))

            # Map stock
            if "stock" not in df.columns and "CANTIDAD_DISPONIBLE" in df.columns:
                stock = int(row["CANTIDAD_DISPONIBLE"])
            else:
                stock = int(row.get("stock", 0))

            product = models.Product(
                name=name,
                description=description,
                price=price,
                stock=stock
            )
            db.add(product)
        
        db.commit()
        print("Data seeded successfully from products.xlsx.")
    except Exception as e:
        print(f"Error seeding data: {e}")
        # Create dummy data if file fails
        print("Creating dummy data...")
        products = [
            models.Product(name="Laptop", description="High performance laptop", price=999.99, stock=10),
            models.Product(name="Mouse", description="Wireless mouse", price=29.99, stock=50),
            models.Product(name="Keyboard", description="Mechanical keyboard", price=89.99, stock=30),
        ]
        db.add_all(products)
        db.commit()
        print("Dummy data seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
