import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional, Dict

class DatabaseManager:
    def __init__(self, db_path: str = "finance_control.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Main daily records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_records (
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
            
            # Individual values table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS record_values (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    daily_record_id INTEGER NOT NULL,
                    value_name TEXT NOT NULL,
                    value_amount REAL NOT NULL,
                    order_index INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (daily_record_id) REFERENCES daily_records (id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
    
    def insert_record(self, date: str, values: List[Tuple[str, float]], fgts: float) -> bool:
        """Insert a new financial record with dynamic values"""
        try:
            total = sum(value[1] for value in values)
            total_with_fgts = total + fgts
            
            # Calculate differences with previous record
            last_record = self.get_last_record()
            percentage_diff = 0
            real_increase = 0
            total_percentage_diff = 0
            total_real_diff = 0
            
            if last_record:
                last_total = last_record[3]  # total column
                last_total_with_fgts = last_record[4]  # total_with_fgts column
                
                if last_total > 0:
                    percentage_diff = ((total - last_total) / last_total) * 100
                    real_increase = total - last_total
                
                if last_total_with_fgts > 0:
                    total_percentage_diff = ((total_with_fgts - last_total_with_fgts) / last_total_with_fgts) * 100
                    total_real_diff = total_with_fgts - last_total_with_fgts
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert daily record
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_records 
                    (date, fgts, total, total_with_fgts, percentage_diff, real_increase, 
                     total_percentage_diff, total_real_diff)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (date, fgts, total, total_with_fgts, percentage_diff, real_increase,
                      total_percentage_diff, total_real_diff))
                
                daily_record_id = cursor.lastrowid
                
                # Delete existing values for this date (in case of update)
                cursor.execute('DELETE FROM record_values WHERE daily_record_id = ?', (daily_record_id,))
                
                # Insert individual values
                for i, (value_name, value_amount) in enumerate(values):
                    cursor.execute('''
                        INSERT INTO record_values (daily_record_id, value_name, value_amount, order_index)
                        VALUES (?, ?, ?, ?)
                    ''', (daily_record_id, value_name, value_amount, i))
                
                conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting record: {e}")
            return False
    
    def get_all_records(self) -> List[Dict]:
        """Get all financial records with their values"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT dr.*, rv.value_name, rv.value_amount, rv.order_index
                FROM daily_records dr
                LEFT JOIN record_values rv ON dr.id = rv.daily_record_id
                ORDER BY dr.date DESC, rv.order_index ASC
            ''')
            
            records = {}
            for row in cursor.fetchall():
                record_id = row[0]
                if record_id not in records:
                    records[record_id] = {
                        'id': row[0],
                        'date': row[1],
                        'fgts': row[2],
                        'total': row[3],
                        'total_with_fgts': row[4],
                        'percentage_diff': row[5],
                        'real_increase': row[6],
                        'total_percentage_diff': row[7],
                        'total_real_diff': row[8],
                        'created_at': row[9],
                        'values': []
                    }
                
                if row[10]:  # value_name exists
                    records[record_id]['values'].append({
                        'name': row[10],
                        'amount': row[11],
                        'order': row[12]
                    })
            
            return list(records.values())
    
    def get_last_record(self) -> Optional[Tuple]:
        """Get the most recent financial record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM daily_records ORDER BY date DESC LIMIT 1')
            return cursor.fetchone()
    
    def delete_record(self, record_id: int) -> bool:
        """Delete a financial record by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Delete from daily_records (CASCADE will handle record_values)
                cursor.execute('DELETE FROM daily_records WHERE id = ?', (record_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
    
    def get_record_by_date(self, date: str) -> Optional[Dict]:
        """Get a record by date"""
        records = self.get_all_records()
        for record in records:
            if record['date'] == date:
                return record
        return None