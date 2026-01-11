"""
Módulo da interface gráfica usando FreeSimpleGUI.
"""

import FreeSimpleGUI as sg
import simulacao
import config
from datetime import datetime


def formatar_resultados_texto(resultados, parametros=None):
    """
    Formata os resultados da simulação como texto para exibir no log.
    
    Args:
        resultados: Dicionário com os resultados da simulação
        parametros: Dicionário opcional com os parâmetros usados
    
    Returns:
        String formatada com os resultados
    """
    texto = []
    texto.append("=" * 60)
    texto.append("RESULTADOS / LOG")
    texto.append("=" * 60)
    texto.append("")
    
    # Parâmetros
    if parametros:
        texto.append("=== PARÂMETROS ===")
        taxa = parametros.get('taxa_chegada', None)
        if taxa is not None:
            texto.append(f"λ (doentes/hora): {taxa:.2f}")
        else:
            texto.append(f"λ (doentes/hora): N/A")
        texto.append(f"Nº médicos: {parametros.get('num_medicos', 'N/A')}")
        texto.append(f"Distribuição consulta: {parametros.get('distribuicao', 'N/A')}")
        if 'tempo_medio_consulta' in parametros:
            texto.append(f"Média consulta (min): {parametros['tempo_medio_consulta']:.1f}")
        tempo_sim = parametros.get('tempo_simulacao', None)
        if tempo_sim is not None:
            texto.append(f"Tempo simulação (min): {tempo_sim:.1f}")
        else:
            texto.append(f"Tempo simulação (min): N/A")
        texto.append("")
    
    # Resultados principais
    texto.append("=== RESULTADOS ===")
    texto.append(f"Doentes atendidos: {resultados.get('doentes_atendidos', 0)}")
    texto.append(f"Tempo médio espera (min): {resultados.get('tempo_medio_espera', 0):.2f}")
    texto.append(f"Tempo médio consulta (min): {resultados.get('tempo_medio_consulta', 0):.2f}")
    texto.append(f"Tempo médio na clínica (min): {resultados.get('tempo_medio_na_clinica', 0):.2f}")
    texto.append(f"Fila média (média temporal): {resultados.get('tamanho_medio_fila', 0):.2f}")
    texto.append(f"Fila máxima: {resultados.get('tamanho_maximo_fila', 0)}")
    
    # Ocupação global
    tempo_simulacao = resultados.get('tempo_simulacao', 1)
    ocupacao_global = 0
    if 'estatisticas_por_medico' in resultados and resultados['estatisticas_por_medico']:
        ocupacoes = [m['percentagem_ocupacao'] for m in resultados['estatisticas_por_medico']]
        ocupacao_global = sum(ocupacoes) / len(ocupacoes) if ocupacoes else 0
    texto.append(f"Ocupação global (%): {ocupacao_global:.2f}")
    texto.append("")
    
    # Estatísticas por médico
    if 'estatisticas_por_medico' in resultados and resultados['estatisticas_por_medico']:
        texto.append("=== OCUPAÇÃO POR MÉDICO (%) ===")
        for estat in resultados['estatisticas_por_medico']:
            texto.append(f"{estat['medico']}: {estat['percentagem_ocupacao']:.2f}")
        texto.append("")
    
    texto.append("=" * 60)
    texto.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    texto.append("")
    
    return "\n".join(texto)


def validar_entrada_numero(valor, nome_campo, valor_minimo=1):
    """
    Valida se uma entrada é um número válido.
    
    Args:
        valor: Valor a validar
        nome_campo: Nome do campo (para mensagens de erro)
        valor_minimo: Valor mínimo aceitável
    
    Returns:
        Tuplo (sucesso: bool, valor: float ou None, mensagem_erro: str)
    """
    if valor is None or valor.strip() == "":
        return False, None, f"O campo '{nome_campo}' não pode estar vazio."
    
    try:
        numero = float(valor)
        if numero < valor_minimo:
            return False, None, f"O campo '{nome_campo}' deve ser pelo menos {valor_minimo}."
        return True, numero, ""
    except ValueError:
        return False, None, f"O campo '{nome_campo}' deve ser um número válido."


