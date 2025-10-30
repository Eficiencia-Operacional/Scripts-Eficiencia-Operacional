"""
Processadores Power BI - Looker Studio
Automação para alimentação de dados do Power BI
"""

from .genesys.filas_primeiro_semestre import ProcessadorFilasPrimeiroSemestre
from .genesys.filas_segundo_semestre import ProcessadorFilasSegundoSemestre

__all__ = [
    'ProcessadorFilasPrimeiroSemestre',
    'ProcessadorFilasSegundoSemestre'
]
