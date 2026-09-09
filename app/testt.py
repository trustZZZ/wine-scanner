from app.database import engine, Base

def main():
    print("Dropping and recreating tables...")
    Base.metadata.drop_all(bind=engine)  # ⚠️ Только для локальной разработки!
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    main()
