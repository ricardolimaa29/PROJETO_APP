import flet as ft

def aulas_view(page: ft.Page):
    page.title = "Fábrica do Programador"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 500
    page.window.height = 800
    page.window.min_width = 500
    page.window.max_width = 500
    page.window.min_height = 800
    page.window.max_height = 800
    page.window.center()
    page.padding = 0

    # ---------- Cores e Tema ----------
    primary_color = ft.Colors.CYAN_400
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
                border_radius=10,
            ),
            margin=ft.margin.only(bottom=10),
        )

    def create_section_header(title):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=primary_color),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            margin=ft.margin.only(top=20, bottom=10),
        )

    # ---------- Página Principal ----------
    conteudo = ft.Column(
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

    # ---------- Retorno ----------
    return ft.View(
        route="/aulas",
        controls=[
            ft.Container(
                content=conteudo,
                alignment=ft.alignment.top_center,
                expand=True,
            )
        ],
        vertical_alignment="start",
        horizontal_alignment="center",
    )
