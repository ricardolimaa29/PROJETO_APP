import flet as ft
import datetime


def main(page: ft.Page):
    # ---------- Configurações da Janela ----------
    page.title = "Fábrica do Programador"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700
    page.window.min_width = 360
    page.window.max_width = 500
    page.window.min_height = 600
    page.window.max_height = 800
    page.window.center()
    page.padding = 0

    # ---------- Cores e Tema ----------
    primary_color = ft.Colors.CYAN_400
    secondary_color = ft.Colors.PURPLE_400
    background_color = ft.Colors.GREY_900
    card_color = ft.Colors.GREY_800

    # ---------- Componentes ----------
    def create_card(title, subtitle, icon, route=None):
        return ft.Card(
            elevation=5,
            color=card_color,
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(icon, color=primary_color, size=28),
                    title=ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                    subtitle=ft.Text(subtitle, size=12, color=ft.Colors.GREY_400),
                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_500),
                ),
                padding=10,
                on_click=lambda e: change_page(route) if route else None,
                border_radius=10,
            ),
            margin=ft.margin.only(bottom=10),
        )

    def create_section_header(title):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD,
                            color=primary_color),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            margin=ft.margin.only(top=20, bottom=10),
        )

    # ---------- Páginas ----------
    def home_page():
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.CODE, size=60, color=primary_color),
                            ft.Text("Fábrica do Programador",
                                    size=24, weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER),
                            ft.Text("Desenvolvendo habilidades, construindo o futuro",
                                    size=14, color=ft.Colors.GREY_400,
                                    text_align=ft.TextAlign.CENTER),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                    margin=ft.margin.only(bottom=20),
                ),

                create_section_header("Módulos de Aprendizado"),
                create_card("Módulo 1: Introdução ao Python",
                            "Fundamentos da linguagem Python", ft.Icons.PLAY_ARROW, "MOD1"),
                create_card("Módulo 2: Estruturas de Controle",
                            "Condicionais e loops", ft.Icons.CODE, "MOD2"),
                create_card("Módulo 3: Projetos Práticos",
                            "Aplicação dos conceitos", ft.Icons.BUILD, "MOD3"),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def desempenho_page():
        return ft.Column(
            [
                ft.Text("📊 Seu Desempenho", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Progresso geral e módulos concluídos.", size=14, color=ft.Colors.GREY_400),
                ft.Container(height=20),
                ft.ElevatedButton("⬅ Voltar", on_click=lambda e: change_page("INICIO")),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def modulo_page(num, titulo, descricao):
        return ft.Column(
            [
                ft.Text(f"📖 {titulo}", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text(descricao, size=16),
                ft.Text("Conteúdo em construção...", size=14, italic=True, color="gray"),
                ft.ElevatedButton("⬅ Voltar", on_click=lambda e: change_page("INICIO")),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def simples_page(titulo):
        return ft.Column(
            [
                ft.Icon(ft.Icons.CONSTRUCTION, size=60, color=ft.Colors.ORANGE_400),
                ft.Text(titulo, size=22, weight=ft.FontWeight.BOLD),
                ft.Text(f"A seção {titulo} está em construção...",
                        size=14, color=ft.Colors.GREY_400),
                ft.ElevatedButton("⬅ Voltar", on_click=lambda e: change_page("INICIO")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # ---------- Navegação ----------
    def change_page(route: str):
        page.views.clear()

        if route == "INICIO":
            content = home_page()
        elif route == "DESEMPENHO":
            content = desempenho_page()
        elif route == "MOD1":
            content = modulo_page(1, "Introdução ao Python",
                                  "Aprenda os fundamentos da programação Python.")
        elif route == "MOD2":
            content = modulo_page(2, "Estruturas de Controle",
                                  "Condicionais, loops e lógica de programação.")
        elif route == "MOD3":
            content = modulo_page(3, "Projetos Práticos",
                                  "Desenvolvendo projetos reais em Python.")
        elif route == "NOTIFICAÇÕES":
            content = simples_page("Notificações")
        elif route == "AMIGOS":
            content = simples_page("Amigos")
        elif route == "SUPORTE":
            content = simples_page("Suporte")
        elif route == "CONFIGURAÇÕES":
            content = simples_page("Configurações")
        elif route == "SAIR":
            content = ft.Column(
                [
                    ft.Icon(ft.Icons.EXIT_TO_APP, size=60, color=primary_color),
                    ft.Text("Você saiu do aplicativo", size=20, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            content = simples_page("Página desconhecida")

        page.views.append(ft.View(route, [content]))
        page.update()

    # ---------- Drawer ----------
    drawer = ft.NavigationDrawer(
        bgcolor=card_color,
        indicator_color=primary_color,
        controls=[
            ft.NavigationDrawerDestination(label="INICIO", icon=ft.Icons.HOME_ROUNDED),
            ft.Divider(),
            ft.NavigationDrawerDestination(label="DESEMPENHO", icon=ft.Icons.BAR_CHART),
            ft.NavigationDrawerDestination(label="NOTIFICAÇÕES", icon=ft.Icons.NOTIFICATIONS),
            ft.NavigationDrawerDestination(label="AMIGOS", icon=ft.Icons.PEOPLE),
            ft.NavigationDrawerDestination(label="SUPORTE", icon=ft.Icons.LIVE_HELP),
            ft.NavigationDrawerDestination(label="CONFIGURAÇÕES", icon=ft.Icons.SETTINGS),
            ft.Divider(),
            ft.NavigationDrawerDestination(label="SAIR", icon=ft.Icons.EXIT_TO_APP),
        ],
        on_change=lambda e: [
            change_page(e.control.controls[e.control.selected_index].label),
            page.close(drawer),
        ],
    )

    # ---------- AppBar ----------
    page.appbar = ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=lambda e: page.open(drawer)),
        title=ft.Text("Fábrica do Programador", size=18, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=background_color,
    )

    # ---------- Inicialização ----------
    change_page("INICIO")


ft.app(target=main)
