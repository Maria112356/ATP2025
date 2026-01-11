"""
Módulo com as estruturas de dados e funções de manipulação.
Define os modelos para Eventos, Médicos e a Fila de Eventos.
"""

# ============================================================================
# MODELO: Evento
# Evento = (tempo: float, tipo: str, id_doente: str)
# ============================================================================

def evento_tempo(evento):
    """Retorna o tempo do evento."""
    return evento[0]

def evento_tipo(evento):
    """Retorna o tipo do evento."""
    return evento[1]

def evento_id_doente(evento):
    """Retorna o ID do doente do evento."""
    return evento[2]

def criar_evento(tempo, tipo, id_doente):
    """Cria um novo evento."""
    return (tempo, tipo, id_doente)


# ============================================================================
# MODELO: Fila de Eventos
# Fila ordenada por tempo de ocorrência
# ============================================================================

def procurar_posicao_fila(fila_eventos, tempo):
    """
    Procura a posição correta para inserir um evento na fila,
    mantendo a ordem cronológica.
    """
    i = 0
    while i < len(fila_eventos) and tempo > fila_eventos[i][0]:
        i = i + 1
    return i

def adicionar_evento(fila_eventos, evento):
    """
    Adiciona um evento à fila, mantendo a ordem cronológica.
    """
    posicao = procurar_posicao_fila(fila_eventos, evento_tempo(evento))
    return fila_eventos[:posicao] + [evento] + fila_eventos[posicao:]

def remover_evento(fila_eventos):
    """
    Remove e retorna o primeiro evento da fila (o mais próximo no tempo).
    """
    if fila_eventos == []:
        return None, []
    evento = fila_eventos[0]
    nova_fila = fila_eventos[1:]
    return evento, nova_fila


# ============================================================================
# MODELO: Médico
# Médico = [id: str, ocupado: bool, id_doente_atual: str, 
#           tempo_total_ocupado: float, inicio_consulta_atual: float,
#           num_doentes_atendidos: int, especialidade: str]
# ============================================================================

def medico_id(medico):
    """Retorna o ID do médico."""
    return medico[0]

def medico_ocupado(medico):
    """Retorna True se o médico está ocupado."""
    return medico[1]

def medico_id_doente_atual(medico):
    """Retorna o ID do doente que o médico está a atender."""
    return medico[2]

def medico_tempo_total_ocupado(medico):
    """Retorna o tempo total que o médico esteve ocupado."""
    return medico[3]

def medico_inicio_consulta_atual(medico):
    """Retorna o tempo de início da consulta atual."""
    return medico[4]

def medico_num_doentes_atendidos(medico):
    """Retorna o número de doentes atendidos pelo médico."""
    return medico[5]

def medico_especialidade(medico):
    """Retorna a especialidade do médico."""
    return medico[6]

def medico_alterar_ocupado(medico, ocupado):
    """Altera o estado de ocupação do médico."""
    medico[1] = ocupado
    return medico

def medico_definir_doente_atual(medico, id_doente):
    """Define qual doente o médico está a atender."""
    medico[2] = id_doente
    return medico

def medico_atualizar_tempo_ocupado(medico, tempo_adicional):
    """Adiciona tempo ao tempo total ocupado do médico."""
    medico[3] = medico[3] + tempo_adicional
    return medico

def medico_definir_inicio_consulta(medico, tempo):
    """Define o tempo de início da consulta atual."""
    medico[4] = tempo
    return medico

def medico_incrementar_doentes(medico):
    """Incrementa o contador de doentes atendidos."""
    medico[5] = medico[5] + 1
    return medico

def criar_medico(id_medico, especialidade):
    """
    Cria um novo médico com os valores iniciais.
    """
    return [id_medico, False, None, 0.0, 0.0, 0, especialidade]

