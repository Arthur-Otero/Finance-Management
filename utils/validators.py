import re
from datetime import datetime
from typing import Tuple, Optional

class Validators:
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Validate date format (DD/MM/YYYY)"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True, ""
        except ValueError:
            return False, "Data deve estar no formato DD/MM/AAAA"
    
    @staticmethod
    def validate_currency(value_str: str) -> Tuple[bool, float, str]:
        """Validate and parse currency input"""
        try:
            # Remove currency symbols and spaces
            clean_value = re.sub(r'[R$\s]', '', value_str)
            # Replace comma with dot for decimal
            clean_value = clean_value.replace(',', '.')
            
            value = float(clean_value)
            if value < 0:
                return False, 0.0, "Valor não pode ser negativo"
            
            return True, value, ""
        except ValueError:
            return False, 0.0, "Valor inválido. Use formato: 1000.00 ou 1000,00"
    
    @staticmethod
    def validate_required_fields(**fields) -> Tuple[bool, str]:
        """Validate that required fields are not empty"""
        for field_name, field_value in fields.items():
            if not field_value or str(field_value).strip() == "":
                return False, f"Campo '{field_name}' é obrigatório"
        return True, ""