from dataclasses import dataclass
from typing import List, Dict

from perfil_risco import AvaliadorPerfilRisco
from relatorio import GeradorRelatorio
from persistencia import GerenciadorDados
from motor_investimento import (
    ContextoAlocacao,
    AlocacaoConservadora,
    AlocacaoModerada,
    AlocacaoArrojada
)
from orcamento import GerenciadorOrcamento
from projecao import SimuladorProjecao

@dataclass
class ResultadoSimulacao:
    """DTO atualizado para comportar os novos dados de orçamento e projeção."""
    renda_bruta: float
    total_despesas: float
    sobra_mensal: float
    perfil: str
    alocacao: Dict[str, float]
    anos_projecao: int
    patrimonio_projetado: float

class InvestPlanFacade:
    """
    Fachada principal do sistema integrando orçamento, risco, motor e projeção.
    """
    
    def __init__(self):
        self.avaliador_risco = AvaliadorPerfilRisco()
        self.gerador_relatorio = GeradorRelatorio()
        self.gerenciador_dados = GerenciadorDados()
        self.simulador_projecao = SimuladorProjecao()

    def obter_perguntas_risco(self) -> list:
        """Pede as perguntas para o avaliador e as entrega para o menu."""
        return self.avaliador_risco.obter_questionario()

    def processar_simulacao_completa(self, renda: float, despesas: Dict[str, float], respostas_risco: List[str], anos_projecao: int = 10) -> ResultadoSimulacao:
        """
        Recebe os dados brutos da interface, processa todo o fluxo orçamentário,
        define o perfil, aloca os recursos e projeta o futuro.
        """
        orcamento = GerenciadorOrcamento(renda)
        for categoria, valor in despesas.items():
            orcamento.adicionar_despesa(categoria, valor)
            
        if orcamento.verificar_orcamento_estourado():
            raise ValueError("Operação bloqueada: Suas despesas superam ou igualam sua renda atual.")

        sobra = orcamento.calcular_sobra_liquida()
        
        perfil_definido = self.avaliador_risco.calcular_perfil(respostas_risco)
        
        if perfil_definido == "conservador":
            estrategia = AlocacaoConservadora()
        elif perfil_definido == "moderado":
            estrategia = AlocacaoModerada()
        else:
            estrategia = AlocacaoArrojada() 

        motor = ContextoAlocacao(estrategia)
        alocacao_final = motor.executar_alocacao(sobra)

        patrimonio_futuro = self.simulador_projecao.calcular_patrimonio_futuro(alocacao_final, anos_projecao)

        resultado = ResultadoSimulacao(
            renda_bruta=renda,
            total_despesas=orcamento.calcular_total_despesas(),
            sobra_mensal=sobra,
            perfil=perfil_definido,
            alocacao=alocacao_final,
            anos_projecao=anos_projecao,
            patrimonio_projetado=patrimonio_futuro
        )

        dados_salvos = self.gerenciador_dados.salvar_sessao_completa(
            renda=renda,
            despesas=despesas,
            perfil=perfil_definido,
            alocacao=alocacao_final
        )
        if not dados_salvos:
            raise RuntimeError("Não foi possível salvar os dados da simulação.")
        
        self.gerador_relatorio.gerar_txt(resultado)

        return resultado