def criar_janela_principal():
    """
    Cria e retorna a janela principal da aplicação.
    """
    # Definir tema personalizado: fundo branco, texto preto, botões azuis
    sg.theme("LightBlue1")  # Tema base claro
    
    # Cores personalizadas
    cor_fundo = "#FFFFFF"
    cor_texto = "#000000"
    cor_botao = "#0066CC"
    cor_texto_botao = "#FFFFFF"
    
    layout = [
        [sg.Text("Simulação de Clínica", 
                font=("Helvetica", 16, "bold"), 
                text_color=cor_texto, 
                background_color=cor_fundo)],
        [sg.Text("_" * 80, text_color=cor_texto, background_color=cor_fundo)],
        [
            sg.Column([
                [sg.Text("Número de médicos:", size=(25, 1), text_color=cor_texto, background_color=cor_fundo), 
                 sg.Input(key="-MEDICOS-", default_text=str(config.NUM_MEDICOS_PADRAO), size=(10, 1))],
                [sg.Text("Taxa de chegada (doentes/hora):", size=(25, 1), text_color=cor_texto, background_color=cor_fundo), 
                 sg.Input(key="-TAXA-", default_text=str(config.TAXA_CHEGADA_PADRAO), size=(10, 1))],
                [sg.Text("Tempo de simulação (horas):", size=(25, 1), text_color=cor_texto, background_color=cor_fundo), 
                 sg.Input(key="-TEMPO-", default_text="8", size=(10, 1))],
                [sg.Text("Distribuição tempo consulta:", size=(25, 1), text_color=cor_texto, background_color=cor_fundo),
                 sg.Combo(["exponential", "normal", "uniform"], 
                         default_value=config.DISTRIBUICAO_TEMPO_CONSULTA,
                         key="-DISTRIBUICAO-", size=(15, 1))],
                [sg.Checkbox("Usar sistema de especialidades", 
                           key="-ESPECIALIDADES-", 
                           default=False,
                           text_color=cor_texto,
                           background_color=cor_fundo)],
                [sg.Text("_" * 80, text_color=cor_texto, background_color=cor_fundo)],
                [sg.Button("Executar Simulação", 
                          key="-EXECUTAR-", 
                          size=(20, 1),
                          button_color=(cor_texto_botao, cor_botao)),
                 sg.Button("Gráfico Taxa vs Fila", 
                          key="-GRAFICO_TAXA-", 
                          size=(20, 1),
                          button_color=(cor_texto_botao, cor_botao))],
                [sg.Button("Cancelar", 
                          key="-CANCELAR-", 
                          size=(15, 1),
                          button_color=(cor_texto_botao, cor_botao))],
                [sg.Text("", key="-STATUS-", size=(50, 2), text_color=cor_texto, background_color=cor_fundo)]
            ], background_color=cor_fundo, pad=(10, 10)),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Text("Resultados / Log", 
                        font=("Helvetica", 12, "bold"),
                        text_color=cor_texto,
                        background_color=cor_fundo)],
                [sg.Multiline("Bem-vindo à Simulação de Clínica!\n\n"
                            "Configure os parâmetros e clique em 'Executar Simulação' para começar.\n\n"
                            "Os resultados aparecerão aqui após a execução.",
                            key="-LOG-",
                            size=(50, 25),
                            autoscroll=True,
                            disabled=True,
                            text_color=cor_texto,
                            background_color="#F5F5F5",
                            font=("Courier", 9))]
            ], background_color=cor_fundo, pad=(10, 10))
        ]
    ]
    
    return sg.Window("Simulação Clínica", 
                    layout, 
                    finalize=True,
                    background_color=cor_fundo,
                    resizable=True)


