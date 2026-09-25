import os
from datetime import datetime

class GeradorRelatorio:
    """
    Responsável por formatar os dados finais em texto e salvar no disco
    utilizando a técnica de escrita atômica para evitar corrupção de arquivos.
    """
    
    def __init__(self, caminho_arquivo: str = None):
        if caminho_arquivo is None:
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            self.caminho_arquivo = os.path.join(diretorio_atual, "plano_investplan.txt")
        else:
            self.caminho_arquivo = caminho_arquivo

    def gerar_txt(self, resultado_simulacao) -> bool:
        """
        Recebe o DTO com o resultado da simulação, formata e salva de forma atômica.
        """
        def formatar_br(valor: float) -> str:
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        linhas = [
            "=" * 50,
            "         RELATÓRIO DE INVESTIMENTO - INVESTPLAN",
            "=" * 50,
            f"Data da Simulação: {data_atual}",
            f"Renda Bruta: R$ {formatar_br(resultado_simulacao.renda_bruta)}",
            f"Total de Despesas: R$ {formatar_br(resultado_simulacao.total_despesas)}",
            f"Sobra Orçamentária: R$ {formatar_br(resultado_simulacao.sobra_mensal)}",
            f"Perfil de Risco: {resultado_simulacao.perfil.upper()}",
            "-" * 50,
            "SUA ALOCAÇÃO RECOMENDADA:",
        ]

        for ativo, valor in resultado_simulacao.alocacao.items():
            linhas.append(f"  * {ativo}: R$ {formatar_br(valor)}")
            
        linhas.append("-" * 50)
        linhas.append(f"Projeção do Patrimônio em {resultado_simulacao.anos_projecao} anos: R$ {formatar_br(resultado_simulacao.patrimonio_projetado)}")
        linhas.append("-" * 50)
        linhas.append("Lembre-se: Invista com responsabilidade e consistência.")
        linhas.append("=" * 50)

        conteudo_texto = "\n".join(linhas)
        caminho_temporario = f"{self.caminho_arquivo}.tmp"
        
        try:
            with open(caminho_temporario, "w", encoding="utf-8") as arquivo_tmp:
                arquivo_tmp.write(conteudo_texto)
                arquivo_tmp.flush()
                os.fsync(arquivo_tmp.fileno())

            os.replace(caminho_temporario, self.caminho_arquivo)
            return True
            
        except Exception as erro:
            if os.path.exists(caminho_temporario):
                os.remove(caminho_temporario)
            
            raise RuntimeError(f"Erro crítico ao exportar relatório atômico: {erro}")
