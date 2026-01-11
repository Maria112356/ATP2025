# Simulação de Clínica Médica

## Descrição

Este projeto implementa uma *simulação de eventos discretos* de uma clínica médica, desenvolvido no âmbito da unidade curricular de Algoritmos e Técnicas de Programação. A aplicação modela o atendimento de doentes numa clínica com chegadas aleatórias de doentes;atendimento por um número configurável de médicos; gestão de filas de espera;distribuições estatísticas para tempos de consulta, permitindo analisar métricas operacionais como tempos de espera, ocupação dos médicos e comportamento da fila de espera ao longo do tempo.

A simulação é executada através de uma interface gráfica, onde o utilizador define os parâmetros do sistema e observa os resultados estatísticos e gráficos produzidos.

## Autores

Desenvolvido pelas alunas:

- Ana Luísa Vieira Guimarães A111242
- Maria dos Santos Vidal A112356
- Rafaela Ferreira de Lima e Campos A111322

## Características Principais

- *Simulação de eventos discretos*: Modela o funcionamento de uma clínica médica com chegadas aleatórias de doentes
- *Distribuições estatísticas*: Suporta diferentes distribuições para tempos de consulta (exponencial, normal, uniforme)
- *Sistema de especialidades*: Opção para implementar médicos com especialidades específicas
- *Interface gráfica intuitiva*: Interface desenvolvida com FreeSimpleGUI
- *Visualização de resultados*: Gráficos e estatísticas detalhadas
- *Log integrado*: Visualização dos resultados diretamente na interface

## Estrutura do Projeto

Projeto_Clinica/
├── main.py              # Ponto de entrada da aplicação
├── config.py            # Configurações e constantes
├── modelos.py           # Estruturas de dados (Eventos, Médicos, Fila)
├── simulacao.py         # Lógica principal da simulação
├── interface.py         # Interface gráfica
├── requirements.txt     # Dependências do projeto
├── README.md            # Este ficheiro
└── venv/                # Ambiente virtual Python


## Requisitos

- Python 3.8 ou superior
- Bibliotecas Python (ver requirements.txt):
  - numpy - Cálculos numéricos e distribuições estatísticas
  - matplotlib - Geração de gráficos
  - FreeSimpleGUI - Interface gráfica

## Instalação

1. *Clonar ou descarregar o projeto*
2. *Ativar ambiente virtual*
3. *Instalar dependências*:
bash
pip install -r requirements.txt

## Execução
Para iniciar a simulação:
python main.py

A interface gráfica será aberta automaticamente.

## Funcionalidades
A simulação baseia-se num modelo de eventos discretos, onde:
-Os doentes chegam segundo uma taxa definida
-Caso não haja médicos disponíveis, os doentes entram numa fila
-Cada médico atende um doente de cada vez

O tempo de consulta segue a distribuição estatística escolhida
### Parâmetros Configuráveis

- *Número de médicos*: Define o número de médicos disponíveis para atendimento dos doentes na clínica.
- *Taxa de chegada de doentes*: Corresponde à taxa média de chegada de doentes à clínica (doentes por unidade de tempo).
- *Tempo de simulação*: Define o tempo total durante o qual a simulação decorre.
- *Distribuição de tempo de consulta*:Permite selecionar a distribuição estatística associada ao tempo de consulta: Exponencial, Normal ou Uniforme.Permite selecionar a distribuição estatística associada ao tempo de consulta:
- *Sistema de especialidades*: Permite ativar ou desativar a atribuição de médicos a especialidades específicas.

### Resultados Gerados
No final de cada simulação, são calculadas e apresentadas as seguintes métricas:
- Número total de doentes atendidos
- Tempo médio de espera na fila
- Tempo médio de consulta
- Tempo médio total de permanência na clínica
- Tamanho médio e máximo da fila de espera 
- Ocupação dos médicos (global e individual)
- Gráficos de evolução temporal
- Gráfico de relação taxa de chegada vs tamanho da fila
-Estatisticas individuais por médico 
*Resultados são:*
-Apresentados na interface gráfica 
-Guardados no ficheiro resultado.json
-Complementados com gráficos de evolução temporal e gráficos compara

## Objetivos finais
Este projeto permite analisar diferentes cenários operacionais de uma clinica médica, sendo útil para compreender o impacto de parametros como o número de médicos e a taxa de chegada no desempenho do sistema.