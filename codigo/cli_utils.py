import math

def ler_float_obrigatorio(mensagem_prompt: str) -> float:
    """Lê um número decimal finito e positivo do terminal."""
    while True:
        try:
            entrada_usuario = input(mensagem_prompt).strip().replace(",", ".")
            valor_convertido = float(entrada_usuario)
            if not math.isfinite(valor_convertido):
                print("[!] Erro: O valor informado deve ser finito.")
                continue
            if valor_convertido <= 0:
                print("[!] Erro: O valor informado deve ser maior que zero.")
                continue
            return valor_convertido
        except ValueError:
            print("[!] Erro de Digitação: Insira um número decimal válido (Ex: 1500.50).")

def ler_int_positivo(mensagem_prompt: str) -> int:
    """Lê um número inteiro positivo do terminal."""
    while True:
        try:
            valor_convertido = int(input(mensagem_prompt).strip())
            if valor_convertido <= 0:
                print("[!] Erro: O valor informado deve ser maior que zero.")
                continue
            return valor_convertido
        except ValueError:
            print("[!] Erro de Digitação: Insira um número inteiro válido.")

def ler_opcao(mensagem_prompt: str, opcoes_validas: list[str]) -> str:
    """Lê uma opção do usuário garantindo que ela esteja dentro da lista de opções válidas."""
    while True:
        opcao = input(mensagem_prompt).strip()
        if opcao in opcoes_validas:
            return opcao
        print(f"[!] Opção inválida. Escolha entre: {', '.join(opcoes_validas)}")

def confirmar_sim_nao(mensagem_prompt: str) -> bool:
    """Lê uma resposta de Sim ou Não do usuário, retornando True para Sim e False para Não."""
    while True:
        resp = input(f"{mensagem_prompt} (S/N): ").strip().upper()
        if resp == 'S':
            return True
        if resp == 'N':
            return False
        print("[!] Responda apenas com 'S' para Sim ou 'N' para Não.")

def exibir_titulo(titulo: str) -> None:
    """Exibe um título formatado e centralizado."""
    print("\n" + "=" * 50)
    print(titulo.center(50))
    print("=" * 50)

def exibir_alerta(mensagem: str) -> None:
    """Exibe uma mensagem de alerta formatada."""
    print(f"\n[ALERTA] {mensagem}")

def exibir_sucesso(mensagem: str) -> None:
    """Exibe uma mensagem de sucesso formatada."""
    print(f"\n[SUCESSO] {mensagem}")