def executar_interface():
    """
    Executa a interface gráfica principal.
    """
    janela = criar_janela_principal()
    a_correr= True
    while a_correr:
        evento, valores = janela.read()
        
        if evento in (sg.WIN_CLOSED, "-CANCELAR-"):
            a_correr= False
        
        elif evento == "-EXECUTAR-":
            # Validar entradas
            sucesso_medicos, num_medicos, msg_medicos = validar_entrada_numero(
                valores["-MEDICOS-"], "Número de médicos", valor_minimo=1
            )
            
            sucesso_taxa, taxa_chegada, msg_taxa = validar_entrada_numero(
                valores["-TAXA-"], "Taxa de chegada", valor_minimo=0.1
            )
            
            sucesso_tempo, tempo_horas, msg_tempo = validar_entrada_numero(
                valores["-TEMPO-"], "Tempo de simulação", valor_minimo=0.1
            )
            
            # Verificar se todas as validações passaram
            if not (sucesso_medicos and sucesso_taxa and sucesso_tempo):
                mensagem_erro = "Erros de validação:\n"
                if not sucesso_medicos:
                    mensagem_erro += f"- {msg_medicos}\n"
                if not sucesso_taxa:
                    mensagem_erro += f"- {msg_taxa}\n"
                if not sucesso_tempo:
                    mensagem_erro += f"- {msg_tempo}\n"
                
                janela["-STATUS-"].update(mensagem_erro)
                sg.popup_error("Erro de Validação", mensagem_erro)
                continue
            
            # Converter tempo de horas para minutos
            tempo_simulacao = tempo_horas * 60
            num_medicos = int(num_medicos)
            usar_especialidades = valores["-ESPECIALIDADES-"]
            distribuicao = valores["-DISTRIBUICAO-"]
            
            # Atualizar distribuição global
            config.DISTRIBUICAO_TEMPO_CONSULTA = distribuicao
            
            # Atualizar status
            janela["-STATUS-"].update("A executar simulação... Por favor aguarde.")
            janela.refresh()
            
            try:
                # Preparar parâmetros para o log
                parametros_log = {
                    'num_medicos': num_medicos,
                    'taxa_chegada': taxa_chegada,
                    'tempo_simulacao': tempo_simulacao,
                    'distribuicao': distribuicao,
                    'tempo_medio_consulta': config.TEMPO_MEDIO_CONSULTA
                }
                
                # Atualizar log com início da simulação
                janela["-LOG-"].update("A executar simulação...\nPor favor aguarde.\n\n")
                janela.refresh()
                
                # Executar simulação
                resultados = simulacao.executar_simulacao(
                    num_medicos=num_medicos,
                    taxa_chegada_hora=taxa_chegada,
                    tempo_simulacao=tempo_simulacao,
                    usar_especialidades=usar_especialidades
                )
                
                # Formatar e exibir resultados no log
                texto_resultados = formatar_resultados_texto(resultados, parametros_log)
                janela["-LOG-"].update(texto_resultados)
                janela.refresh()
                
                # Imprimir estatísticas no terminal também (para compatibilidade)
                simulacao.imprimir_estatisticas(resultados)
                
                # Gerar gráficos
                simulacao.gerar_graficos(resultados, mostrar_graficos=True)
                
                # Guardar resultados
                simulacao.guardar_resultados(resultados)
                
                # Atualizar status
                mensagem_sucesso = f"Simulação concluída!\nDoentes atendidos: {resultados['doentes_atendidos']}"
                janela["-STATUS-"].update(mensagem_sucesso)
                
                sg.popup("Simulação Concluída", 
                        f"A simulação foi executada com sucesso.\n\n"
                        f"Doentes atendidos: {resultados['doentes_atendidos']}\n"
                        f"Tamanho médio da fila: {resultados['tamanho_medio_fila']:.2f}\n\n"
                        f"Resultados guardados em {config.FICHEIRO_RESULTADOS}")
                
            except Exception as e:
                mensagem_erro = f"Erro durante a simulação:\n{str(e)}"
                janela["-STATUS-"].update(mensagem_erro)
                janela["-LOG-"].update(f"ERRO:\n{mensagem_erro}\n\nVerifique os parâmetros e tente novamente.")
                sg.popup_error("Erro", mensagem_erro)
        
        elif evento == "-GRAFICO_TAXA-":
            # Validar entradas para o gráfico
            sucesso_medicos, num_medicos, msg_medicos = validar_entrada_numero(
                valores["-MEDICOS-"], "Número de médicos", valor_minimo=1
            )
            
            sucesso_tempo, tempo_horas, msg_tempo = validar_entrada_numero(
                valores["-TEMPO-"], "Tempo de simulação", valor_minimo=0.1
            )
            
            if not (sucesso_medicos and sucesso_tempo):
                mensagem_erro = "Erros de validação:\n"
                if not sucesso_medicos:
                    mensagem_erro += f"- {msg_medicos}\n"
                if not sucesso_tempo:
                    mensagem_erro += f"- {msg_tempo}\n"
                
                janela["-STATUS-"].update(mensagem_erro)
                sg.popup_error("Erro de Validação", mensagem_erro)
                continue
            
            tempo_simulacao = tempo_horas * 60
            num_medicos = int(num_medicos)
            usar_especialidades = valores["-ESPECIALIDADES-"]
            distribuicao = valores["-DISTRIBUICAO-"]
            
            # Atualizar distribuição global
            config.DISTRIBUICAO_TEMPO_CONSULTA = distribuicao
            
            # Atualizar status
            janela["-STATUS-"].update("A gerar gráfico de relação taxa vs fila...\nIsto pode demorar alguns minutos.")
            janela.refresh()
            
            try:
                # Atualizar log
                janela["-LOG-"].update("A gerar gráfico de relação taxa vs fila...\nIsto pode demorar alguns minutos.\n\n")
                janela.refresh()
                
                # Gerar gráfico de relação
                taxas, tamanhos_medios = simulacao.gerar_grafico_taxa_vs_fila(
                    num_medicos=num_medicos,
                    tempo_simulacao=tempo_simulacao,
                    taxas_min=10,
                    taxas_max=30,
                    passo=5,
                    usar_especialidades=usar_especialidades,
                    mostrar_grafico=True
                )
                
                # Atualizar log com resultados do gráfico
                texto_grafico = "=== GRÁFICO TAXA VS FILA ===\n\n"
                texto_grafico += "Taxa (doentes/hora) | Fila Média\n"
                texto_grafico += "-" * 35 + "\n"
                for taxa, tamanho in zip(taxas, tamanhos_medios):
                    texto_grafico += f"{taxa:>20} | {tamanho:>10.2f}\n"
                texto_grafico += "\nGráfico gerado com sucesso!\n"
                texto_grafico += f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                janela["-LOG-"].update(texto_grafico)
                janela["-STATUS-"].update("Gráfico de relação taxa vs fila gerado com sucesso!")
                sg.popup("Gráfico Gerado", 
                        "O gráfico da relação entre taxa de chegada e tamanho médio da fila foi gerado com sucesso.")
                
            except Exception as e:
                mensagem_erro = f"Erro ao gerar gráfico:\n{str(e)}"
                janela["-STATUS-"].update(mensagem_erro)
                janela["-LOG-"].update(f"ERRO ao gerar gráfico:\n{mensagem_erro}\n")
                sg.popup_error("Erro", mensagem_erro)
    
    janela.close()

