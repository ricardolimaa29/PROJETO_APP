import flet as ft
import time
import threading

class MessageManager:
    def __init__(self):
        self.inbox = []  
        self.archived = []  
        self.deleted = []  
        
    def add_to_inbox(self, message):
        self.inbox.append(message)
    
    def archive_message(self, message):
        self.archived.append(message)
    
    def delete_message(self, message):
        self.deleted.append(message)

def View_notificacao(page: ft.Page):
    page.title = "Fabrica de programadores"
    page.theme_mode = "dark"
    page.window.min_height = 800
    page.window.min_width = 500
    page.window.max_height = 800
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 800
    page.window.center()

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
        
       


        
        # Botões de navegação NO TOPO (logo abaixo do título)
        buttons_row = []
        if current_view == "inbox":
            buttons_row = [
                ft.ElevatedButton("Arquivadas", width=100, bgcolor="none", color="white", 
                                on_click=lambda e: show_archived_messages()),
                ft.ElevatedButton("Excluídas", width=100, bgcolor="none", color="white", 
                                on_click=lambda e: show_deleted_messages()),
            ]
        elif current_view == "archived":
            # View de arquivadas - sem botões adicionais
            buttons_row = []
        else:  # current_view == "deleted"
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
   
        # Lista de mensagens (agora vem depois dos botões)
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
                    height=300 ##
                )
            )
        
        content_column.controls.append(list_view)
        page.update()
    def clicou_menu(e):
        item = e.control.text
        if item == "Suporte":
            print("Abrir suporte...")
        elif item == "Configurações":
            print("Abrir configurações...")
        elif item == "Tema":
            mudar_tema(None)

    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        print(f"Tema alterado para: {page.theme_mode}")
    appbar = ft.AppBar(
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK,
            on_click=lambda _: page.go('/home'),
        ), 
        title=ft.Text("NOTIFICAÇÕES", weight="bold"),  # título da AppBar
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  # cor de fundo
        actions=[  # ações do lado direito
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                    ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                    ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                    ft.PopupMenuItem(),  # separador
                    ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=lambda e:page.go("/")),
                ]
            ),
        ],
        )
     # NAVIGATION BAR
    def mudar_tela(e):
        index = e.control.selected_index
        if index == 0:
            page.go("/home")
        elif index == 1:
            page.go("/desempenho")
        elif index == 2:
            page.go("/notificação")
        elif index == 3:
            page.go("/perfil")

    navbar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BAR_CHART_OUTLINED,
                selected_icon=ft.Icons.BAR_CHART,
                label="Desempenho"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                selected_icon=ft.Icons.NOTIFICATIONS,
                label="Notificações"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINED,
                selected_icon=ft.Icons.PERSON,
                label="Perfil"
            ),
        ],
        on_change=mudar_tela
    )
    # -------------------------------------------------------------
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
            on_update=handle_update,
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
                ft.TextButton("Fechar", on_click=lambda e: close_dialog_instantly(details_dlg))
            ]
        )
        page.open(details_dlg)


    def restore_archived_message(message):
        try:
            message_to_restore = next(msg for msg in message_manager.archived if msg == message)
            message_manager.archived.remove(message_to_restore)
            message_manager.inbox.append(message_to_restore)
            update_view()
        except (ValueError, StopIteration):
            update_view()

    def restore_deleted_message(message):
        if message in message_manager.deleted:
            message_manager.deleted.remove(message)
            message_manager.inbox.append(message)
            update_view()

    def confirm_empty_trash():
        if len(message_manager.deleted) == 0:
            # Se a lixeira já estiver vazia, mostra um aviso
            empty_dlg = ft.AlertDialog(
                title=ft.Text("Lixeira Vazia"),
                content=ft.Text("A lixeira já está vazia."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog_instantly(empty_dlg))]
            )
            page.open(empty_dlg)
        else:
            # Confirmação para esvaziar lixeira
            confirm_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Esvaziar Lixeira"),
                content=ft.Text(f"Tem certeza que deseja esvaziar a lixeira?\n\nIsso irá excluir permanentemente {len(message_manager.deleted)} mensagem(ns).\n\nEsta ação não pode ser desfeita."),
                actions=[
                    ft.TextButton("Sim", on_click=lambda e: handle_empty_trash(confirm_dlg)),
                    ft.TextButton("Cancelar", on_click=lambda e: close_dialog_instantly(confirm_dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER,
            )
            page.open(confirm_dlg)

    def handle_empty_trash(dialog):
        # Fecha o diálogo instantaneamente
        close_dialog_instantly(dialog)
        # Esvazia a lixeira
        message_manager.deleted.clear()
        # Volta automaticamente para a caixa de entrada
        show_inbox()

    def confirm_permanent_delete(message):
        confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Exclusão Permanente"),
            content=ft.Text(f"Tem certeza que deseja excluir permanentemente:\n\"{message}\"?\n\nEsta ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Sim", data=message, on_click=lambda e: handle_permanent_delete(e, confirm_dlg)),
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog_instantly(confirm_dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        page.open(confirm_dlg)

    def handle_permanent_delete(e, dialog):
        message = e.control.data
        # Fecha o diálogo instantaneamente
        close_dialog_instantly(dialog)
        if message in message_manager.deleted:
            message_manager.deleted.remove(message)
            print(f"Item {message} excluído permanentemente.")
            show_inbox()

    def go_back():
        if current_view == "inbox":
            page.go("/home")
        else:
            show_inbox()

    def show_home():
        nonlocal current_view
        current_view = "inbox"
        update_view()

    def show_archived_messages():
        page.vertical_alignment = "center"
        page.horizontal_alignment = "start"
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
        
        # Fecha o diálogo instantaneamente
        close_dialog_instantly(dlg)
        
        if user_confirmed:
            dismissible_control.confirm_dismiss(True)
        else:
            dismissible_control.confirm_dismiss(False)

    # Função para fechar diálogo instantaneamente
    def close_dialog_instantly(dialog):
        page.close(dialog)

    # Função para fechar todos os diálogos
    def close_all_dialogs():
        # Fecha qualquer diálogo aberto
        if hasattr(page, 'dialog') and page.dialog:
            page.close(page.dialog)

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
            print(f"Item {message} arquivado.")
            message_manager.inbox.remove(message)
            message_manager.archived.append(message)
        elif e.direction == ft.DismissDirection.END_TO_START:
            print(f"Item {message} excluído.")
            message_manager.inbox.remove(message)
            message_manager.deleted.append(message)
        
        update_view()

    def handle_update(e: ft.DismissibleUpdateEvent):
        pass

    # Cria coluna principal para conteúdo
    content_column = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    # Configura scroll automático para a página
    page.scroll = ft.ScrollMode.AUTO
    
    # Atualiza a view inicial
    update_view()
    
    # Monta a view final
    view = ft.View(
        route="/notificação",
        controls=[
            appbar,
            content_column,
            navbar
        ],
        vertical_alignment="start",
        horizontal_alignment="center"
    )
    
    return view
