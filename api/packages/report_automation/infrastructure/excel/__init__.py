"""Excel generation and formatting."""

from .generator import ExcelGeneratorImpl, ExcelFormatterImpl, SimpleExcelGenerator

# Alias for easier importing
ExcelGenerator = ExcelGeneratorImpl
ExcelFormatter = ExcelFormatterImpl

__all__ = ["ExcelGenerator", "ExcelGeneratorImpl", "ExcelFormatter", "ExcelFormatterImpl", "SimpleExcelGenerator"]
