"""
Modern dark theme configuration for the financial management application
"""
import tkinter as tk
from tkinter import ttk

class DarkTheme:
    """Dark theme configuration"""
    
    # Color palette
    COLORS = {
        'bg_primary': '#1e1e1e',      # Main background
        'bg_secondary': '#2d2d2d',    # Secondary background
        'bg_tertiary': '#3d3d3d',     # Tertiary background
        'bg_hover': '#404040',        # Hover state
        'accent': '#0078d4',          # Primary accent (blue)
        'accent_hover': '#106ebe',    # Accent hover
        'success': '#107c10',         # Success green
        'warning': '#ff8c00',         # Warning orange
        'error': '#d13438',           # Error red
        'text_primary': '#ffffff',    # Primary text
        'text_secondary': '#cccccc',  # Secondary text
        'text_muted': '#999999',      # Muted text
        'border': '#555555',          # Border color
        'input_bg': '#404040',        # Input background
        'card_bg': '#252525',         # Card background
    }
    
    @classmethod
    def configure_styles(cls, root):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        
        # Configure the theme
        style.theme_use('clam')
        
        # Main window
        root.configure(bg=cls.COLORS['bg_primary'])
        
        # Frame styles
        style.configure('Card.TFrame', 
                       background=cls.COLORS['card_bg'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Main.TFrame', 
                       background=cls.COLORS['bg_primary'])
        
        style.configure('Secondary.TFrame', 
                       background=cls.COLORS['bg_secondary'])
        
        # Label styles
        style.configure('Title.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Heading.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Body.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=('Segoe UI', 9))
        
        style.configure('Muted.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_muted'],
                       font=('Segoe UI', 8))
        
        # Button styles
        style.configure('Accent.TButton',
                       background=cls.COLORS['accent'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        style.map('Accent.TButton',
                 background=[('active', cls.COLORS['accent_hover'])])
        
        style.configure('Success.TButton',
                       background=cls.COLORS['success'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        style.configure('Warning.TButton',
                       background=cls.COLORS['warning'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        # Entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['input_bg'],
                       background=cls.COLORS['input_bg'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       insertcolor=cls.COLORS['text_primary'])
        
        # Treeview styles
        style.configure('Modern.Treeview',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       fieldbackground=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       font=('Segoe UI', 9))
        
        style.configure('Modern.Treeview.Heading',
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 9, 'bold'))
        
        # LabelFrame styles
        style.configure('Modern.TLabelframe',
                       background=cls.COLORS['bg_primary'],
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Modern.TLabelframe.Label',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Notebook styles
        style.configure('Modern.TNotebook',
                       background=cls.COLORS['bg_primary'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_secondary'],
                       padding=[20, 10],
                       font=('Segoe UI', 9))
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', cls.COLORS['accent']),
                           ('active', cls.COLORS['bg_hover'])],
                 foreground=[('selected', cls.COLORS['text_primary'])])
        
        return style