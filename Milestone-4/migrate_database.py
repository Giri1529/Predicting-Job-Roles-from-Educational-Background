#!/usr/bin/env python3
"""
Database Migration Script for Edu2Job Enhanced
Adds TOP 3 predictions and gap analysis columns
"""

import sqlite3
import sys
from datetime import datetime

DB_NAME = "smartland.db"

def backup_database():
    """Create a backup of the database"""
    backup_name = f"smartland_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    try:
        import shutil
        shutil.copy2(DB_NAME, backup_name)
        print(f"✅ Backup created: {backup_name}")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def check_database_exists():
    """Check if database exists"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.close()
        return True
    except:
        print(f"❌ Database '{DB_NAME}' not found!")
        return False

def get_column_names(cursor, table_name):
    """Get existing column names from a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]

def migrate_predictions_table():
    """Add new columns to predictions table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    existing_columns = get_column_names(cursor, 'predictions')
    
    migrations = [
        # TOP 3 Predictions
        ("predicted_label_1", "ALTER TABLE predictions ADD COLUMN predicted_label_1 TEXT"),
        ("confidence_1", "ALTER TABLE predictions ADD COLUMN confidence_1 FLOAT"),
        ("predicted_label_2", "ALTER TABLE predictions ADD COLUMN predicted_label_2 TEXT"),
        ("confidence_2", "ALTER TABLE predictions ADD COLUMN confidence_2 FLOAT"),
        ("predicted_label_3", "ALTER TABLE predictions ADD COLUMN predicted_label_3 TEXT"),
        ("confidence_3", "ALTER TABLE predictions ADD COLUMN confidence_3 FLOAT"),
        
        # Gap Analysis
        ("educational_gap", "ALTER TABLE predictions ADD COLUMN educational_gap TEXT"),
        ("educational_gap_reason", "ALTER TABLE predictions ADD COLUMN educational_gap_reason TEXT"),
        ("career_gap", "ALTER TABLE predictions ADD COLUMN career_gap TEXT"),
        ("career_gap_years", "ALTER TABLE predictions ADD COLUMN career_gap_years FLOAT"),
        ("career_gap_reason", "ALTER TABLE predictions ADD COLUMN career_gap_reason TEXT"),
    ]
    
    added_count = 0
    skipped_count = 0
    
    for column_name, sql_statement in migrations:
        if column_name in existing_columns:
            print(f"⏭️  Skipping '{column_name}' - already exists")
            skipped_count += 1
        else:
            try:
                cursor.execute(sql_statement)
                print(f"✅ Added column: {column_name}")
                added_count += 1
            except Exception as e:
                print(f"❌ Failed to add '{column_name}': {e}")
    
    # Migrate old data: Copy predicted_label to predicted_label_1
    if 'predicted_label' in existing_columns and 'predicted_label_1' in get_column_names(cursor, 'predictions'):
        try:
            cursor.execute("""
                UPDATE predictions 
                SET predicted_label_1 = predicted_label,
                    confidence_1 = confidence
                WHERE predicted_label_1 IS NULL
            """)
            migrated_rows = cursor.rowcount
            print(f"✅ Migrated {migrated_rows} old predictions to new format")
        except Exception as e:
            print(f"⚠️  Old data migration warning: {e}")
    
    conn.commit()
    conn.close()
    
    return added_count, skipped_count

def verify_migration():
    """Verify that migration was successful"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    columns = get_column_names(cursor, 'predictions')
    
    required_columns = [
        'predicted_label_1', 'confidence_1',
        'predicted_label_2', 'confidence_2',
        'predicted_label_3', 'confidence_3',
        'educational_gap', 'educational_gap_reason',
        'career_gap', 'career_gap_years', 'career_gap_reason'
    ]
    
    missing = [col for col in required_columns if col not in columns]
    
    conn.close()
    
    if missing:
        print(f"\n❌ Missing columns: {missing}")
        return False
    else:
        print("\n✅ All required columns present!")
        return True

def main():
    print("=" * 60)
    print("🚀 Edu2Job Database Migration Script")
    print("=" * 60)
    print()
    
    # Step 1: Check database exists
    print("Step 1: Checking database...")
    if not check_database_exists():
        print("\n❌ Migration aborted: Database not found")
        sys.exit(1)
    print("✅ Database found")
    print()
    
    # Step 2: Create backup
    print("Step 2: Creating backup...")
    if not backup_database():
        response = input("⚠️  Backup failed. Continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("\n❌ Migration aborted by user")
            sys.exit(1)
    print()
    
    # Step 3: Run migration
    print("Step 3: Running migrations...")
    added, skipped = migrate_predictions_table()
    print(f"\n📊 Migration Summary:")
    print(f"   - Columns added: {added}")
    print(f"   - Columns skipped: {skipped}")
    print()
    
    # Step 4: Verify
    print("Step 4: Verifying migration...")
    if verify_migration():
        print("\n✅ Migration completed successfully!")
        print("\n🎉 Your database is ready for Edu2Job Enhanced!")
        print("\nNext steps:")
        print("  1. Replace the updated Python files")
        print("  2. Run: streamlit run app.py")
        print("  3. Test the new features!")
    else:
        print("\n⚠️  Migration completed with warnings")
        print("Please check the missing columns and try again")
        sys.exit(1)
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()