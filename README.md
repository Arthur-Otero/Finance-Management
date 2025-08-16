# Finance Control Application

A modular Python application for managing financial records with a visual interface, based on your CSV structure.

## Features

- **Visual Interface**: Easy-to-use GUI built with tkinter
- **Database Storage**: SQLite database for persistent data storage
- **Automatic Calculations**: Automatically calculates totals, percentages, and differences
- **Data Validation**: Input validation for dates and currency values
- **Modular Architecture**: Clean separation of concerns with organized file structure

## Project Structure

```
├── test.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── database/
│   ├── __init__.py
│   └── db_manager.py      # Database operations
├── models/
│   ├── __init__.py
│   └── financial_record.py # Data model
├── utils/
│   ├── __init__.py
│   └── validators.py      # Input validation utilities
└── gui/
    ├── __init__.py
    └── main_window.py     # Main GUI interface
```

## Installation

1. Make sure you have Python 3.7+ installed
2. The application uses only built-in Python libraries (tkinter, sqlite3, datetime)
3. No additional installations required!

## Usage

1. Run the application:
   ```bash
   python test.py
   ```

2. The interface allows you to:
   - **Add Records**: Enter date, values (1, 2, 3), and FGTS
   - **View Records**: See all records in a table format
   - **Delete Records**: Select and delete unwanted records
   - **Automatic Calculations**: The app calculates:
     - Total (sum of values 1, 2, 3)
     - Percentage difference from previous record
     - Real increase/decrease in currency
     - Total with FGTS
     - Total percentage and real differences

## Data Fields

- **Date**: DD/MM/YYYY format
- **Valor 1, 2, 3**: Financial values (Valor 3 is optional, defaults to 0)
- **FGTS**: FGTS value
- **Automatic calculations**:
  - Total
  - Percentage difference from last record
  - Real increase/decrease
  - Total + FGTS
  - Total percentage difference
  - Total real difference

## Database

The application creates a SQLite database file (`finance_control.db`) automatically in the same directory. All your financial records are stored persistently.

## Currency Format

- Input: Accept both formats: `1000.50` or `1000,50`
- Display: Brazilian format `R$ 1.000,50`
- Validation: Ensures positive values and proper number format