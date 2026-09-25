import cli_utils
import csv
import os
from facade import InvestPlanFacade

def imprimir_relatorio_tela(resultado_dto) -> None:
    """Função utilitária para aplicar o princípio DRY na impressão dos resultados."""
    cli_utils.exibir_titulo("RESULTADO DA SIMULAÇÃO")
    print(f"Renda Bruta: R$ {resultado_dto.renda_bruta:.2f}")
    print(f"Total de Despesas: R$ {resultado_dto.total_despesas:.2f}")
    print(f"Sobra Líquida (Aporte Mensal): R$ {resultado_dto.sobra_mensal:.2f}")
    print("-" * 30)
    
    print(f"Perfil detectado: {resultado_dto.perfil.capitalize()}")
    print("Estratégia de Alocação Recomendada:")
    for ativo, valor in resultado_dto.alocacao.items():
        print(f"* {ativo}: R$ {valor:.2f}")
    print("-" * 30)
    
    print(f"Projeção do Patrimônio em {resultado_dto.anos_projecao} anos: R$ {resultado_dto.patrimonio_projetado:.2f}")
    print("\n[OK] Simulação salva e relatório .txt gerado com sucesso!")
    print("-" * 50)

def iniciar_sistema() -> None:
    """Ponto de entrada do sistema. Apenas instancia a Facade e o loop do menu principal."""
    facade = InvestPlanFacade()
    
    while True:
        cli_utils.exibir_titulo("INVESTPLAN - MENU PRINCIPAL")
        print("1. Iniciar Simulação Completa")
        print("2. Sair do Sistema")
        print("3. Importar Simulações em Lote (CSV)")
        
        opcao = cli_utils.ler_opcao("\nEscolha uma opção (1-3): ", ["1", "2", "3"])
        
        if opcao == "1":
            cli_utils.exibir_titulo("NOVA SIMULAÇÃO")
            try:
                renda = cli_utils.ler_float_obrigatorio("Digite sua renda bruta mensal (R$): ")
                
                despesas = {}
                print("\n--- Cadastro de Despesas ---")
                print("Digite as despesas. Pressione ENTER com a categoria vazia para finalizar.")
                while True:
                    categoria = input("Categoria da despesa (ex: Aluguel, Mercado): ").strip()
                    if not categoria:
                        break 
                    valor_despesa = cli_utils.ler_float_obrigatorio(f"Valor para '{categoria}' (R$): ")
                    categoria_normalizada = categoria.strip().lower()
                    despesas[categoria_normalizada] = despesas.get(categoria_normalizada, 0.0) + valor_despesa

                perguntas = facade.obter_perguntas_risco()
                respostas = []
                print("\n--- Questionário de Risco ---")
                for p in perguntas:
                    print(f"\n{p.id}. {p.enunciado}")
                    for letra, texto in p.opcoes.items():
                        print(f"  {letra}) {texto}")
                    resp = cli_utils.ler_opcao("Sua resposta (a/b/c): ", list(p.opcoes))
                    respostas.append(resp)
                
                print("\n--- Projeção de Patrimônio ---")
                anos_projecao = cli_utils.ler_int_positivo("Para quantos anos deseja projetar seus investimentos? (ex: 10): ")
                
                resultado_dto = facade.processar_simulacao_completa(
                    renda=renda, 
                    despesas=despesas, 
                    respostas_risco=respostas, 
                    anos_projecao=anos_projecao
                )
                
                imprimir_relatorio_tela(resultado_dto)
                
            except ValueError as e:
                cli_utils.exibir_alerta(f"Erro de validação: {e}")
            except Exception as e:
                cli_utils.exibir_alerta(f"Erro inesperado: {e}")
                
        elif opcao == "2":
            cli_utils.exibir_sucesso("Encerrando o InvestPlan. Até logo!")
            break
            
        elif opcao == "3":
            cli_utils.exibir_titulo("IMPORTAÇÃO EM LOTE VIA CSV")
            nome_arquivo = input("Digite o nome do arquivo CSV (ex: clientes_teste.csv): ").strip()
            
            caminho_completo = os.path.join(os.path.dirname(__file__), nome_arquivo)
            
            if not os.path.exists(caminho_completo):
                cli_utils.exibir_alerta(f"Arquivo '{nome_arquivo}' não encontrado na pasta do código.")
                continue
                
            try:
                with open(caminho_completo, mode='r', encoding='utf-8-sig') as arquivo_csv:
                    leitor = csv.DictReader(arquivo_csv)
                    linhas_processadas = 0
                    
                    for linha in leitor:
                        linhas_processadas += 1
                        print(f"\n>> PROCESSANDO CLIENTE #{linhas_processadas} <<")
                        
                        renda_csv = float(linha["Renda"])
                        anos_csv = int(linha["AnosProjecao"])
                        respostas_csv = [linha["Resposta1"].strip().lower(), linha["Resposta2"].strip().lower(), linha["Resposta3"].strip().lower()]
                        
                        despesas_csv = {}
                        string_despesas = linha["Despesas"].strip()
                        if string_despesas:
                            pares = string_despesas.split(";")
                            for par in pares:
                                if ":" in par:
                                    cat, val = par.split(":")
                                    categoria_normalizada = cat.strip().lower()
                                    despesas_csv[categoria_normalizada] = despesas_csv.get(categoria_normalizada, 0.0) + float(val)
                                    
                        try:
                            resultado_dto = facade.processar_simulacao_completa(
                                renda=renda_csv,
                                despesas=despesas_csv,
                                respostas_risco=respostas_csv,
                                anos_projecao=anos_csv
                            )
                            imprimir_relatorio_tela(resultado_dto)
                        except ValueError as e:
                            cli_utils.exibir_alerta(f"Erro ao processar cliente #{linhas_processadas}: {e}")
                            
                    cli_utils.exibir_sucesso(f"Processamento em Lote concluído! {linhas_processadas} simulações processadas.")
            except Exception as e:
                cli_utils.exibir_alerta(f"Erro ao ler o CSV: {e}")

if __name__ == "__main__":
    iniciar_sistema()
