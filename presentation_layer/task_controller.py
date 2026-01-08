
from service_layer.task_service import TaskService
from service_layer.task_status_service import TaskStatusService


class TaskController:
    """Controlador principal da interface"""
    
    def __init__(self):
        """Inicializa o controlador com os serviços"""
        self.task_service = TaskService()
        self.status_service = TaskStatusService()
        self.running = True
    
    def show_menu(self):
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
    
    def get_number(self, message, min_value, max_value):
        """Pede um número e valida"""
        while True:
            try:
                text = input(message)
                if not text:
                    print("Digite algo!")
                    continue
                    
                number = int(text)
                
                if number < min_value or number > max_value:
                    print(f"Digite entre {min_value} e {max_value}")
                    continue
                    
                return number
                
            except:
                print("Digite um número válido!")
    
    def get_text(self, message, optional=False):
        """Pede um texto"""
        while True:
            text = input(message)
            
            if not text:
                if optional:
                    return ""
                print("Não pode ser vazio!")
                continue
                
            return text
    
    def choose_status(self):
        """Deixa usuário escolher um status"""
        try:
            # Pegar lista de status
            all_status = self.status_service.get_available_status_names()
            
            if not all_status:
                print("Erro: não tem status")
                return None
            
            print("\nEscolha o status:")
            # Mostrar opções
            counter = 1
            for status in all_status:
                print(f"{counter}. {status}")
                counter += 1
            
            # Pedir escolha
            choice = self.get_number(f"Escolha (1-{len(all_status)}): ", 1, len(all_status))
            
            # Retornar status escolhido
            return all_status[choice - 1]
            
        except Exception as e:
            print(f"Erro: {e}")
            return None
    
    def add_task(self):
        """Adiciona uma nova tarefa"""
        print("\n" + "-"*30)
        print("ADICIONAR TAREFA")
        print("-"*30)
        
        # Pedir informações
        name = self.get_text("Nome da tarefa: ")
        
        print("Descrição (pode pular - Enter):")
        description = input()
        if not description:
            description = ""
        
        # Escolher status
        status = self.choose_status()
        if not status:
            return
        
        # Tentar salvar
        try:
            self.task_service.create_task(name, description, status)
            print(f"\nTarefa '{name}' adicionada!")
            print(f"Status: {status}")
        except Exception as e:
            print(f"Erro: {e}")
    
    def list_tasks(self):
        """Mostra todas as tarefas"""
        print("\n" + "-"*30)
        print("LISTA DE TAREFAS")
        print("-"*30)
        
        try:
            # Pegar tarefas
            task_list = self.task_service.list_all_tasks()
            
            if not task_list:
                print("Nenhuma tarefa ainda.")
                return
            
            print(f"Total: {len(task_list)} tarefas")
            print("-"*50)
            print("ID  | NOME               | STATUS      | DESCRIÇÃO")
            print("-"*50)
            
            # Mostrar cada tarefa
            for task in task_list:
                # Cortar textos muito longos
                name_display = task.name
                if len(name_display) > 18:
                    name_display = name_display[:15] + "..."
                
                desc_display = task.description
                if len(desc_display) > 20:
                    desc_display = desc_display[:17] + "..."
                
                print(f"{task.id:3} | {name_display:18} | {task.status.name:11} | {desc_display}")
            
            print("-"*50)
            
        except Exception as e:
            print(f"Erro: {e}")
    
    def remove_task(self):
        """Remove uma tarefa"""
        print("\n" + "-"*30)
        print("REMOVER TAREFA")
        print("-"*30)
        
        try:
            # Primeiro mostrar tarefas
            task_list = self.task_service.list_all_tasks()
            
            if not task_list:
                print("Não tem tarefas para remover.")
                return
            
            self.list_tasks()  # Mostrar lista
            
            # Achar maior ID
            max_id = 0
            for task in task_list:
                if task.id > max_id:
                    max_id = task.id
            
            # Pedir qual remover
            print(f"\nDigite 0 para cancelar")
            task_id = self.get_number(f"ID para remover (1-{max_id}): ", 0, max_id)
            
            if task_id == 0:
                print("Cancelado.")
                return
            
            resposta = input(f"Remover tarefa {task_id}? (s/n): ").lower()
            
            if resposta == 's' or resposta == 'sim':
                try:
                    self.task_service.delete_task(task_id)
                    print(f"Tarefa {task_id} removida!")
                except Exception as e:
                    print(f"Erro: {e}")
            else:
                print("Cancelado.")
                
        except Exception as e:
            print(f"Erro: {e}")
    
    def change_status(self):
        """Altera status de uma tarefa"""
        print("\n" + "-"*30)
        print("ALTERAR STATUS")
        print("-"*30)
        
        try:
            # Mostrar tarefas
            task_list = self.task_service.list_all_tasks()
            
            if not task_list:
                print("Não tem tarefas.")
                return
            
            self.list_tasks()  # Mostrar lista
            
            # Achar maior ID
            max_id = 0
            for task in task_list:
                if task.id > max_id:
                    max_id = task.id
            
            # Pedir qual tarefa
            print(f"\nDigite 0 para cancelar")
            task_id = self.get_number(f"ID da tarefa (1-{max_id}): ", 0, max_id)
            
            if task_id == 0:
                print("Cancelado.")
                return
            
            # Escolher novo status
            print(f"\nEscolher novo status para tarefa {task_id}:")
            new_status = self.choose_status()
            if not new_status:
                return
            
            # Confirmar
            resposta = input(f"Mudar tarefa {task_id} para '{new_status}'? (s/n): ").lower()
            
            if resposta == 's' or resposta == 'sim':
                try:
                    self.task_service.update_task_status(task_id, new_status)
                    print(f"Status da tarefa {task_id} mudado para '{new_status}'!")
                except Exception as e:
                    print(f"Erro: {e}")
            else:
                print("Cancelado.")
                
        except Exception as e:
            print(f"Erro: {e}")
    
    def run(self):
        """Método principal que executa o programa"""
        print("="*50)
        print("GERENCIADOR DE TAREFAS")
        print("="*50)
        
        self.running = True
        
        while self.running:
            self.show_menu()
            
            option = self.get_number("Sua escolha: ", 1, 5)
            
            if option == 1:
                self.add_task()
            elif option == 2:
                self.list_tasks()
            elif option == 3:
                self.remove_task()
            elif option == 4:
                self.change_status()
            elif option == 5:
                print("\n" + "="*50)
                print("OBRIGADO POR USAR! ATÉ MAIS!")
                print("="*50)
                self.running = False
            
            # Pausa entre operações
            if self.running:
                input("\nPressione Enter para continuar...")



def main():
    """Função principal que inicia o programa"""
    try:
        controller = TaskController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
