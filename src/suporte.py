import flet as ft

def suporte_view(page: ft.Page):
    # ---------- Configurações básicas ----------
    page.title = "Suporte"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.CYAN)
    page.window.width = 500
    page.window.height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.window.center()
    page.padding = 0
    page.scroll = "medio"

    # ---------- Cores ----------
    primary_color = ft.Colors.CYAN_400
    card_color = ft.Colors.GREY_800

    # ===================================== FUNÇÕES DO MENU =====================================
    def clicou_menu(e):
        item = e.control.text.upper()
        if item == "SUPORTE":
            print("Abrir suporte...")
        elif item == "CONFIGURAÇÕES":
            print("Abrir configurações...")
        elif item == "TEMA":
            mudar_tema(None)
        elif item == "SAIR":
            print("Encerrar aplicação...")

    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.CYAN)
        print(f"Tema alterado para: {page.theme_mode}")
        page.update()

    # ===================================== FUNÇÕES DOS ELEMENTOS =====================================
    def enviar_click(e):
        if nome.value.strip() and mensagem.value.strip():
            page.open(
                ft.SnackBar(
                    content=ft.Text("Enviado com sucesso!", color="white"),
                    bgcolor="green",
                    duration=2000
                )
            )
            nome.value = ""
            mensagem.value = ""
        else:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Preencha todos os campos!", color="white"),
                    bgcolor="red",
                    duration=2000
                )
            )
        page.update()

    def voltar_home(e):
        page.go("/home")

    # ---------- Campos ----------
    nome = ft.TextField(
        label="Nome de usuário",
        width=350,
        border_color=primary_color,
        focused_border_color=primary_color,
    )
    mensagem = ft.TextField(
        label="Mensagem",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=350,
        border_color=primary_color,
        focused_border_color=primary_color,
    )

    # ---------- Conteúdo principal ----------
    conteudo = ft.Column(
        [
            ft.Icon(ft.Icons.HELP_OUTLINE_ROUNDED, size=60, color=primary_color),
            ft.Text(
                "Central de Suporte",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Envie sua dúvida ou solicitação abaixo",
                size=14,
                color=ft.Colors.GREY_400,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=20),
            nome,
            mensagem,
            ft.ElevatedButton(
                "Enviar",
                on_click=enviar_click,
                bgcolor=primary_color,
                color="black",
                width=200,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            ),
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # ---------- Layout principal ----------
    return ft.View(
        route="/suporte",
        controls=[
            ft.AppBar(
                title=ft.Text("SUPORTE", size=20, weight=ft.FontWeight.BOLD, color="white"),
                bgcolor=card_color,
                center_title=True,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color="white",
                    tooltip="Voltar",
                    on_click=voltar_home,
                ),
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                            ft.PopupMenuItem(text="ACESSIBILIDADE", icon="ACCESSIBILITY", on_click=clicou_menu),
                            ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                            ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=clicou_menu),
                        ]
                    ),
                ],
            ),
            ft.Container(
                content=conteudo,
                expand=True,
                alignment=ft.alignment.center,
                padding=20,
            ),
        ],
    )


# ---------- Inicialização ----------
def main(page: ft.Page):
    def route_change(e):
        if page.route == "/suporte":
            page.views.clear()
            page.views.append(suporte_view(page))
        elif page.route == "/home":
            page.views.clear()
            page.views.append(
                ft.View(
                    route="/home",
                    controls=[
                        ft.AppBar(title=ft.Text("HOME")),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Tela inicial de exemplo"),
                                    ft.ElevatedButton(
                                        "Ir para Suporte", on_click=lambda e: page.go("/suporte")
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            expand=True,
                            alignment=ft.alignment.center,
                        ),
                    ],
                )
            )

    
    
    return ft.View(
    route="/suporte",
    controls=[       ft.Container(
            content=suporte_view,
            alignment=ft.alignment.center,
            expand=True,
        )],
    vertical_alignment="center",
    horizontal_alignment="center",
        )


