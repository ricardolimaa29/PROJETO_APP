import flet as ft

def main(page: ft.Page):
    page.title = "Fabrica de programadores"
    page.theme_mode = "dark"
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900

    def handle_dlg_action_clicked(e):
        page.close(dlg)
        dlg.data.confirm_dismiss(e.control.data)

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
        if e.direction == ft.DismissDirection.END_TO_START:  # right-to-left slide
            # save current dismissible to dialog's data, for confirmation in handle_dlg_action_clicked
            dlg.data = e.control
            page.open(dlg)
        else:  # left-to-right slide
            e.control.confirm_dismiss(True)

    def handle_dismiss(e):
        e.control.parent.controls.remove(e.control)
        page.update()

    def handle_update(e: ft.DismissibleUpdateEvent):
        print(
            f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}"
        )

    # Criar o título corretamente como um widget Text
    titulo = ft.Text("Caixa De Entrada", size=24, weight=ft.FontWeight.BOLD)
    
    page.add(
        ft.Row([titulo], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=10),
        ft.ListView(
            expand=True,
            controls=[
                ft.Dismissible(
                    content=ft.ListTile(title=ft.Text(f"Item {i}")),
                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                    background=ft.Container(bgcolor=ft.Colors.GREEN, content=ft.Text("ARQUIVAR")),
                    secondary_background=ft.Container(bgcolor=ft.Colors.RED,content=ft.Text("EXCLUIR")),
                    on_dismiss=handle_dismiss,
                    on_update=handle_update,
                    on_confirm_dismiss=handle_confirm_dismiss,
                    dismiss_thresholds={
                        ft.DismissDirection.END_TO_START: 0.2,
                        ft.DismissDirection.START_TO_END: 0.2,
                    },
                )
                for i in range(10)
            ],
        )
    )

    # return ft.View(
    #         route="/",
    #         controls=[
    #             ft.Row([titulo],alignment="center"),
    #             ft.Row([nome],alignment="center"),
    #             ft.Row([senha],alignment="center"),
    #             ft.Row([botao,],alignment="center")
    #         ],
    #         vertical_alignment="center",
    #         horizontal_alignment="center"
    # )
ft.app(target=main)
