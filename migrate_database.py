#!/usr/bin/env python3
"""
Database migration script to convert from old fixed-column structure 
to new flexible value structure
"""

import sqlite3
import os
from datetime import datetime

def migrate_database(db_path="finance_control.db"):
    """Migrate existing database to new structure"""
    
    if not os.path.exists(db_path):
        print("No existing database found. New structure will be created automatically.")
        return
    
    print("Starting database migration...")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if old table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='financial_records'")
        old_table_exists = cursor.fetchone() is not None
        
        if not old_table_exists:
            print("No old table found. Migration not needed.")
            return
        
        # Check if new tables already exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_records'")
        new_table_exists = cursor.fetchone() is not None
        
        if new_table_exists:
            print("New table structure already exists. Migration may have been done already.")
            return
        
        # Create new tables
        cursor.execute('''
            CREATE TABLE daily_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                fgts REAL NOT NULL DEFAULT 0,
                total REAL NOT NULL DEFAULT 0,
                total_with_fgts REAL NOT NULL DEFAULT 0,
                percentage_diff REAL DEFAULT 0,
                real_increase REAL DEFAULT 0,
                total_percentage_diff REAL DEFAULT 0,
                total_real_diff REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE record_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                daily_record_id INTEGER NOT NULL,
                value_name TEXT NOT NULL,
                value_amount REAL NOT NULL,
                order_index INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (daily_record_id) REFERENCES daily_records (id) ON DELETE CASCADE
            )
        ''')
        
        # Migrate data from old table
        cursor.execute("SELECT * FROM financial_records ORDER BY date")
        old_records = cursor.fetchall()
        
        print(f"Migrating {len(old_records)} records...")
        
        for record in old_records:
            # Old structure: id, date, valor1, valor2, valor3, total, percentage_diff, 
            # real_increase, fgts, total_with_fgts, total_percentage_diff, total_real_diff, created_at
            old_id, date, valor1, valor2, valor3, total, percentage_diff, real_increase, \
            fgts, total_with_fgts, total_percentage_diff, total_real_diff, created_at = record
            
            # Insert into daily_records
            cursor.execute('''
                INSERT INTO daily_records 
                (date, fgts, total, total_with_fgts, percentage_diff, real_increase, 
                 total_percentage_diff, total_real_diff, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, fgts, total, total_with_fgts, percentage_diff, real_increase,
                  total_percentage_diff, total_real_diff, created_at))
            
            daily_record_id = cursor.lastrowid
            
            # Insert individual values
            values_to_insert = []
            if valor1 != 0:
                values_to_insert.append(("Valor 1", valor1, 0))
            if valor2 != 0:
                values_to_insert.append(("Valor 2", valor2, 1))
            if valor3 != 0:
                values_to_insert.append(("Valor 3", valor3, 2))
            
            for value_name, value_amount, order_index in values_to_insert:
                cursor.execute('''
                    INSERT INTO record_values (daily_record_id, value_name, value_amount, order_index)
                    VALUES (?, ?, ?, ?)
                ''', (daily_record_id, value_name, value_amount, order_index))
        
        # Rename old table as backup
        backup_table_name = f"financial_records_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute(f"ALTER TABLE financial_records RENAME TO {backup_table_name}")
        
        conn.commit()
        
        print(f"Migration completed successfully!")
        print(f"Old table backed up as: {backup_table_name}")
        print("You can delete the backup table once you've verified the migration worked correctly.")

if __name__ == "__main__":
    migrate_database()