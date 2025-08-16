import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.db_manager import DatabaseManager
from models.financial_record import FinancialRecord
from utils.validators import Validators

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Controle Financeiro")
        self.root.geometry("1400x800")
        
        self.db_manager = DatabaseManager()
        self.value_entries = []  # List to store dynamic value entries
        self.setup_ui()
        self.load_records()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Records display section
        self.create_records_section(main_frame)
        
        # Buttons section
        self.create_buttons_section(main_frame)
    
    def create_input_section(self, parent):
        """Create input fields section"""
        input_frame = ttk.LabelFrame(parent, text="Novo Registro", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Date input
        date_frame = ttk.Frame(input_frame)
        date_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(date_frame, text="Data (DD/MM/AAAA):").pack(side=tk.LEFT, padx=(0, 5))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(date_frame, textvariable=self.date_var, width=15).pack(side=tk.LEFT, padx=(0, 20))
        
        # FGTS input (optional)
        ttk.Label(date_frame, text="FGTS (opcional):").pack(side=tk.LEFT, padx=(20, 5))
        self.fgts_var = tk.StringVar()
        fgts_entry = ttk.Entry(date_frame, textvariable=self.fgts_var, width=15)
        fgts_entry.pack(side=tk.LEFT)
        
        # Add placeholder text hint
        fgts_entry.insert(0, "0,00")
        fgts_entry.bind("<FocusIn>", lambda e: self.on_fgts_focus_in(e))
        fgts_entry.bind("<FocusOut>", lambda e: self.on_fgts_focus_out(e))
        
        # Dynamic values section
        values_frame = ttk.LabelFrame(input_frame, text="Valores", padding="5")
        values_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        values_frame.columnconfigure(0, weight=1)
        
        # Scrollable frame for values
        self.values_canvas = tk.Canvas(values_frame, height=150)
        self.values_scrollbar = ttk.Scrollbar(values_frame, orient="vertical", command=self.values_canvas.yview)
        self.values_scrollable_frame = ttk.Frame(self.values_canvas)
        
        self.values_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.values_canvas.configure(scrollregion=self.values_canvas.bbox("all"))
        )
        
        self.values_canvas.create_window((0, 0), window=self.values_scrollable_frame, anchor="nw")
        self.values_canvas.configure(yscrollcommand=self.values_scrollbar.set)
        
        self.values_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.values_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons for managing values
        values_buttons_frame = ttk.Frame(values_frame)
        values_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        ttk.Button(values_buttons_frame, text="+ Adicionar Valor", command=self.add_value_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(values_buttons_frame, text="Limpar Valores", command=self.clear_value_entries).pack(side=tk.LEFT)
        
        # Add initial value entries
        self.add_value_entry("Valor 1")
        self.add_value_entry("Valor 2")
        
        # Action buttons
        action_frame = ttk.Frame(input_frame)
        action_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(action_frame, text="Adicionar Registro", command=self.add_record).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Limpar Campos", command=self.clear_fields).pack(side=tk.LEFT)
    
    def add_value_entry(self, default_name=""):
        """Add a new value entry row"""
        row = len(self.value_entries)
        
        entry_frame = ttk.Frame(self.values_scrollable_frame)
        entry_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=2, padx=5)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.columnconfigure(3, weight=1)
        
        # Name entry
        ttk.Label(entry_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        name_var = tk.StringVar(value=default_name)
        name_entry = ttk.Entry(entry_frame, textvariable=name_var, width=15)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Value entry
        ttk.Label(entry_frame, text="Valor:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        value_var = tk.StringVar()
        value_entry = ttk.Entry(entry_frame, textvariable=value_var, width=15)
        value_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Remove button
        remove_btn = ttk.Button(entry_frame, text="×", width=3, 
                               command=lambda: self.remove_value_entry(row))
        remove_btn.grid(row=0, column=4, padx=(5, 0))
        
        # Store the entry data
        entry_data = {
            'frame': entry_frame,
            'name_var': name_var,
            'value_var': value_var,
            'name_entry': name_entry,
            'value_entry': value_entry,
            'remove_btn': remove_btn
        }
        
        self.value_entries.append(entry_data)
        self.update_values_canvas()
        
        return entry_data
    
    def remove_value_entry(self, index):
        """Remove a value entry by index"""
        if len(self.value_entries) <= 1:
            messagebox.showwarning("Aviso", "Deve haver pelo menos um valor!")
            return
        
        if 0 <= index < len(self.value_entries):
            entry = self.value_entries[index]
            entry['frame'].destroy()
            self.value_entries.pop(index)
            self.reindex_value_entries()
            self.update_values_canvas()
    
    def reindex_value_entries(self):
        """Reindex value entries after removal"""
        for i, entry in enumerate(self.value_entries):
            entry['frame'].grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2, padx=5)
            # Update remove button command
            entry['remove_btn'].configure(command=lambda idx=i: self.remove_value_entry(idx))
    
    def clear_value_entries(self):
        """Clear all value entries and add default ones"""
        for entry in self.value_entries:
            entry['frame'].destroy()
        self.value_entries.clear()
        
        self.add_value_entry("Valor 1")
        self.add_value_entry("Valor 2")
    
    def update_values_canvas(self):
        """Update the canvas scroll region"""
        self.values_canvas.update_idletasks()
        self.values_canvas.configure(scrollregion=self.values_canvas.bbox("all"))
    
    def on_fgts_focus_in(self, event):
        """Handle FGTS field focus in - clear placeholder if it's the default"""
        if self.fgts_var.get() == "0,00":
            self.fgts_var.set("")
    
    def on_fgts_focus_out(self, event):
        """Handle FGTS field focus out - restore placeholder if empty"""
        if not self.fgts_var.get().strip():
            self.fgts_var.set("0,00")
    
    def create_records_section(self, parent):
        """Create records display section"""
        records_frame = ttk.LabelFrame(parent, text="Registros Financeiros", padding="10")
        records_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        records_frame.columnconfigure(0, weight=1)
        records_frame.rowconfigure(0, weight=1)
        
        # Create treeview with basic columns (will be updated dynamically)
        self.tree = ttk.Treeview(records_frame, show='headings', height=15)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(records_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_buttons_section(self, parent):
        """Create buttons section"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Atualizar", command=self.load_records).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Excluir Selecionado", command=self.delete_selected).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Limpar Campos", command=self.clear_fields).pack(side=tk.LEFT)
    
    def add_record(self):
        """Add a new financial record"""
        try:
            # Validate date
            date_valid, date_error = Validators.validate_date(self.date_var.get())
            if not date_valid:
                messagebox.showerror("Erro", date_error)
                return
            
            # Validate FGTS (optional - defaults to 0 if empty or placeholder)
            fgts_str = self.fgts_var.get().strip()
            if fgts_str and fgts_str != "0,00":
                fgts_valid, fgts, fgts_error = Validators.validate_currency(fgts_str)
                if not fgts_valid:
                    messagebox.showerror("Erro", f"FGTS: {fgts_error}")
                    return
            else:
                fgts = 0.0
            
            # Collect and validate all values
            values = []
            for i, entry in enumerate(self.value_entries):
                name = entry['name_var'].get().strip()
                value_str = entry['value_var'].get().strip()
                
                if not name:
                    messagebox.showerror("Erro", f"Nome do valor {i+1} é obrigatório")
                    return
                
                if not value_str:
                    messagebox.showerror("Erro", f"Valor para '{name}' é obrigatório")
                    return
                
                value_valid, value_amount, value_error = Validators.validate_currency(value_str)
                if not value_valid:
                    messagebox.showerror("Erro", f"{name}: {value_error}")
                    return
                
                values.append((name, value_amount))
            
            if not values:
                messagebox.showerror("Erro", "Adicione pelo menos um valor")
                return
            
            # Insert record
            success = self.db_manager.insert_record(
                self.date_var.get(), values, fgts
            )
            
            if success:
                messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
                self.clear_fields()
                self.load_records()
            else:
                messagebox.showerror("Erro", "Erro ao adicionar registro")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def load_records(self):
        """Load and display all records"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load records from database
        records = self.db_manager.get_all_records()
        
        if not records:
            return
        
        # Determine all unique value names across all records
        all_value_names = set()
        for record in records:
            for value in record['values']:
                all_value_names.add(value['name'])
        
        # Create columns dynamically
        base_columns = ['ID', 'Data']
        value_columns = sorted(list(all_value_names))
        summary_columns = ['Total', 'Diferença %', 'Aumento Real', 'FGTS', 
                          'Total + FGTS', 'Diferença % Total', 'Diferença Real Total']
        
        all_columns = base_columns + value_columns + summary_columns
        
        # Configure treeview columns
        self.tree['columns'] = all_columns
        
        for col in all_columns:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=50, minwidth=50)
            elif col == 'Data':
                self.tree.column(col, width=100, minwidth=100)
            else:
                self.tree.column(col, width=120, minwidth=100)
        
        # Insert records
        for record in records:
            # Create FinancialRecord object for formatting
            financial_record = FinancialRecord(
                id=record['id'],
                date=record['date'],
                values=record['values'],
                total=record['total'],
                percentage_diff=record['percentage_diff'],
                real_increase=record['real_increase'],
                fgts=record['fgts'],
                total_with_fgts=record['total_with_fgts'],
                total_percentage_diff=record['total_percentage_diff'],
                total_real_diff=record['total_real_diff']
            )
            
            # Create row data
            row_data = [record['id'], record['date']]
            
            # Add value columns
            value_dict = {v['name']: v['amount'] for v in record['values']}
            for col_name in value_columns:
                if col_name in value_dict:
                    row_data.append(financial_record.format_currency(value_dict[col_name]))
                else:
                    row_data.append("-")
            
            # Add summary columns
            row_data.extend([
                financial_record.format_currency(record['total']),
                financial_record.format_percentage(record['percentage_diff']),
                financial_record.format_currency(record['real_increase']),
                financial_record.format_currency(record['fgts']),
                financial_record.format_currency(record['total_with_fgts']),
                financial_record.format_percentage(record['total_percentage_diff']),
                financial_record.format_currency(record['total_real_diff'])
            ])
            
            self.tree.insert('', 'end', values=row_data)
    
    def delete_selected(self):
        """Delete selected record"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este registro?"):
            item = self.tree.item(selected_item)
            record_id = item['values'][0]  # ID is the first column
            
            success = self.db_manager.delete_record(record_id)
            if success:
                messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
                self.load_records()
            else:
                messagebox.showerror("Erro", "Erro ao excluir registro")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.date_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.fgts_var.set("0,00")
        
        # Clear all value entries
        for entry in self.value_entries:
            entry['value_var'].set("")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()