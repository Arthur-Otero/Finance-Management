# Finance Control Application

A flexible Python application for managing financial records with a dynamic visual interface. Track multiple income sources with custom names and automatic calculations.

## Features

- **Dynamic Value Inputs**: Add unlimited custom-named financial values per day
- **Visual Interface**: Intuitive GUI built with tkinter with scrollable input sections
- **Flexible Database**: Modern database structure supporting N values per record
- **Optional FGTS**: FGTS field is optional and defaults to 0 when empty
- **Automatic Calculations**: Calculates totals, percentages, and differences automatically
- **Smart Columns**: Table columns adapt dynamically to show all your custom value names
- **Data Migration**: Automatic migration from old fixed-column structure
- **Data Validation**: Comprehensive input validation for dates and currency values
- **Modular Architecture**: Clean separation of concerns with organized file structure

## Project Structure

```
├── main.py                 # Main application entry point
├── migrate_database.py     # Database migration script
├── database/
│   ├── __init__.py
│   └── db_manager.py      # Database operations with flexible schema
├── models/
│   ├── __init__.py
│   └── financial_record.py # Data model supporting dynamic values
├── utils/
│   ├── __init__.py
│   └── validators.py      # Input validation utilities
└── gui/
    ├── __init__.py
    └── main_window.py     # Dynamic GUI interface
```

## Installation

1. Make sure you have Python 3.7+ installed
2. The application uses only built-in Python libraries (tkinter, sqlite3, datetime)
3. No additional installations required!

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. **Adding Records**:
   - Enter the date (DD/MM/YYYY format)
   - Add custom-named values using the dynamic input section:
     - Click "+ Adicionar Valor" to add more value inputs
     - Give each value a meaningful name (e.g., "Salário", "Freelance", "Investimentos")
     - Enter the corresponding amounts
     - Use "×" button to remove unwanted value inputs
   - FGTS is optional - leave empty or enter amount
   - Click "Adicionar Registro" to save

3. **Managing Values**:
   - **Dynamic Inputs**: Start with "Valor 1" and "Valor 2", add more as needed
   - **Custom Names**: Each value can have a meaningful name
   - **Scrollable Interface**: Handle many values with scrollable input area
   - **Flexible Removal**: Remove any value input except when only one remains

4. **Viewing Records**:
   - Table columns adapt automatically to show all your custom value names
   - All calculations are performed automatically
   - Records are sorted by date (newest first)

5. **Other Features**:
   - **Delete Records**: Select and delete unwanted records
   - **Clear Fields**: Reset all input fields
   - **Auto-refresh**: Table updates automatically after adding/deleting records

## Data Fields

### Input Fields
- **Date**: DD/MM/YYYY format (required)
- **Custom Values**: Unlimited named financial values (at least one required)
  - Each value needs a name (e.g., "Salário", "Freelance", "Bonus")
  - Each value needs an amount in currency format
- **FGTS**: Optional FGTS value (defaults to 0 if empty)

### Automatic Calculations
- **Total**: Sum of all custom values
- **Percentage Difference**: Percentage change from previous record's total
- **Real Increase**: Currency difference from previous record's total
- **Total + FGTS**: Total including FGTS amount
- **Total Percentage Difference**: Percentage change including FGTS
- **Total Real Difference**: Currency difference including FGTS

### Dynamic Table Columns
The table automatically creates columns for:
- ID and Date (fixed)
- All unique value names from your records (dynamic)
- Summary calculations (fixed)

## Database

The application uses a modern SQLite database structure with two main tables:

- **daily_records**: Stores main record information (date, totals, FGTS, calculations)
- **record_values**: Stores individual named values for each day

The database file (`finance_control.db`) is created automatically in the same directory.

### Migration from Old Structure

If you have an existing database with the old fixed-column structure, run the migration script:

```bash
python migrate_database.py
```

This will:
- Convert old "Valor 1, 2, 3" columns to flexible named values
- Preserve all your existing data and calculations
- Create a backup of the old table
- Set up the new flexible structure

## Currency Format

- Input: Accept both formats: `1000.50` or `1000,50`
- Display: Brazilian format `R$ 1.000,50`
- Validation: Ensures positive values and proper number format

## Examples

### Basic Usage
1. Start the app: `python main.py`
2. Enter today's date
3. Add values like:
   - Name: "Salário", Value: "5000,00"
   - Name: "Freelance", Value: "1200,00"
4. Leave FGTS empty or enter amount
5. Click "Adicionar Registro"

### Advanced Usage
- Track multiple income sources with meaningful names
- Add seasonal bonuses or one-time payments
- Monitor investment returns
- Compare month-to-month growth with automatic calculations

### Custom Value Names Examples
- **Income**: "Salário", "Freelance", "Consultoria", "Vendas"
- **Investments**: "Ações", "Fundos", "Crypto", "Renda Fixa"
- **Business**: "Receita Produto A", "Receita Produto B", "Serviços"
- **Other**: "Bonus", "13º Salário", "Férias", "PLR"

## Benefits of the New Flexible System

- **Scalability**: Add as many income sources as needed
- **Clarity**: Meaningful names instead of generic "Valor 1, 2, 3"
- **Adaptability**: Table columns adjust automatically to your data
- **Future-proof**: Easy to add new income sources without code changes
- **User-friendly**: Intuitive interface with add/remove buttons
- **Optional FGTS**: Skip FGTS if not applicable to your situation