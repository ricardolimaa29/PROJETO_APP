import flet  as ft
from flet import *

def Home(page: ft.Page):
    
    page.theme_mode = ft.ThemeMode.DARK 
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
    page.title = "MENU APP"
    page.window.width = 390
    page.window.height = 740
    page.window.max_width = 390
    page.window.max_height = 740
    page.window.min_width = 390
    page.window.min_height = 740
    page.scroll = 'auto'


    # ===================================== CRIANDO FUCOES DOS ELEMENTOS
    # FUNCAO DO MENU
    def clicou_menu(e):
        item = e.control.text
        if item == "Suporte":
            print("Abrir suporte...")
        elif item == "Configurações":
            print("Abrir configurações...")
        elif item == "Tema":
            # Alternar entre claro e escuro
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
            else:
                page.theme_mode = ft.ThemeMode.DARK
                page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
            print(f"Tema alterado para: {page.theme_mode}")
            page.update()

    def mudar_tema(a):
            # Alternar entre claro e escuro inultil
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
            else:
                page.theme_mode = ft.ThemeMode.DARK
                page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
            print(f"Tema alterado para: {page.theme_mode}")
            page.update()

    # FUNCAO PARA MUDAR DE TELA para o navbar
    def mudar_tela(nova_tela):
        page.controls.clear()
        page.add(nova_tela)    
        page.update()     
    # ft.ElevatedButton("Voltar para Login",on_click=lambda _: mudar_tela(tela()))
    


    # ===================================== CRIANDO ELEMENTOS
    # Titulo da app/nome do app dentro do appbar

    page.appbar = ft.AppBar(
        leading_width=40,
        title=ft.Text("NomeApp"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, on_click=mudar_tema),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
            ft.PopupMenuItem(text="Suporte", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
            ft.PopupMenuItem(text="Configurações", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(text="Tema", icon="WB_SUNNY_OUTLINED", on_click=clicou_menu),
                    
                ]
            ),
        ],
    )
    
    # Perfil imagem
    page.padding = 15
    perfil = ft.Row(
        spacing=15,
        controls=[
            # Avatar com inicial
            ft.CircleAvatar(
                content=ft.Text("X", size=24, weight="bold", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN,
                radius=30
            ),
            # Coluna com nome + user
            ft.Column(
                spacing=3,
                alignment="center",
                controls=[
                    ft.Text("Nome", size=18, weight="bold"),
                    ft.Row(
                        spacing=5,
                        controls=[
                            ft.Text("@nome.com", size=14),
                            ft.Text("•", size=14),
                            ft.Text("Ver perfil", size=14),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16),
                        ] ) ] ) ] )


    page.add(perfil)

    # NavBar inferior (Home, Notificacoes, Desempenho, Perfil, )
    page.navigation_bar = NavigationBar(
        destinations = [
            NavigationBarDestination(icon=Icons.HOME_OUTLINED, label="Início"),
            NavigationBarDestination(icon=Icons.LIBRARY_BOOKS_OUTLINED, label="Desempenho"),
            NavigationBarDestination(icon=Icons.MESSAGE_OUTLINED, label="Notificações"),
            NavigationBarDestination(icon=Icons.TAG_FACES_OUTLINED, label="Perfil"),
        ]
    )

    # Container
    # ===================================== ALINHANDO ELEMENTOS
    # ------------------------------------- ALINHAMENTO DOS ELEMENTOS NA PAGINA
    page.add(ft.ResponsiveRow([
        ft.CupertinoFilledButton(
            content=ft.Text("CupertinoFilledA"),
            opacity_on_click=0.3,
            on_click=lambda e: print("CupertinoFilledButton clickedA!"),
        ),
        ft.CupertinoFilledButton(
            content=ft.Text("CupertinoFilledB"),
            opacity_on_click=0.3,
            on_click=lambda e: print("CupertinoFilledButton clickedB!"),
        ),
        ft.CupertinoFilledButton(
            content=ft.Text("CupertinoFilledC"),
            opacity_on_click=0.3,
            on_click=lambda e: print("CupertinoFilledButton clickedC!"),
        )
    ]))
ft.app(target=Home)

# add um pouco sobre o perfil, nos proxismos dias..., um pouco sobre a fab
