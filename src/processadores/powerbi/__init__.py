"""
Processadores Power BI - Looker Studio
Automação para alimentação de dados do Power BI
"""

from .filas.filas_primeiro_semestre import ProcessadorFilasPrimeiroSemestre
from .filas.filas_segundo_semestre import ProcessadorFilasSegundoSemestre
from .autoservico.autoservico_primeiro_semestre import ProcessadorAutoservicoPrimeiroSemestre
from .autoservico.autoservico_segundo_semestre import ProcessadorAutoservicoSegundoSemestre

__all__ = [
    'ProcessadorFilasPrimeiroSemestre',
    'ProcessadorFilasSegundoSemestre',
    'ProcessadorAutoservicoPrimeiroSemestre',
    'ProcessadorAutoservicoSegundoSemestre'
]


