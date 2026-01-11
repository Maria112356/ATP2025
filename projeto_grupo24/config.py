"""
Ficheiro de configuração com os parâmetros da simulação.
"""

# Parâmetros da simulação
NUM_MEDICOS_PADRAO = 3
TAXA_CHEGADA_PADRAO = 10  # doentes por hora
TEMPO_MEDIO_CONSULTA = 15  # minutos
TEMPO_SIMULACAO_PADRAO = 8 * 60  # 8 horas em minutos
DISTRIBUICAO_TEMPO_CONSULTA = "exponential"  # exponential, normal, uniform

# Tipos de eventos
TIPO_EVENTO_CHEGADA = "chegada"
TIPO_EVENTO_SAIDA = "saída"

# Especialidades disponíveis
ESPECIALIDADES = ["Geral", "Pediatria", "Cardiologia", "Teste"]

# Ficheiros
FICHEIRO_RESULTADOS = "resultados.json"
FICHEIRO_PESSOAS = "pessoas.json"

