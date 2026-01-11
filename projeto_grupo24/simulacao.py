"""
Módulo principal da simulação de eventos discretos da clínica.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import json
from modelos import (
    criar_evento, adicionar_evento, remover_evento,
    evento_tempo, evento_tipo, evento_id_doente,
    criar_medico, medico_ocupado, medico_id, medico_id_doente_atual,
    medico_alterar_ocupado, medico_definir_doente_atual,
    medico_atualizar_tempo_ocupado, medico_definir_inicio_consulta,
    medico_incrementar_doentes, medico_tempo_total_ocupado,
    medico_num_doentes_atendidos, medico_especialidade,
    medico_inicio_consulta_atual
)
import config


# ============================================================================
# Funções auxiliares para geração de tempos
# ============================================================================

def gerar_intervalo_chegada(taxa_chegada):
    """
    Gera um intervalo de tempo até a próxima chegada usando distribuição exponencial.
    
    Args:
        taxa_chegada: Taxa de chegada em doentes por minuto
    
    Returns:
        Intervalo de tempo em minutos
    """
    if taxa_chegada <= 0:
        return float('inf')
    return np.random.exponential(1 / taxa_chegada)

def gerar_tempo_consulta():
    """
    Gera o tempo de duração de uma consulta baseado na distribuição configurada.
    
    Returns:
        Tempo de consulta em minutos (sempre positivo)
    """
    if config.DISTRIBUICAO_TEMPO_CONSULTA == "exponential":
        return np.random.exponential(config.TEMPO_MEDIO_CONSULTA)
    elif config.DISTRIBUICAO_TEMPO_CONSULTA == "normal":
        tempo = np.random.normal(config.TEMPO_MEDIO_CONSULTA, 5)
        return max(0.1, tempo)  # Garantir que é positivo
    elif config.DISTRIBUICAO_TEMPO_CONSULTA == "uniform":
        return np.random.uniform(
            config.TEMPO_MEDIO_CONSULTA * 0.5,
            config.TEMPO_MEDIO_CONSULTA * 1.5
        )
    else:
        # Por defeito, usar exponencial
        return np.random.exponential(config.TEMPO_MEDIO_CONSULTA)


# ============================================================================
# Funções auxiliares
# ============================================================================

def procurar_medico_livre(medicos, especialidade=None):
    """
    Procura o primeiro médico livre.
    
    Args:
        medicos: Lista de médicos
        especialidade: Se especificado, procura apenas médicos dessa especialidade
    
    Returns:
        Médico livre ou None se não houver
    """
    for medico in medicos:
        if not medico_ocupado(medico):
            if especialidade is None or medico_especialidade(medico) == especialidade:
                return medico
    return None

def criar_doente(id_doente):
    """
    Cria um novo doente com características aleatórias.
    
    Args:
        id_doente: Identificador único do doente
    
    Returns:
        Dicionário com informações do doente
    """
    sexo = random.choice(["M", "F"])
    idade = random.randint(1, 90)
    quadro = random.choice(config.ESPECIALIDADES)
    return {
        "id": id_doente,
        "sexo": sexo,
        "idade": idade,
        "quadro": quadro
    }


# ============================================================================
# Função principal de simulação
# ============================================================================

def executar_simulacao(num_medicos, taxa_chegada_hora, tempo_simulacao, usar_especialidades=False):
    """
    Executa a simulação completa da clínica.
    
    Args:
        num_medicos: Número de médicos disponíveis
        taxa_chegada_hora: Taxa de chegada em doentes por hora
        tempo_simulacao: Tempo total de simulação em minutos
        usar_especialidades: Se True, médicos só atendem a sua especialidade
    
    Returns:
        Dicionário com resultados e estatísticas da simulação
    """
    # Converter taxa de chegada para minutos
    taxa_chegada = taxa_chegada_hora / 60.0
    
    # Inicialização
    tempo_atual = 0.0
    contador_doentes = 1
    doentes = {}
    fila_eventos = []
    fila_espera = []  # Fila de doentes à espera: [(id_doente, tempo_chegada), ...]
    
    # Estruturas para estatísticas
    tempos_fila = [0.0]
    tamanhos_fila = [0]
    tempos_medicos = [0.0]
    medicos_ocupados = [0]
    
    # Rastreamento de tempos de espera e na clínica
    tempos_espera = []  # Tempo de espera de cada doente
    tempos_na_clinica = []  # Tempo total na clínica de cada doente
    tempos_consulta = []  # Tempo de consulta de cada doente
    chegadas_doentes = {}  # {id_doente: tempo_chegada}
    inicio_atendimento = {}  # {id_doente: tempo_inicio_atendimento}
    
    # Criar médicos
    medicos = []
    for i in range(num_medicos):
        especialidade = random.choice(config.ESPECIALIDADES)
        medico = criar_medico(f"m{i}", especialidade)
        medicos.append(medico)
    
    # Gerar eventos de chegada
    tempo_proxima_chegada = gerar_intervalo_chegada(taxa_chegada)
    while tempo_proxima_chegada < tempo_simulacao:
        id_doente = f"d{contador_doentes}"
        doentes[id_doente] = criar_doente(id_doente)
        chegadas_doentes[id_doente] = tempo_proxima_chegada
        contador_doentes += 1
        
        evento_chegada = criar_evento(
            tempo_proxima_chegada,
            config.TIPO_EVENTO_CHEGADA,
            id_doente
        )
        fila_eventos = adicionar_evento(fila_eventos, evento_chegada)
        
        tempo_proxima_chegada += gerar_intervalo_chegada(taxa_chegada)
    
    # Processar eventos
    doentes_atendidos = 0
    
    while fila_eventos != []:
        evento, fila_eventos = remover_evento(fila_eventos)
        tempo_atual = evento_tempo(evento)
        tipo_evento = evento_tipo(evento)
        id_doente = evento_id_doente(evento)
        
        # Atualizar estatísticas de ocupação dos médicos
        ocupados = sum(1 for m in medicos if medico_ocupado(m))
        tempos_medicos.append(tempo_atual)
        medicos_ocupados.append(ocupados)
        
        if tipo_evento == config.TIPO_EVENTO_CHEGADA:
            # Doente chegou
            especialidade_necessaria = None
            if usar_especialidades:
                especialidade_necessaria = doentes[id_doente]["quadro"]
            
            medico_livre = procurar_medico_livre(medicos, especialidade_necessaria)
            
            if medico_livre is not None:
                # Atender imediatamente (sem espera)
                inicio_atendimento[id_doente] = tempo_atual
                tempo_espera = 0.0
                tempos_espera.append(tempo_espera)
                
                medico_livre = medico_alterar_ocupado(medico_livre, True)
                medico_livre = medico_definir_inicio_consulta(medico_livre, tempo_atual)
                medico_livre = medico_definir_doente_atual(medico_livre, id_doente)
                
                # Atualizar o médico na lista
                for i, m in enumerate(medicos):
                    if medico_id(m) == medico_id(medico_livre):
                        medicos[i] = medico_livre
                        
                
                # Agendar saída
                tempo_consulta = gerar_tempo_consulta()
                tempo_saida = tempo_atual + tempo_consulta
                evento_saida = criar_evento(tempo_saida, config.TIPO_EVENTO_SAIDA, id_doente)
                fila_eventos = adicionar_evento(fila_eventos, evento_saida)
            else:
                # Adicionar à fila de espera
                fila_espera.append((id_doente, tempo_atual))
                tamanhos_fila.append(len(fila_espera))
                tempos_fila.append(tempo_atual)
        
        elif tipo_evento == config.TIPO_EVENTO_SAIDA:
            # Consulta terminou
            doentes_atendidos += 1
            
            # Calcular estatísticas do doente
            tempo_chegada = chegadas_doentes.get(id_doente, tempo_atual)
            tempo_inicio_atendimento = inicio_atendimento.get(id_doente, tempo_atual)
            tempo_espera_doente = tempo_inicio_atendimento - tempo_chegada
            
            # Encontrar e libertar o médico
            medico_encontrado = None
            indice_medico = -1
            
            for i, medico in enumerate(medicos):
                if medico_id_doente_atual(medico) == id_doente and medico_encontrado is None:
                    medico_encontrado = medico
                    indice_medico = i
                
            
            if medico_encontrado is not None:
                # Calcular tempo da consulta
                tempo_consulta = tempo_atual - medico_inicio_consulta_atual(medico_encontrado)
                tempos_consulta.append(tempo_consulta)
                
                # Calcular tempo total na clínica
                tempo_total_clinica = tempo_atual - tempo_chegada
                tempos_na_clinica.append(tempo_total_clinica)
                
                # Se ainda não foi registado o tempo de espera, registar agora
                if id_doente not in inicio_atendimento or tempo_espera_doente > 0:
                    tempos_espera.append(tempo_espera_doente)
                
                # Atualizar estatísticas do médico
                medico_encontrado = medico_atualizar_tempo_ocupado(medico_encontrado, tempo_consulta)
                medico_encontrado = medico_incrementar_doentes(medico_encontrado)
                medico_encontrado = medico_alterar_ocupado(medico_encontrado, False)
                medico_encontrado = medico_definir_doente_atual(medico_encontrado, None)
                
                medicos[indice_medico] = medico_encontrado
                
                # Se há doentes à espera, atender o próximo
                if fila_espera != []:
                    id_proximo_doente, tempo_chegada_proximo = fila_espera.pop(0)
                    
                    # Verificar especialidade se necessário
                    especialidade_necessaria = None
                    if usar_especialidades:
                        especialidade_necessaria = doentes[id_proximo_doente]["quadro"]
                    
                    # Só atender se a especialidade corresponder (ou se não usar especialidades)
                    pode_atender = (not usar_especialidades or 
                                  medico_especialidade(medico_encontrado) == especialidade_necessaria)
                    
                    if pode_atender:
                        # Registar início do atendimento e calcular tempo de espera
                        inicio_atendimento[id_proximo_doente] = tempo_atual
                        tempo_espera_proximo = tempo_atual - tempo_chegada_proximo
                        tempos_espera.append(tempo_espera_proximo)
                        
                        medico_encontrado = medico_alterar_ocupado(medico_encontrado, True)
                        medico_encontrado = medico_definir_inicio_consulta(medico_encontrado, tempo_atual)
                        medico_encontrado = medico_definir_doente_atual(medico_encontrado, id_proximo_doente)
                        
                        medicos[indice_medico] = medico_encontrado
                        
                        # Agendar saída
                        tempo_consulta = gerar_tempo_consulta()
                        tempo_saida = tempo_atual + tempo_consulta
                        evento_saida = criar_evento(tempo_saida, config.TIPO_EVENTO_SAIDA, id_proximo_doente)
                        fila_eventos = adicionar_evento(fila_eventos, evento_saida)
                    else:
                        # Não pode atender, volta para a fila
                        fila_espera.insert(0, (id_proximo_doente, tempo_chegada_proximo))
    
    
    if 'tempo_atual' in locals():
        tempo_fim_simulacao = max(tempo_atual, tempo_simulacao)
    else:
        tempo_fim_simulacao = tempo_simulacao
    
    for id_doente_fila, tempo_chegada_fila in fila_espera:
        tempo_espera_final = tempo_fim_simulacao - tempo_chegada_fila
        if tempo_espera_final > 0:  # Só adicionar se realmente esperou
            tempos_espera.append(tempo_espera_final)
    
    # Calcular estatísticas finais
    resultados = calcular_estatisticas(
        medicos, doentes_atendidos, tempo_simulacao,
        tamanhos_fila, tempos_fila, tempos_medicos, medicos_ocupados,
        tempos_espera, tempos_na_clinica, tempos_consulta
    )
    
    return resultados


# ============================================================================
# Funções de estatísticas e visualização
# ============================================================================

def calcular_estatisticas(medicos, doentes_atendidos, tempo_simulacao,
                         tamanhos_fila, tempos_fila, tempos_medicos, medicos_ocupados,
                         tempos_espera, tempos_na_clinica, tempos_consulta):
    """
    Calcula todas as estatísticas da simulação.
    """
    resultados = {
        "doentes_atendidos": doentes_atendidos,
        "tempo_simulacao": tempo_simulacao
    }
    
    # Estatísticas da fila
    if tamanhos_fila:
        resultados["tamanho_medio_fila"] = sum(tamanhos_fila) / len(tamanhos_fila)
        resultados["tamanho_maximo_fila"] = max(tamanhos_fila)
    else:
        resultados["tamanho_medio_fila"] = 0
        resultados["tamanho_maximo_fila"] = 0
    
    # Tempo médio de espera
    if tempos_espera:
        resultados["tempo_medio_espera"] = sum(tempos_espera) / len(tempos_espera)
        resultados["tempo_maximo_espera"] = max(tempos_espera)
    else:
        resultados["tempo_medio_espera"] = 0
        resultados["tempo_maximo_espera"] = 0
    
    # Tempo médio de consulta
    if tempos_consulta:
        resultados["tempo_medio_consulta"] = sum(tempos_consulta) / len(tempos_consulta)
        resultados["tempo_maximo_consulta"] = max(tempos_consulta)
    else:
        resultados["tempo_medio_consulta"] = 0
        resultados["tempo_maximo_consulta"] = 0
    
    # Tempo médio na clínica
    if tempos_na_clinica:
        resultados["tempo_medio_na_clinica"] = sum(tempos_na_clinica) / len(tempos_na_clinica)
        resultados["tempo_maximo_na_clinica"] = max(tempos_na_clinica)
    else:
        resultados["tempo_medio_na_clinica"] = 0
        resultados["tempo_maximo_na_clinica"] = 0
    
    # Estatísticas por médico
    estatisticas_medicos = []
    for medico in medicos:
        tempo_ocupado = medico_tempo_total_ocupado(medico)
        percentagem_ocupacao = (tempo_ocupado / tempo_simulacao) * 100 if tempo_simulacao > 0 else 0
        
        estatisticas_medicos.append({
            "medico": medico_id(medico),
            "especialidade": medico_especialidade(medico),
            "doentes_atendidos": medico_num_doentes_atendidos(medico),
            "tempo_ocupado": round(tempo_ocupado, 2),
            "percentagem_ocupacao": round(percentagem_ocupacao, 2)
        })
    
    resultados["estatisticas_por_medico"] = estatisticas_medicos
    
    # Dados para gráficos
    resultados["dados_graficos"] = {
        "tempos_fila": tempos_fila,
        "tamanhos_fila": tamanhos_fila,
        "tempos_medicos": tempos_medicos,
        "medicos_ocupados": medicos_ocupados
    }
    
    return resultados

def gerar_graficos(resultados, mostrar_graficos=True):
    """
    Gera os gráficos da simulação.
    """
    dados = resultados.get("dados_graficos", {})
    
    if not dados:
        return
    
    tempos_fila = dados.get("tempos_fila", [])
    tamanhos_fila = dados.get("tamanhos_fila", [])
    tempos_medicos = dados.get("tempos_medicos", [])
    medicos_ocupados = dados.get("medicos_ocupados", [])
    
    # Gráfico da evolução da fila
    if tempos_fila and tamanhos_fila:
        plt.figure(figsize=(10, 6))
        plt.plot(tempos_fila, tamanhos_fila)
        plt.xlabel("Tempo (minutos)")
        plt.ylabel("Tamanho da fila")
        plt.title("Evolução do tamanho da fila de espera")
        plt.grid(True)
        if mostrar_graficos:
            plt.show()
    
    # Gráfico da ocupação dos médicos
    if tempos_medicos and medicos_ocupados:
        plt.figure(figsize=(10, 6))
        plt.plot(tempos_medicos, medicos_ocupados)
        plt.xlabel("Tempo (minutos)")
        plt.ylabel("Número de médicos ocupados")
        plt.title("Evolução da ocupação dos médicos")
        plt.grid(True)
        if mostrar_graficos:
            plt.show()

def gerar_grafico_taxa_vs_fila(num_medicos=3, tempo_simulacao=480, 
                               taxas_min=10, taxas_max=30, passo=5,
                               usar_especialidades=False, mostrar_grafico=True):
    """
    Gera gráfico da relação entre taxa de chegada e tamanho médio da fila.
    Varia a taxa de chegada entre taxas_min e taxas_max.
    
    Args:
        num_medicos: Número de médicos
        tempo_simulacao: Tempo de simulação em minutos
        taxas_min: Taxa mínima de chegada (doentes/hora)
        taxas_max: Taxa máxima de chegada (doentes/hora)
        passo: Incremento da taxa
        usar_especialidades: Se deve usar sistema de especialidades
        mostrar_grafico: Se deve mostrar o gráfico
    
    Returns:
        Tuplo (taxas, tamanhos_medios_fila)
    """
    taxas = list(range(taxas_min, taxas_max + 1, passo))
    tamanhos_medios_fila = []
    
    print(f"\nA gerar gráfico de relação taxa vs fila...")
    print(f"Testando {len(taxas)} valores de taxa de chegada...")
    
    for taxa in taxas:
        print(f"  Testando taxa: {taxa} doentes/hora...", end=" ")
        resultados = executar_simulacao(
            num_medicos=num_medicos,
            taxa_chegada_hora=taxa,
            tempo_simulacao=tempo_simulacao,
            usar_especialidades=usar_especialidades
        )
        tamanho_medio = resultados.get("tamanho_medio_fila", 0)
        tamanhos_medios_fila.append(tamanho_medio)
        print(f"Fila média: {tamanho_medio:.2f}")
    
    # Gerar gráfico
    if mostrar_grafico:
        plt.figure(figsize=(10, 6))
        plt.plot(taxas, tamanhos_medios_fila, marker="o", linewidth=2, markersize=8)
        plt.xlabel("Taxa de chegada (doentes/hora)")
        plt.ylabel("Tamanho médio da fila")
        plt.title("Relação entre taxa de chegada e tamanho médio da fila de espera")
        plt.grid(True, alpha=0.3)
        plt.show()
    
    return taxas, tamanhos_medios_fila

def guardar_resultados(resultados, nome_ficheiro=None):
    """
    Guarda os resultados da simulação num ficheiro JSON.
    """
    if nome_ficheiro is None:
        nome_ficheiro = config.FICHEIRO_RESULTADOS
    
    # Remover dados de gráficos antes de guardar (são muito grandes)
    resultados_para_guardar = resultados.copy()
    resultados_para_guardar.pop("dados_graficos", None)
    
    try:
        with open(nome_ficheiro, "w", encoding="utf-8") as f:
            json.dump(resultados_para_guardar, f, indent=4, ensure_ascii=False)
        print(f"Resultados guardados em {nome_ficheiro}")
        return True
    except Exception as e:
        print(f"Erro ao guardar resultados: {e}")
        return False

def imprimir_estatisticas(resultados):
    """
    Imprime as estatísticas da simulação de forma formatada.
    """
    print("\n" + "="*60)
    print("ESTATÍSTICAS DA SIMULAÇÃO")
    print("="*60)
    
    print(f"\nDoentes atendidos: {resultados['doentes_atendidos']}")
    print(f"Tempo de simulação: {resultados['tempo_simulacao']} minutos")
    print(f"\n--- Estatísticas da Fila ---")
    print(f"Tamanho médio da fila: {resultados['tamanho_medio_fila']:.2f}")
    print(f"Tamanho máximo da fila: {resultados['tamanho_maximo_fila']}")
    print(f"\n--- Tempos ---")
    print(f"Tempo médio de espera: {resultados['tempo_medio_espera']:.2f} minutos")
    print(f"Tempo máximo de espera: {resultados['tempo_maximo_espera']:.2f} minutos")
    print(f"Tempo médio de consulta: {resultados['tempo_medio_consulta']:.2f} minutos")
    print(f"Tempo máximo de consulta: {resultados['tempo_maximo_consulta']:.2f} minutos")
    print(f"Tempo médio na clínica: {resultados['tempo_medio_na_clinica']:.2f} minutos")
    print(f"Tempo máximo na clínica: {resultados['tempo_maximo_na_clinica']:.2f} minutos")
    
    print("\n--- Estatísticas por médico ---")
    for estat in resultados["estatisticas_por_medico"]:
        print(f"Médico {estat['medico']} ({estat['especialidade']}):")
        print(f"  - Doentes atendidos: {estat['doentes_atendidos']}")
        print(f"  - Percentagem de ocupação: {estat['percentagem_ocupacao']:.1f}%")
    
    print("="*60 + "\n")

