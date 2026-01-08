
# Importar serviços 
from service_layer.task_service import TaskService
from service_layer.task_status_service import TaskStatusService

# Criar os serviços 
servico_tarefas = TaskService()
servico_status = TaskStatusService()

def mostrar_menu():
    """Mostra o menu principal"""
    print("\n" + "="*40)
    print("GERENCIADOR DE TAREFAS")
    print("="*40)
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Remover Tarefa")
    print("4. Alterar Status")
    print("5. Sair")
    print("="*40)

def pedir_numero(mensagem, min_valor, max_valor):
    """Pede um número e valida"""
    while True:
        try:
            texto = input(mensagem)
            if not texto:
                print("Digite algo!")
                continue
                
            numero = int(texto)
            
            if numero < min_valor or numero > max_valor:
                print(f"Digite entre {min_valor} e {max_valor}")
                continue
                
            return numero
            
        except:
            print("Digite um número válido!")

def pedir_texto(mensagem, pode_ser_vazio=False):
    """Pede um texto"""
    while True:
        texto = input(mensagem)
        
        if not texto:
            if pode_ser_vazio:
                return ""
            print("Não pode ser vazio!")
            continue
            
        return texto

def escolher_status():
    """Deixa usuário escolher um status"""
    try:
        # Pegar lista de status
        todos_status = servico_status.get_available_status_names()
        
        if not todos_status:
            print("Erro: não tem status")
            return None
        
        print("\nEscolha o status:")
        # Mostrar opções
        contador = 1
        for status in todos_status:
            print(f"{contador}. {status}")
            contador += 1
        
        # Pedir escolha
        escolha = pedir_numero(f"Escolha (1-{len(todos_status)}): ", 1, len(todos_status))
        
        # Retornar status escolhido
        return todos_status[escolha - 1]
        
    except Exception as e:
        print(f"Erro: {e}")
        return None

def adicionar_tarefa():
    """Adiciona uma nova tarefa"""
    print("\n" + "-"*30)
    print("ADICIONAR TAREFA")
    print("-"*30)
    
    # Pedir informações
    nome = pedir_texto("Nome da tarefa: ")
    
    print("Descrição (pode pular - Enter):")
    descricao = input()
    if not descricao:
        descricao = ""
    
    # Escolher status
    status = escolher_status()
    if not status:
        return
    
    # Tentar salvar
    try:
        servico_tarefas.create_task(nome, descricao, status)
        print(f"\nTarefa '{nome}' adicionada!")
        print(f"Status: {status}")
    except Exception as e:
        print(f"Erro: {e}")

def listar_tarefas():
    """Mostra todas as tarefas"""
    print("\n" + "-"*30)
    print("LISTA DE TAREFAS")
    print("-"*30)
    
    try:
        # Pegar tarefas
        lista_tarefas = servico_tarefas.list_all_tasks()
        
        if not lista_tarefas:
            print("Nenhuma tarefa ainda.")
            return
        
        print(f"Total: {len(lista_tarefas)} tarefas")
        print("-"*50)
        print("ID  | NOME               | STATUS      | DESCRIÇÃO")
        print("-"*50)
        
        # Mostrar cada tarefa
        for t in lista_tarefas:
            # Cortar textos muito longos
            nome_display = t.name
            if len(nome_display) > 18:
                nome_display = nome_display[:15] + "..."
            
            desc_display = t.description
            if len(desc_display) > 20:
                desc_display = desc_display[:17] + "..."
            
            print(f"{t.id:3} | {nome_display:18} | {t.status.name:11} | {desc_display}")
        
        print("-"*50)
        
    except Exception as e:
        print(f"Erro: {e}")

def remover_tarefa():
    """Remove uma tarefa"""
    print("\n" + "-"*30)
    print("REMOVER TAREFA")
    print("-"*30)
    
    try:
        # Primeiro mostrar tarefas
        lista_tarefas = servico_tarefas.list_all_tasks()
        
        if not lista_tarefas:
            print("Não tem tarefas para remover.")
            return
        
        listar_tarefas()  # Mostrar lista
        
        # Achar maior ID
        maior_id = 0
        for t in lista_tarefas:
            if t.id > maior_id:
                maior_id = t.id
        
        # Pedir qual remover
        print(f"\nDigite 0 para cancelar")
        id_remover = pedir_numero(f"ID para remover (1-{maior_id}): ", 0, maior_id)
        
        if id_remover == 0:
            print("Cancelado.")
            return
        
        # Confirmar
        resposta = input(f"Remover tarefa {id_remover}? (s/n): ").lower()
        
        if resposta == 's' or resposta == 'sim':
            try:
                servico_tarefas.delete_task(id_remover)
                print(f"Tarefa {id_remover} removida!")
            except Exception as e:
                print(f"Erro: {e}")
        else:
            print("Cancelado.")
            
    except Exception as e:
        print(f"Erro: {e}")

def alterar_status():
    """Altera status de uma tarefa"""
    print("\n" + "-"*30)
    print("ALTERAR STATUS")
    print("-"*30)
    
    try:
        # Mostrar tarefas
        lista_tarefas = servico_tarefas.list_all_tasks()
        
        if not lista_tarefas:
            print("Não tem tarefas.")
            return
        
        listar_tarefas()  # Mostrar lista
        
        # Achar maior ID
        maior_id = 0
        for t in lista_tarefas:
            if t.id > maior_id:
                maior_id = t.id
        
        # Pedir qual tarefa
        print(f"\nDigite 0 para cancelar")
        id_tarefa = pedir_numero(f"ID da tarefa (1-{maior_id}): ", 0, maior_id)
        
        if id_tarefa == 0:
            print("Cancelado.")
            return
        
        # Escolher novo status
        print(f"\nEscolher novo status para tarefa {id_tarefa}:")
        novo_status = escolher_status()
        if not novo_status:
            return
        
        # Confirmar
        resposta = input(f"Mudar tarefa {id_tarefa} para '{novo_status}'? (s/n): ").lower()
        
        if resposta == 's' or resposta == 'sim':
            try:
                servico_tarefas.update_task_status(id_tarefa, novo_status)
                print(f"Status da tarefa {id_tarefa} mudado para '{novo_status}'!")
            except Exception as e:
                print(f"Erro: {e}")
        else:
            print("Cancelado.")
            
    except Exception as e:
        print(f"Erro: {e}")

# PROGRAMA PRINCIPAL
print("="*50)
print("GERENCIADOR DE TAREFAS - INICIANDO")
print("="*50)

rodando = True

while rodando:
    mostrar_menu()
    
    opcao = pedir_numero("Sua escolha: ", 1, 5)
    
    if opcao == 1:
        adicionar_tarefa()
    elif opcao == 2:
        listar_tarefas()
    elif opcao == 3:
        remover_tarefa()
    elif opcao == 4:
        alterar_status()
    elif opcao == 5:
        print("\n" + "="*50)
        print("OBRIGADO POR USAR! ATÉ MAIS!")
        print("="*50)
        rodando = False
    
    # Pausa entre operações
    if rodando:
        input("\nPressione Enter para continuar...")


def main():
    # PROGRAMA PRINCIPAL
    print("="*50)
    print("GERENCIADOR DE TAREFAS")
    print("="*50)
    
    rodando = True
    while rodando:
        
        pass

if __name__ == "__main__":
    main()