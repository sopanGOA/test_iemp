"""
Quick Table Verification
========================
This script checks what tables actually exist in your database.
"""

from sqlalchemy import create_engine, text
import logging
from config import DATABASE_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#
DB_CONFIG = DATABASE_CONFIG

connection_string = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(connection_string)

print("=" * 60)
print("CHECKING TABLES IN DATABASE")
print("=" * 60)
print(f"Database: {DB_CONFIG['database']}")
print(f"Schema: {DB_CONFIG['schema']}")
print("")

try:
    with engine.connect() as conn:
        # Get all tables in the schema
        result = conn.execute(text(f"""
            SELECT table_name, 
                   pg_size_pretty(pg_total_relation_size(quote_ident(table_schema)||'.'||quote_ident(table_name))) AS size
            FROM information_schema.tables 
            WHERE table_schema = '{DB_CONFIG['schema']}'
            ORDER BY table_name
        """))
        
        tables = result.fetchall()
        
        if tables:
            print(f"Found {len(tables)} tables in schema '{DB_CONFIG['schema']}':")
            print("-" * 60)
            for table in tables:
                print(f"  ✓ {table[0]:<30} Size: {table[1]}")
            
            print("\n" + "=" * 60)
            print("TABLE STRUCTURE CHECK")
            print("=" * 60)
            
            # Check structure of wrmmoutputs table
            result = conn.execute(text(f"""
                SELECT column_name, data_type, character_maximum_length
                FROM information_schema.columns
                WHERE table_schema = '{DB_CONFIG['schema']}'
                  AND table_name = 'wrmmoutputs'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            print("\nwrmmoutputs table columns:")
            print("-" * 60)
            for col in columns:
                col_name, data_type, max_length = col
                if max_length:
                    print(f"  {col_name:<30} {data_type}({max_length})")
                else:
                    print(f"  {col_name:<30} {data_type}")
            
            # Check indexes
            result = conn.execute(text(f"""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE schemaname = '{DB_CONFIG['schema']}'
                  AND tablename = 'wrmmoutputs'
            """))
            
            indexes = result.fetchall()
            if indexes:
                print("\nIndexes on wrmmoutputs:")
                print("-" * 60)
                for idx in indexes:
                    print(f"  ✓ {idx[0]}")
            
            print("\n" + "=" * 60)
            print("✓ ALL TABLES VERIFIED SUCCESSFULLY!")
            print("=" * 60)
            print("\nYour database is ready to use!")
            print(f"\nIMPORTANT: Update your code to use schema: '{DB_CONFIG['schema']}'")
            
        else:
            print(f"⚠ No tables found in schema '{DB_CONFIG['schema']}'")
            print("\nChecking all schemas...")
            
            result = conn.execute(text("""
                SELECT schema_name 
                FROM information_schema.schemata
                WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
                ORDER BY schema_name
            """))
            
            schemas = result.fetchall()
            print("\nAvailable schemas:")
            for schema in schemas:
                print(f"  - {schema[0]}")
                
                # Check tables in each schema
                result2 = conn.execute(text(f"""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = '{schema[0]}'
                """))
                table_count = result2.fetchone()[0]
                if table_count > 0:
                    print(f"    ({table_count} tables)")

except Exception as e:
    print(f"Error: {e}")
finally:
    engine.dispose()