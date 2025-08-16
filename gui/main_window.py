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
        self.update_value_entries_from_db()  # Populate entries based on existing data
    
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
        ttk.Button(values_buttons_frame, text="Gerenciar Colunas", command=self.manage_columns).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(values_buttons_frame, text="Limpar Valores", command=self.clear_value_entries).pack(side=tk.LEFT)
        
        # Help message frame (will be shown when no entries exist)
        self.help_message_frame = ttk.Frame(values_frame)
        self.help_message_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        help_label = ttk.Label(self.help_message_frame, 
                              text="Nenhum campo de valor adicionado.\nClique em '+ Adicionar Valor' para começar ou 'Gerenciar Colunas' para usar campos existentes.",
                              font=('TkDefaultFont', 9), 
                              foreground='gray',
                              justify=tk.CENTER)
        help_label.pack()
        
        # Initially hide the help message
        self.help_message_frame.grid_remove()
        
        # Initial value entries will be added automatically based on existing data
        # or user can add them manually
        
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
        """Clear all value entries and add ones based on database if available"""
        for entry in self.value_entries:
            entry['frame'].destroy()
        self.value_entries.clear()
        
        # Get existing columns from database
        existing_columns = self.get_all_value_names_from_db()
        
        if existing_columns:
            # Add entries for existing columns
            for col_name in existing_columns:
                self.add_value_entry(col_name)
        # If no existing columns, leave empty - user must add manually
    
    def update_values_canvas(self):
        """Update the canvas scroll region"""
        self.values_canvas.update_idletasks()
        self.values_canvas.configure(scrollregion=self.values_canvas.bbox("all"))
        self.update_help_message_visibility()
    
    def update_help_message_visibility(self):
        """Show or hide help message based on whether there are value entries"""
        if hasattr(self, 'help_message_frame'):
            if len(self.value_entries) == 0:
                self.help_message_frame.grid()
            else:
                self.help_message_frame.grid_remove()
    
    def on_fgts_focus_in(self, event):
        """Handle FGTS field focus in - clear placeholder if it's the default"""
        if self.fgts_var.get() == "0,00":
            self.fgts_var.set("")
    
    def on_fgts_focus_out(self, event):
        """Handle FGTS field focus out - restore placeholder if empty"""
        if not self.fgts_var.get().strip():
            self.fgts_var.set("0,00")
    
    def get_all_value_names_from_db(self):
        """Get all unique value names from the database"""
        records = self.db_manager.get_all_records()
        all_value_names = set()
        for record in records:
            for value in record['values']:
                all_value_names.add(value['name'])
        return sorted(list(all_value_names))
    
    def update_value_entries_from_db(self):
        """Update value entries based on existing database columns"""
        existing_names = self.get_all_value_names_from_db()
        current_names = [entry['name_var'].get() for entry in self.value_entries]
        
        # Add entries for new columns found in database
        for name in existing_names:
            if name not in current_names:
                self.add_value_entry(name)
    
    def manage_columns(self):
        """Open column management dialog"""
        self.open_column_manager()
    
    def open_column_manager(self):
        """Open a dialog to manage database value columns"""
        # Create column management window
        self.column_window = tk.Toplevel(self.root)
        self.column_window.title("Gerenciar Colunas do Banco de Dados")
        self.column_window.geometry("500x600")
        self.column_window.transient(self.root)
        self.column_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.column_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        ttk.Label(main_frame, text="Gerenciamento de Colunas do Banco de Dados", 
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=(0, 5))
        ttk.Label(main_frame, text="Renomeie, exclua ou crie novas colunas de valores no banco de dados.", 
                 font=('TkDefaultFont', 9)).pack(pady=(0, 15))
        
        # Current database columns
        columns_frame = ttk.LabelFrame(main_frame, text="Colunas Existentes no Banco de Dados", padding="10")
        columns_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Listbox for database columns
        listbox_frame = ttk.Frame(columns_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.columns_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=8)
        self.columns_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.columns_listbox.yview)
        
        # Populate columns
        self.refresh_columns_listbox()
        
        # Action buttons
        actions_frame = ttk.Frame(columns_frame)
        actions_frame.pack(fill=tk.X)
        
        ttk.Button(actions_frame, text="Renomear Coluna", 
                  command=self.rename_column_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Excluir Coluna", 
                  command=self.delete_column_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actions_frame, text="Atualizar Lista", 
                  command=self.refresh_columns_listbox).pack(side=tk.LEFT)
        
        # Create new column section
        create_frame = ttk.LabelFrame(main_frame, text="Criar Nova Coluna", padding="10")
        create_frame.pack(fill=tk.X, pady=(0, 15))
        
        # New column input
        input_frame = ttk.Frame(create_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Nome da nova coluna:").pack(side=tk.LEFT, padx=(0, 10))
        self.new_column_var = tk.StringVar()
        self.new_column_entry = ttk.Entry(input_frame, textvariable=self.new_column_var, width=25)
        self.new_column_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.new_column_entry.bind('<Return>', lambda e: self.create_new_column())
        
        ttk.Button(input_frame, text="Criar Coluna", 
                  command=self.create_new_column).pack(side=tk.LEFT)
        
        # Help text
        ttk.Label(create_frame, text="Nota: Criar uma coluna apenas adiciona o nome aos campos de entrada.\nVocê precisará adicionar valores nos registros para que apareça no banco.", 
                 font=('TkDefaultFont', 8), foreground='gray').pack(pady=(5, 0))
        
        # Close button
        ttk.Button(main_frame, text="Fechar", command=self.column_window.destroy).pack(pady=(10, 0))
    
    def refresh_columns_listbox(self):
        """Refresh the database columns listbox"""
        if hasattr(self, 'columns_listbox'):
            self.columns_listbox.delete(0, tk.END)
            columns = self.get_all_value_names_from_db()
            for col in columns:
                self.columns_listbox.insert(tk.END, col)
    
    def rename_column_dialog(self):
        """Open dialog to rename a column"""
        selection = self.columns_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma coluna para renomear")
            return
        
        old_name = self.columns_listbox.get(selection[0])
        
        # Create rename dialog
        rename_dialog = tk.Toplevel(self.column_window)
        rename_dialog.title("Renomear Coluna")
        rename_dialog.geometry("400x200")
        rename_dialog.transient(self.column_window)
        rename_dialog.grab_set()
        
        # Center the dialog
        rename_dialog.update_idletasks()
        x = (rename_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (rename_dialog.winfo_screenheight() // 2) - (200 // 2)
        rename_dialog.geometry(f"400x200+{x}+{y}")
        
        main_frame = ttk.Frame(rename_dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Renomear coluna: '{old_name}'", 
                 font=('TkDefaultFont', 10, 'bold')).pack(pady=(0, 15))
        
        ttk.Label(main_frame, text="Novo nome:").pack(anchor=tk.W, pady=(0, 5))
        new_name_var = tk.StringVar(value=old_name)
        new_name_entry = ttk.Entry(main_frame, textvariable=new_name_var, width=30)
        new_name_entry.pack(fill=tk.X, pady=(0, 15))
        new_name_entry.select_range(0, tk.END)
        new_name_entry.focus()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def confirm_rename():
            new_name = new_name_var.get().strip()
            if not new_name:
                messagebox.showerror("Erro", "O nome da coluna não pode estar vazio")
                return
            
            if new_name == old_name:
                rename_dialog.destroy()
                return
            
            # Check if new name already exists
            existing_columns = self.get_all_value_names_from_db()
            if new_name in existing_columns:
                messagebox.showerror("Erro", f"Já existe uma coluna com o nome '{new_name}'")
                return
            
            # Confirm the operation
            if messagebox.askyesno("Confirmar", 
                                 f"Tem certeza que deseja renomear a coluna '{old_name}' para '{new_name}'?\n\n"
                                 f"Esta operação afetará todos os registros existentes."):
                
                success = self.db_manager.rename_value_column(old_name, new_name)
                if success:
                    messagebox.showinfo("Sucesso", f"Coluna renomeada de '{old_name}' para '{new_name}'!")
                    self.refresh_columns_listbox()
                    self.load_records()  # Refresh the main table
                    self.update_value_entries_from_db()  # Update input fields
                    rename_dialog.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao renomear a coluna")
        
        ttk.Button(button_frame, text="Renomear", command=confirm_rename).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancelar", command=rename_dialog.destroy).pack(side=tk.RIGHT)
    
    def delete_column_dialog(self):
        """Open dialog to delete a column"""
        selection = self.columns_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma coluna para excluir")
            return
        
        column_name = self.columns_listbox.get(selection[0])
        
        # Confirm deletion
        if messagebox.askyesno("Confirmar Exclusão", 
                             f"Tem certeza que deseja excluir a coluna '{column_name}'?\n\n"
                             f"Esta operação:\n"
                             f"• Removerá todos os valores desta coluna de todos os registros\n"
                             f"• Recalculará os totais automaticamente\n"
                             f"• NÃO PODE SER DESFEITA\n\n"
                             f"Deseja continuar?"):
            
            success = self.db_manager.delete_value_column(column_name)
            if success:
                messagebox.showinfo("Sucesso", f"Coluna '{column_name}' excluída com sucesso!")
                self.refresh_columns_listbox()
                self.load_records()  # Refresh the main table
                self.update_value_entries_from_db()  # Update input fields
            else:
                messagebox.showerror("Erro", "Erro ao excluir a coluna")
    
    def create_new_column(self):
        """Create a new column (add to input fields)"""
        new_name = self.new_column_var.get().strip()
        if not new_name:
            messagebox.showerror("Erro", "Digite um nome para a nova coluna")
            return
        
        # Check if name already exists in database
        existing_columns = self.get_all_value_names_from_db()
        if new_name in existing_columns:
            messagebox.showwarning("Aviso", f"A coluna '{new_name}' já existe no banco de dados")
            return
        
        # Check if name already exists in input fields
        current_names = [entry['name_var'].get() for entry in self.value_entries]
        if new_name in current_names:
            messagebox.showwarning("Aviso", f"Já existe um campo de entrada com o nome '{new_name}'")
            return
        
        # Add to input fields
        self.add_value_entry(new_name)
        self.new_column_var.set("")
        messagebox.showinfo("Sucesso", f"Campo '{new_name}' adicionado aos campos de entrada!\n\n"
                                     f"Adicione valores com este nome em novos registros para que apareça no banco de dados.")
        
        # Update help message visibility
        self.update_help_message_visibility()
    
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
            # Check if there are any value entries
            if not self.value_entries:
                messagebox.showerror("Erro", "Adicione pelo menos um campo de valor antes de criar um registro.\nClique em '+ Adicionar Valor' para adicionar um campo.")
                return
            
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
        
        # Update value entries if new columns were found
        self.update_value_entries_from_db()
    
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