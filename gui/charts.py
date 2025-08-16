"""
Financial charts and data visualization components
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

class FinancialCharts:
    """Financial data visualization components"""
    
    def __init__(self, parent, theme_colors):
        self.parent = parent
        self.colors = theme_colors
        self.setup_matplotlib_style()
    
    def setup_matplotlib_style(self):
        """Configure matplotlib for dark theme"""
        plt.style.use('dark_background')
        
        # Set default colors
        plt.rcParams.update({
            'figure.facecolor': self.colors['bg_primary'],
            'axes.facecolor': self.colors['bg_secondary'],
            'axes.edgecolor': self.colors['border'],
            'axes.labelcolor': self.colors['text_primary'],
            'text.color': self.colors['text_primary'],
            'xtick.color': self.colors['text_secondary'],
            'ytick.color': self.colors['text_secondary'],
            'grid.color': self.colors['border'],
            'grid.alpha': 0.3,
            'font.size': 9,
            'font.family': 'Segoe UI'
        })
    
    def create_evolution_chart(self, records_data):
        """Create total evolution line chart"""
        if not records_data:
            return self.create_empty_chart("Nenhum dado disponível")
        
        # Prepare data
        dates = []
        totals = []
        totals_with_fgts = []
        
        for record in reversed(records_data):  # Reverse to get chronological order
            try:
                date = datetime.strptime(record['date'], '%d/%m/%Y')
                dates.append(date)
                totals.append(record['total'])
                totals_with_fgts.append(record['total_with_fgts'])
            except ValueError:
                continue
        
        if not dates:
            return self.create_empty_chart("Dados de data inválidos")
        
        # Create figure
        fig = Figure(figsize=(10, 6), facecolor=self.colors['bg_primary'])
        ax = fig.add_subplot(111)
        
        # Plot lines
        ax.plot(dates, totals, color=self.colors['accent'], linewidth=2.5, 
               label='Total', marker='o', markersize=4)
        ax.plot(dates, totals_with_fgts, color=self.colors['success'], linewidth=2.5, 
               label='Total + FGTS', marker='s', markersize=4)
        
        # Customize chart
        ax.set_title('Evolução Financeira', fontsize=14, fontweight='bold', 
                    color=self.colors['text_primary'], pad=20)
        ax.set_xlabel('Data', fontsize=10, color=self.colors['text_secondary'])
        ax.set_ylabel('Valor (R$)', fontsize=10, color=self.colors['text_secondary'])
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(self.format_currency))
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        
        # Grid and legend
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        
        # Rotate x-axis labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        fig.tight_layout()
        return fig
    
    def create_values_breakdown_chart(self, records_data):
        """Create pie chart showing breakdown of latest values"""
        if not records_data:
            return self.create_empty_chart("Nenhum dado disponível")
        
        # Get latest record
        latest_record = records_data[0]
        values = latest_record.get('values', [])
        
        if not values:
            return self.create_empty_chart("Nenhum valor encontrado")
        
        # Prepare data
        labels = [v['name'] for v in values]
        sizes = [v['amount'] for v in values]
        
        # Create figure
        fig = Figure(figsize=(8, 6), facecolor=self.colors['bg_primary'])
        ax = fig.add_subplot(111)
        
        # Create color palette
        colors = [self.colors['accent'], self.colors['success'], self.colors['warning'], 
                 self.colors['error'], '#9d4edd', '#f72585', '#4cc9f0', '#7209b7']
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         colors=colors[:len(labels)], startangle=90,
                                         textprops={'color': self.colors['text_primary']})
        
        # Customize
        ax.set_title(f'Composição de Valores - {latest_record["date"]}', 
                    fontsize=14, fontweight='bold', color=self.colors['text_primary'], pad=20)
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        fig.tight_layout()
        return fig
    
    def create_growth_chart(self, records_data):
        """Create bar chart showing month-over-month growth"""
        if len(records_data) < 2:
            return self.create_empty_chart("Dados insuficientes para análise de crescimento")
        
        # Prepare data
        dates = []
        growth_values = []
        growth_percentages = []
        
        for record in reversed(records_data):  # Reverse to get chronological order
            try:
                date = datetime.strptime(record['date'], '%d/%m/%Y')
                dates.append(date.strftime('%m/%Y'))
                growth_values.append(record['real_increase'])
                growth_percentages.append(record['percentage_diff'])
            except ValueError:
                continue
        
        if len(dates) < 2:
            return self.create_empty_chart("Dados insuficientes")
        
        # Create figure
        fig = Figure(figsize=(10, 6), facecolor=self.colors['bg_primary'])
        ax = fig.add_subplot(111)
        
        # Create bars with colors based on positive/negative growth
        colors = [self.colors['success'] if val >= 0 else self.colors['error'] 
                 for val in growth_values[1:]]  # Skip first value (no previous data)
        
        bars = ax.bar(dates[1:], growth_values[1:], color=colors, alpha=0.8)
        
        # Add value labels on bars
        for bar, percentage in zip(bars, growth_percentages[1:]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{percentage:.1f}%',
                   ha='center', va='bottom' if height >= 0 else 'top',
                   color=self.colors['text_primary'], fontweight='bold')
        
        # Customize chart
        ax.set_title('Crescimento Mensal', fontsize=14, fontweight='bold', 
                    color=self.colors['text_primary'], pad=20)
        ax.set_xlabel('Período', fontsize=10, color=self.colors['text_secondary'])
        ax.set_ylabel('Variação (R$)', fontsize=10, color=self.colors['text_secondary'])
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(self.format_currency))
        
        # Add horizontal line at zero
        ax.axhline(y=0, color=self.colors['border'], linestyle='-', alpha=0.5)
        
        # Grid
        ax.grid(True, alpha=0.3, axis='y')
        
        # Rotate x-axis labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        fig.tight_layout()
        return fig
    
    def create_empty_chart(self, message):
        """Create empty chart with message"""
        fig = Figure(figsize=(8, 6), facecolor=self.colors['bg_primary'])
        ax = fig.add_subplot(111)
        
        ax.text(0.5, 0.5, message, transform=ax.transAxes, 
               ha='center', va='center', fontsize=14,
               color=self.colors['text_muted'])
        
        ax.set_facecolor(self.colors['bg_secondary'])
        ax.set_xticks([])
        ax.set_yticks([])
        
        return fig
    
    def format_currency(self, x, pos):
        """Format number as Brazilian currency"""
        if x >= 1000000:
            return f'R$ {x/1000000:.1f}M'
        elif x >= 1000:
            return f'R$ {x/1000:.1f}K'
        else:
            return f'R$ {x:.0f}'
    
    def embed_chart(self, parent_frame, figure):
        """Embed matplotlib figure in tkinter frame"""
        # Clear existing widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(figure, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return canvas