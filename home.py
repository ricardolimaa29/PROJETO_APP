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

    slides = [
        ft.Image(src="https://picsum.photos/800/400?1", width=500, height=300, fit=ft.ImageFit.COVER, border_radius=10),
        ft.Image(src="https://picsum.photos/800/400?2", width=500, height=300, fit=ft.ImageFit.COVER, border_radius=10),
        ft.Image(src="https://picsum.photos/800/400?3", width=500, height=300, fit=ft.ImageFit.COVER, border_radius=10),
        ft.Image(src="https://picsum.photos/800/400?4", width=500, height=300, fit=ft.ImageFit.COVER, border_radius=10),
    ]

    # Índice atual
    current_index = ft.Ref[int]()
    current_index.value = 0

    # Container onde o slide será mostrado
    slide_view = ft.Container(content=slides[current_index.value], width=500, height=300, border_radius=10)

    # Atualizar slide
    def update_slide(index):
        slide_view.content = slides[index]
        for i, d in enumerate(dots.controls):
            d.bgcolor = "red" if i == index else "white"
        page.update()

    # Botão próximo
    def next_slide(e):
        current_index.value = (current_index.value + 1) % len(slides)
        update_slide(current_index.value)

    # Botão anterior
    def prev_slide(e):
        current_index.value = (current_index.value - 1) % len(slides)
        update_slide(current_index.value)

    # Indicadores (bolinhas)
    dots = ft.Row(
        controls=[
            ft.Container(width=15, height=5, bgcolor="white", border_radius=5)
            for _ in slides
        ],
        alignment="center",
        spacing=5,
    )
    dots.controls[0].bgcolor = "red"

    # Botões estilizados como na imagem
    prev_button = ft.IconButton(
        icon=ft.Icons.KEYBOARD_ARROW_LEFT_SHARP,
        icon_color="white",
        
        on_click=prev_slide,
        style=ft.ButtonStyle(shape=ft.CircleBorder())
    )
    next_button = ft.IconButton(
        icon_color="white",
        icon=ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
        
        on_click=next_slide,
        style=ft.ButtonStyle(shape=ft.CircleBorder())
    )

    # Layout com botões sobrepostos ao slide
    carousel = ft.Stack(
        controls=[
            slide_view,
            ft.Row([prev_button, ft.Container(expand=True), next_button],
                   alignment="spaceBetween",
                   width=500,
                   height=300,
                   vertical_alignment="center"),
        ],
        width=500,
        height=300,
    )

    # Layout final
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

    """""criar uma função que vai mudando de tela depois colocar no icone que vai mudar de tela on_click = Mudar_tela(sla,configuração,perfil)"""
    def mudar_tela(nova_tela):
        page.controls.clear()
        page.add(nova_tela)    
        page.update()     
    # ft.ElevatedButton("Voltar para Login",on_click=lambda _: mudar_tela(tela()))
    


    # ===================================== CRIANDO ELEMENTOS
    # Titulo da app/nome do app dentro do appbar

    page.appbar = ft.AppBar(
        leading_width=10,
        title=ft.Text("FÁBRICA  PROGRAMADORES"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.PopupMenuButton(
                items=[
            ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
            ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
            ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=clicou_menu),        
                
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
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        indicator_color="TEMA",
        # indicator_color="#0e68b1",
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.LIBRARY_BOOKS_OUTLINED,
                selected_icon=ft.Icons.INSERT_CHART,
                label="Desempenho"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.MESSAGE_OUTLINED,
                selected_icon=ft.Icons.MESSAGE,
                label="Notificações"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.TAG_FACES_OUTLINED,
                selected_icon=ft.Icons.PERSON,
                label="Perfil"
            ),
        ],
        on_change=lambda e: print(f"Você clicou na aba {e.control.selected_index}")
)


    eventos = ft.Column(
        spacing=20,
        controls=[
            # Evento do dia 04 de Outubro
            ft.Row(
                spacing=10,
                controls=[
                    # Conteúdo do evento
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text("Títulooooooooo", weight="bold"),
                                padding=10,
                                border_radius=10
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Subtítulo em negrito", weight="bold"),
                                    ft.Text(
                                        "Conteúdo explicativo com várias linhas:\n"
                                        "• Usar weight='bold' para negrito\n"
                                        "• size=12 para tamanho pequeno",
                                        size=12,
                                    )
                                ]),
                                padding=10,
                                border_radius=10
                            ),
                        ]
                    )
                ]
            )
        ]
    )

    page.add(
        ft.ExpansionTile(
            title=ft.Text("Opaaaa"),
            subtitle=ft.Text("O que será que será?"),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            controls=[eventos],
        )
    )



    # Função para abrir links externos
    def abrir_link(e, url):
        page.launch_url(url)



            
    links = ft.Row(
            alignment="spaceEvenly",
            spacing=20,
            controls=[
                # Primeiro botão (foto circular)
                ft.Column(
                    spacing=0,
                    horizontal_alignment="center",
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="img\santana.png",   # 🔹 sua imagem PNG
                                width=73,
                                height=73,
                                fit=ft.ImageFit.COVER
                            ),
                            width=73,
                            height=73,
                            border_radius=100, # 🔹 deixa circular
                            on_click=lambda e: abrir_link(e, "https://prefeitura.santanadeparnaiba.sp.gov.br/Plataforma/smti/fabrica-de-programadores"),
                            ink=True,
                        ),
                        ft.Text("FÁBRICA", size=14, color="white")
                    ]
                ),

                # Segundo botão
                ft.Column(
                    spacing=0,
                    horizontal_alignment="center",
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="img/portifolio.jpg",
                                width=73,
                                height=73,
                                fit=ft.ImageFit.COVER
                            ),
                            width=73,
                            height=73,
                            border_radius=100,
                            on_click=lambda e: abrir_link(e, "https://youtube.com"),
                            ink=True,
                        ),
                        ft.Text("DEVS", size=14, color="white")
                    ]
                ),

                # Terceiro botão
                ft.Column(
                    spacing=0,
                    horizontal_alignment="center",
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="img\senai.jpg",
                                width=73,
                                height=73,
                                fit=ft.ImageFit.COVER
                            ),
                            width=73,
                            height=73,
                            border_radius=100,
                            on_click=lambda e: abrir_link(e, "https://www.sp.senai.br/"),
                            ink=True,
                        ), 
                        ft.Text("SENAI", size=14, color="white")
                    ]
                ),
            ]
        )


    page.add(
        carousel,
        dots
    )
    page.add(links)
ft.app(target=Home)

# add um pouco sobre o perfil, nos proxismos dias..., um pouco sobre a fab
