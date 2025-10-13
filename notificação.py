import flet as ft

class MessageManager:
    def __init__(self):
        self.inbox = []  
        self.archived = []  
        self.deleted = []  
        
    def add_to_inbox(self, message):
        self.inbox.append(message)

def NotificacaoView (page: ft.Page):
    page.title = "Fabrica de programadores"
    page.theme_mode = "dark"
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900

    message_manager = MessageManager()
    
    # Adiciona mensagens de exemplo
    for i in range(10):
        message_manager.add_to_inbox(f"Item {i+1}")

    current_view = "inbox"

    def update_view():
        content_column.controls.clear()
        
        # Define o título baseado na view atual
        if current_view == "inbox":
            title_text = "Caixa De Entrada"
        elif current_view == "archived":
            title_text = "Mensagens Arquivadas"
        else:
            title_text = "Mensagens Excluídas"
        
        # Cabeçalho com botão voltar
        header_row_controls = [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                tooltip="Voltar",
                on_click=lambda e: go_back(),
                width=40,
                height=40
            )
        ]
        
        # Título centralizado
        header_row_controls.append(
            ft.Container(
                ft.Row(
                    [ft.Text(title_text, size=24, weight=ft.FontWeight.BOLD)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                expand=True
            )
        )
        
        content_column.controls.append(
            ft.Container(
                ft.Row(header_row_controls),
                padding=ft.padding.only(bottom=10)
            )
        )
        
        # Botões de navegação
        buttons_row = []
        if current_view == "inbox":
            buttons_row = [
                ft.ElevatedButton("Arquivadas", width=100, bgcolor="none", color="white", 
                                on_click=lambda e: show_archived_messages()),
                ft.ElevatedButton("Excluídas", width=100, bgcolor="none", color="white", 
                                on_click=lambda e: show_deleted_messages()),
            ]
        elif current_view == "deleted":
            # View de excluídas - apenas botão esvaziar lixeira
            buttons_row = [
                ft.ElevatedButton("Esvaziar Lixeira", width=120, bgcolor="red", color="white", 
                                on_click=lambda e: confirm_empty_trash()),
            ]
        
        if buttons_row:
            content_column.controls.append(
                ft.Container(
                    ft.Row(buttons_row, alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    padding=ft.padding.only(top=10, bottom=10)
                )
            )
        
        content_column.controls.append(ft.Divider(height=10))
   
        # Lista de mensagens
        list_view = ft.ListView(expand=True)
        
        if current_view == "inbox":
            for i, message in enumerate(message_manager.inbox):
                list_view.controls.append(create_dismissible_item(message, i))
        elif current_view == "archived":
            for i, message in enumerate(message_manager.archived):
                list_view.controls.append(create_archived_item(message, i))
        elif current_view == "deleted":
            for i, message in enumerate(message_manager.deleted):
                list_view.controls.append(create_deleted_item(message, i))
        
        # Mensagem para lista vazia
        if (current_view == "inbox" and len(message_manager.inbox) == 0) or \
           (current_view == "archived" and len(message_manager.archived) == 0) or \
           (current_view == "deleted" and len(message_manager.deleted) == 0):
            
            if current_view == "inbox":
                empty_text = "Caixa de entrada vazia"
            elif current_view == "archived":
                empty_text = "Nenhuma mensagem arquivada"
            else:
                empty_text = "Nenhuma mensagem excluída"
            
            list_view.controls.append(
                ft.Container(
                    content=ft.Text(empty_text, size=16, color=ft.Colors.GREY_400),
                    alignment=ft.alignment.center,
                    padding=20,
                    height=200
                )
            )
        
        content_column.controls.append(list_view)
        page.update()

    def create_dismissible_item(message, index):
        return ft.Dismissible(
            content=ft.ListTile(
                title=ft.Text(message),
                subtitle=ft.Text("Clique para ver detalhes"),
                on_click=lambda e, msg=message: show_message_details(msg, "inbox")
            ),
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            background=ft.Container(
                alignment=ft.alignment.center_left, 
                padding=ft.padding.only(left=20),
                bgcolor=ft.Colors.GREEN, 
                content=ft.Text("ARQUIVAR", weight=ft.FontWeight.BOLD)
            ),
            secondary_background=ft.Container(
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(right=20),
                bgcolor=ft.Colors.RED, 
                content=ft.Text("EXCLUIR", weight=ft.FontWeight.BOLD)
            ),
            on_dismiss=lambda e, msg=message: handle_dismiss(e, msg),
            on_confirm_dismiss=handle_confirm_dismiss,
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.3,
                ft.DismissDirection.START_TO_END: 0.3,
            },
        )

    def create_archived_item(message, index):
        return ft.Container(
            content=ft.ListTile(
                title=ft.Text(message),
                subtitle=ft.Text("Mensagem arquivada - Clique para ver detalhes"),
                on_click=lambda e, msg=message: show_message_details(msg, "arquivada"),
                trailing=ft.IconButton(
                    icon=ft.Icons.RESTORE,
                    tooltip="Restaurar para Caixa de Entrada",
                    on_click=lambda e, msg=message: restore_archived_message(msg)
                )
            ),
            border=ft.border.all(1, ft.Colors.GREEN),
            margin=ft.margin.only(bottom=5),
            border_radius=10
        )

    def create_deleted_item(message, index):
        return ft.Container(
            content=ft.ListTile(
                title=ft.Text(message),
                subtitle=ft.Text("Mensagem excluída - Clique para ver detalhes"),
                on_click=lambda e, msg=message: show_message_details(msg, "excluída"),
                trailing=ft.IconButton(
                    icon=ft.Icons.RESTORE,
                    tooltip="Restaurar para Caixa de Entrada",
                    on_click=lambda e, msg=message: restore_deleted_message(msg)
                )
            ),
            border=ft.border.all(1, ft.Colors.RED),
            margin=ft.margin.only(bottom=5),
            border_radius=10
        )

    def show_message_details(message, source):
        details_dlg = ft.AlertDialog(
            title=ft.Text("Detalhes da Mensagem"),
            content=ft.Text(f"Conteúdo: {message}\n\nOrigem: {source}"),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: close_dialog(details_dlg))
            ]
        )
        page.open(details_dlg)

    def restore_archived_message(message):
        if message in message_manager.archived:
            message_manager.archived.remove(message)
            message_manager.inbox.append(message)
            update_view()

    def restore_deleted_message(message):
        if message in message_manager.deleted:
            message_manager.deleted.remove(message)
            message_manager.inbox.append(message)
            update_view()

    def confirm_empty_trash():
        if len(message_manager.deleted) == 0:
            empty_dlg = ft.AlertDialog(
                title=ft.Text("Lixeira Vazia"),
                content=ft.Text("A lixeira já está vazia."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(empty_dlg))]
            )
            page.open(empty_dlg)
        else:
            confirm_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Esvaziar Lixeira"),
                content=ft.Text(f"Tem certeza que deseja esvaziar a lixeira?\n\nIsso irá excluir permanentemente {len(message_manager.deleted)} mensagem(ns).\n\nEsta ação não pode ser desfeita."),
                actions=[
                    ft.TextButton("Sim", on_click=lambda e: handle_empty_trash(confirm_dlg)),
                    ft.TextButton("Cancelar", on_click=lambda e: close_dialog(confirm_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            page.open(confirm_dlg)

    def handle_empty_trash(dialog):
        message_manager.deleted.clear()
        close_dialog(dialog)
        update_view()  # Apenas atualiza a view, mantendo na tela atual (deleted)

    def close_dialog(dialog):
        page.close(dialog)

    def go_back():
        if current_view == "inbox":
            page.window_close()
        else:
            show_inbox()

    def show_archived_messages():
        nonlocal current_view
        current_view = "archived"
        update_view()

    def show_deleted_messages():
        nonlocal current_view
        current_view = "deleted"
        update_view()

    def show_inbox():
        nonlocal current_view
        current_view = "inbox"
        update_view()

    def handle_dlg_action_clicked(e):
        user_confirmed = e.control.data
        dismissible_control = dlg.data["control"]
        message = dlg.data["message"]
        
        page.close(dlg)
        
        if user_confirmed:
            dismissible_control.confirm_dismiss(True)
        else:
            dismissible_control.confirm_dismiss(False)

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Por favor, nos informe."),
        content=ft.Text("Você deseja excluir esse item?"),
        actions=[
            ft.TextButton("Sim", data=True, on_click=handle_dlg_action_clicked),
            ft.TextButton("Não", data=False, on_click=handle_dlg_action_clicked),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
        if e.direction == ft.DismissDirection.END_TO_START:  
            message = e.control.content.title.value
            dlg.data = {"control": e.control, "message": message}
            page.open(dlg)
        else:  
            e.control.confirm_dismiss(True)

    def handle_dismiss(e: ft.DismissibleDismissEvent, message):
        if e.direction == ft.DismissDirection.START_TO_END:
            message_manager.inbox.remove(message)
            message_manager.archived.append(message)
        elif e.direction == ft.DismissDirection.END_TO_START:
            message_manager.inbox.remove(message)
            message_manager.deleted.append(message)
        
        update_view()

    content_column = ft.Column()

    # Adiciona o conteúdo à página
    page.add(content_column)
    
    # Atualiza a view inicial
    update_view()

    return ft.View(
        route = "/notificacao",
        controls=[
    content_column
    ],
        vertical_alignment="center",
        horizontal_alignment="center"
)
