"""
Processadores Genesys para Power BI
"""

from .filas_primeiro_semestre import ProcessadorFilasPrimeiroSemestre
from .filas_segundo_semestre import ProcessadorFilasSegundoSemestre

__all__ = [
    'ProcessadorFilasPrimeiroSemestre',
    'ProcessadorFilasSegundoSemestre'
]
