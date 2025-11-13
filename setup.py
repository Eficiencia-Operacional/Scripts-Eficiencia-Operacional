#!/usr/bin/env python3
"""
Setup para instalação do pacote Automação Leroy Merlin
Permite instalar o projeto como um pacote Python
"""
from setuptools import setup, find_packages
import os

# Ler requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Ler README.md para descrição longa
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Sistema RPA para automação de processamento de dados Leroy Merlin"

setup(
    name="automacao-leroy-merlin",
    version="2.4.0",
    description="Sistema RPA para automação de processamento de dados Leroy Merlin",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Leroy Merlin",
    author_email="rycordeiro@leroymerlin.com.br",
    url="https://github.com/Eficiencia-Operacional/Scripts-Eficiencia-Operacional",
    
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    
    install_requires=read_requirements(),
    
    python_requires='>=3.8',
    
    entry_points={
        'console_scripts': [
            'lm-automacao=main:main',
            'lm-interface=interface_visual:main',
            'lm-renomear=renomeador_inteligente:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Portuguese (Brazilian)',
    ],
    
    keywords='rpa automacao leroy-merlin google-sheets salesforce genesys',
    
    project_urls={
        'Repositório': 'https://github.com/Eficiencia-Operacional/Scripts-Eficiencia-Operacional',
        'Documentação': 'https://github.com/Eficiencia-Operacional/Scripts-Eficiencia-Operacional/tree/main/docs',
        'Issues': 'https://github.com/Eficiencia-Operacional/Scripts-Eficiencia-Operacional/issues',
    },
    
    include_package_data=True,
    zip_safe=False,
)
