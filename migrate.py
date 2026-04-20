import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Parse DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Extract connection details from DATABASE_URL
# Format: postgresql+psycopg2://user:password@host:port/database
if DATABASE_URL:
    # Remove the postgresql+psycopg2:// prefix
    url = DATABASE_URL.replace("postgresql+psycopg2://", "")
    # Split into user:password@host:port/database
    auth, location = url.split("@")
    user, password = auth.split(":")
    host_port, dbname = location.split("/")
    host, port = host_port.split(":")
    
    conn = psycopg2.connect(
        host=host,
        port=int(port),
        dbname=dbname,
        user=user,
        password=password,
        sslmode="require"
    )
else:
    print("❌ DATABASE_URL not found in .env file")
    exit(1)

cursor = conn.cursor()

# Safely add email column — IF NOT EXISTS means this won't fail if already added
cursor.execute("""
    ALTER TABLE escalation_logs
    ADD COLUMN IF NOT EXISTS email TEXT;
""")

conn.commit()
print("✅ Migration complete — email column added to escalation_logs")
conn.close()