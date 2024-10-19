from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

class TaskManager(BoxLayout):
    tasks = []  # Lista para armazenar as tarefas

    def add_task(self):
        task_input = self.ids.task_input.text
        if task_input:
            # Cria um layout para a tarefa
            task_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            task_box.complete = False  # Adiciona a propriedade complete ao task_box

            # Cria um Label com texto da tarefa
            task_label = Label(
                text=task_input,
                size_hint_x=0.6,
                size_hint_y=None,
                height=30,
                color=(0, 0, 0, 1),  # Texto preto
            )

            # Botão para concluir a tarefa
            complete_button = Button(text="C", size_hint_x=None, width=30, height=30)
            complete_button.bind(on_press=lambda instance, task_box=task_box, task_label=task_label: self.complete_task(task_box, task_label))

            # Botão para editar a tarefa
            edit_button = Button(text="E", size_hint_x=None, width=30, height=30)
            edit_button.bind(on_press=lambda instance, task_box=task_box, task_label=task_label: self.edit_task(task_box, task_label))

            # Botão para apagar a tarefa
            delete_button = Button(text="A", size_hint_x=None, width=30, height=30)
            delete_button.bind(on_press=lambda instance, task_box=task_box: self.delete_task(task_box))

            # Adiciona os widgets no layout da tarefa
            task_box.add_widget(task_label)
            task_box.add_widget(complete_button)
            task_box.add_widget(edit_button)
            task_box.add_widget(delete_button)

            # Adiciona a tarefa na lista de tarefas
            self.tasks.insert(0, task_box)  # Insere a nova tarefa no início da lista

            # Limpa a lista e adiciona todas as tarefas na ordem correta
            self.update_task_list()

            # Limpa o campo de entrada de texto
            self.ids.task_input.text = ''

    def update_task_list(self):
        # Limpa a lista de tarefas existente
        task_list = self.ids.task_list
        task_list.clear_widgets()

        # Adiciona todas as tarefas da lista (novas no início e concluídas no final)
        for task_box in self.tasks:
            task_list.add_widget(task_box)

    def edit_task(self, task_box, task_label):
        # Salva referências aos botões
        complete_button = task_box.children[2]  # O botão "Concluir"
        edit_button = task_box.children[1]  # O botão "Editar"
        delete_button = task_box.children[0]  # O botão "Apagar"

        # Cria um TextInput para edição da tarefa
        edit_input = TextInput(text=task_label.text, size_hint_x=0.6, size_hint_y=None, height=30)

        # Substitui o Label pelo TextInput para permitir edição
        task_box.clear_widgets()  # Remove todos os widgets antigos
        task_box.add_widget(edit_input)  # Adiciona o campo de entrada

        # Botão para confirmar a edição
        confirm_button = Button(text="OK", size_hint_x=None, width=30, height=30)
        # Após a confirmação, o texto da tarefa é atualizado e os botões são reexibidos
        confirm_button.bind(
            on_press=lambda instance, edit_input=edit_input, task_box=task_box, complete_button=complete_button,
                            edit_button=edit_button, delete_button=delete_button: self.confirm_edit(edit_input,
                                                                                                    task_box,
                                                                                                    complete_button,
                                                                                                    edit_button,
                                                                                                    delete_button, task_label))
        task_box.add_widget(confirm_button)  # Adiciona o botão de confirmação

    def confirm_edit(self, edit_input, task_box, complete_button, edit_button, delete_button, task_label):
        # Substitui o TextInput pelo Label com o texto editado
        edited_text = edit_input.text

        # Cria um novo Label com o texto editado
        task_label.text = edited_text  # Atualiza o texto da tarefa

        # Mantém o estado de conclusão (caso a tarefa já tenha sido concluída)
        if task_box.complete:  # Usa o estado do task_box para verificar se já foi concluído
            task_label.color = (0, 1, 0, 1)  # Verde se já concluído
        else:
            task_label.color = (0, 0, 0, 1)  # Preto se não concluído

        # Atualiza a tarefa com o novo texto
        task_box.clear_widgets()  # Limpa os widgets antigos
        task_box.add_widget(task_label)  # Adiciona o texto atualizado

        # Re-adiciona os botões com a ordem correta
        task_box.add_widget(complete_button)  # Botão "Concluir"
        task_box.add_widget(edit_button)  # Botão "Editar"
        task_box.add_widget(delete_button)  # Botão "Apagar"

    def complete_task(self, task_box, task_label):
        # Se a tarefa não estiver concluída, muda a cor do texto para verde
        if not task_box.complete:  # Se o texto não estiver verde
            task_label.color = (0, 1, 0, 1)  # Altera para verde
            task_box.complete = True  # Marca a tarefa como concluída

            # Mover tarefa concluída para o final
            self.move_task_to_end(task_box)
        else:
            task_label.color = (0, 0, 0, 1)  # Se já estiver verde, volta para preto
            task_box.complete = False  # Marca a tarefa como não concluída

            # Mover tarefa não concluída de volta para o início
            self.move_task_to_start(task_box)

    def move_task_to_end(self, task_box):
        # Remove a tarefa da posição atual
        self.tasks.remove(task_box)

        # Adiciona a tarefa no final da lista
        self.tasks.append(task_box)

        # Reorganiza a lista
        self.update_task_list()

    def move_task_to_start(self, task_box):
        # Remove a tarefa da posição atual
        self.tasks.remove(task_box)

        # Adiciona a tarefa no início da lista
        self.tasks.insert(0, task_box)

        # Reorganiza a lista
        self.update_task_list()

    def delete_task(self, task_box):
        # Remove a tarefa da lista de tarefas
        self.tasks.remove(task_box)

        # Reorganiza a lista
        self.update_task_list()


class TaskManagerApp(App):
    def build(self):
        return TaskManager()


if __name__ == '__main__':
    TaskManagerApp().run()
