from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict

@dataclass
class FinancialRecord:
    """Data class representing a financial record"""
    id: Optional[int] = None
    date: str = ""
    values: List[Dict[str, any]] = field(default_factory=list)
    total: float = 0.0
    percentage_diff: float = 0.0
    real_increase: float = 0.0
    fgts: float = 0.0
    total_with_fgts: float = 0.0
    total_percentage_diff: float = 0.0
    total_real_diff: float = 0.0
    created_at: Optional[str] = None
    
    def calculate_total(self):
        """Calculate total from individual values"""
        self.total = sum(value['amount'] for value in self.values)
        self.total_with_fgts = self.total + self.fgts
    
    def format_currency(self, value: float) -> str:
        """Format value as Brazilian currency"""
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def format_percentage(self, value: float) -> str:
        """Format value as percentage"""
        return f"{value:.2f}%"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for easy display"""
        result = {
            'ID': self.id,
            'Data': self.date,
        }
        
        # Add individual values
        for value in self.values:
            result[value['name']] = self.format_currency(value['amount'])
        
        # Add calculated fields
        result.update({
            'Total': self.format_currency(self.total),
            'Diferença %': self.format_percentage(self.percentage_diff),
            'Aumento Real': self.format_currency(self.real_increase),
            'FGTS': self.format_currency(self.fgts),
            'Total + FGTS': self.format_currency(self.total_with_fgts),
            'Diferença % Total': self.format_percentage(self.total_percentage_diff),
            'Diferença Real Total': self.format_currency(self.total_real_diff)
        })
        
        return result
    
    def get_values_as_tuples(self) -> List[tuple]:
        """Get values as list of (name, amount) tuples"""
        return [(value['name'], value['amount']) for value in self.values]