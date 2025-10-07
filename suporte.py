import flet as ft

def suporte_view(page: ft.Page):
    page.title = "Suporte"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
    page.window.width = 500
    page.window.height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.scroll = "medio"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------- Inputs ----------
    envidas = ft.TextField(label="Nome de usuário", width=350)
    mensagem = ft.TextField(
        label="Mensagem",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=350,
    )

    # ---------- Funções ----------
    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
        print(f"Tema alterado para: {page.theme_mode}")
        page.update()

    def clicou_menu(e):
        item = e.control.text
        print(f"Item clicado: {item}")

    def enviar_click(e):
        if envidas.value.strip() and mensagem.value.strip():
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Mensagem enviada com sucesso!", color="white"),
                    bgcolor="green",
                )
            )
        else:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Preencha todos os campos!", color="white"),
                    bgcolor="red",
                )
            )

    # ---------- Barra superior ----------
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            ft.Icons.ARROW_BACK,
            icon_color="white",
            tooltip="Voltar",
            on_click=lambda e: page.go("/home"),
        ),
        leading_width=40,
        title=ft.Text("FÁBRICA DE PROGRAMADORES", weight="bold"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                    ft.PopupMenuItem(text="ACESSIBILIDADE", icon="ACCESSIBILITY", on_click=None),
                    ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                    ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=clicou_menu),
                ]
            ),
        ],
    )

    # ---------- Conteúdo ----------
    conteudo = ft.Column(
        [
            ft.Text("SUPORTE", size=30, weight="bold"),
            envidas,
            mensagem,
            ft.ElevatedButton("Enviar", on_click=enviar_click, width=200),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    
    
    return ft.View(
    route="/suporte",
    controls=[       ft.Container(
            content=conteudo,
            alignment=ft.alignment.center,
            expand=True,
        )],
    vertical_alignment="center",
    horizontal_alignment="center",
        )
