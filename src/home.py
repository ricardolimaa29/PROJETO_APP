import flet as ft
from flet import *
import time
import threading
from gtts import gTTS
import os 

def HomeView(page: ft.Page):
    
    page.theme_mode = ft.ThemeMode.DARK 
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
    page.title = "PROGRAMADORES"

    # Configurações da página
    page.scroll = "always"
    page.padding = 0
    page.spacing = 0
 
    # CARROSSEL MELHORADO
    carousel_images = [
        r"Fabrica_app\src\img\fabrica-programadores-parnaiba.png", 
        r"Fabrica_app\src\img\sala.jpg", 
        r"Fabrica_app\src\img\gaby.jpg",
        r"Fabrica_app\src\img\fabrica.jpg"
    ]
    carousel_index = 0

    # Container do carrossel
    carousel_image = ft.Image(
        src=carousel_images[0],
        width=450,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=15
    )

    def update_carousel():
        carousel_image.src = carousel_images[carousel_index]
        # Atualizar dots
        for i, dot in enumerate(dots.controls):
            dot.bgcolor = ft.Colors.DEEP_ORANGE if i == carousel_index else ft.Colors.WHITE24
        page.update()

    def next_slide(e=None):
        nonlocal carousel_index
        carousel_index = (carousel_index + 1) % len(carousel_images)
        update_carousel()

    def prev_slide(e=None):
        nonlocal carousel_index
        carousel_index = (carousel_index - 1) % len(carousel_images)
        update_carousel()

    # Auto-play do carrossel com animação suave
    def auto_play():
        while True:
            time.sleep(4)
            next_slide()

    # Iniciar thread do auto-play em background
    threading.Thread(target=auto_play, daemon=True).start()

    # Indicadores (dots) mais modernos
    dots = ft.Row(
        controls=[
            ft.Container(
                width=8,
                height=8,
                border_radius=4,
                bgcolor=ft.Colors.WHITE24,
            ) for _ in carousel_images
        ],
        alignment="center",
        spacing=8,
    )
    dots.controls[0].bgcolor = ft.Colors.DEEP_ORANGE

    # Layout do carrossel
    carousel = ft.Container(
        content=ft.Stack(
            controls=[
                carousel_image,
                ft.Row(
                    alignment="spaceBetween",
                    vertical_alignment="center",
                    height=200
                ),
                ft.Container(
                    content=dots,
                    alignment=ft.alignment.bottom_center,
                    margin=ft.margin.only(bottom=15)
                )
            ],
        ),
        width=450,
        height=200,
        margin=15,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK54,
            offset=ft.Offset(0, 3)
        )
    )

    # ===================================== CRIANDO FUNÇÕES DOS ELEMENTOS
    
    # Funções de navegação com efeito de transição
    def ir_para_perfil(e):
        page.views.append(
            ft.View(
                route="/perfil",
                transition=ft.PageTransition.FADE,
                transition_duration=300
            )
        )
        page.go("/perfil")

    def ir_para_aulas(e):
        page.views.append(
            ft.View(
                route="/aulasView",
                transition=ft.PageTransition.FADE,
                transition_duration=300
            )
        )
        page.go("/aulasView")

    def ir_para_suporte(e):
        page.views.append(
            ft.View(
                route="/suporte",
                transition=ft.PageTransition.FADE,
                transition_duration=300
            )
        )
        page.go("/suporte")

    # Função para alternar tema com animação
    def mudar_tema(e):
        with page.batch_update():
            if page.theme_mode == ft.ThemeMode.DARK:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.theme = ft.Theme(
                    color_scheme_seed=ft.colors.INDIGO,
                    visual_density=ft.ThemeVisualDensity.COMFORTABLE
                )
            else:
                page.theme_mode = ft.ThemeMode.DARK
                page.theme = ft.Theme(
                    color_scheme_seed=ft.colors.DEEP_ORANGE,
                    visual_density=ft.ThemeVisualDensity.COMFORTABLE
                )
        # Atualiza a UI com animação
        page.update()

    # ===================================== CRIANDO ELEMENTOS
    appbar = ft.AppBar(
        leading_width=10,
        title=ft.Text("FÁBRICA DE PROGRAMADORES", weight="bold"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  
        actions=[ 
                ft.IconButton(ft.Icons.HEARING,),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                    ft.PopupMenuItem(text="ACESSIBILIDADE", icon="SUN", on_click=mudar_tema),
                    ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=...),
                    ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=ir_para_suporte),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=...),        
                ]
            ),
        ],
    )
    
    # PERFIL
    perfil = ft.Container(
        content=ft.Row(
            spacing=20,
            controls=[
                # Container da foto de perfil
                ft.Container(
                    content=ft.Image(
                        src=r"Fabrica_app\src\img\perfil.png",
                        width=110,
                        height=110,
                        fit=ft.ImageFit.COVER,
                    ),
                    width=110,
                    height=110,
                    border_radius=55,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                # Coluna com informações do usuário
                ft.Column(
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Usuário", size=20, weight="bold"),
                        ft.Text("Programador Iniciante", size=14, color=ft.Colors.GREY_400),
                        ft.ElevatedButton(
                            "Editar Perfil",
                            icon=ft.Icons.EDIT_ROUNDED,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=ir_para_perfil
                        )
                    ]
                )
            ]
        ),
        padding=20,
        margin=15,
        border_radius=15,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        )
    )

    # Configurando o NavigationBar
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
    )

    # Container de MATERIAL DO CURSO
    eventos = ft.Container(
        on_click=ir_para_aulas,
        ink=True,
        content=ft.Column(
            alignment=ft.alignment.center, 
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("MATERIAL DO CURSO", size=18, weight="bold"),
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Image(src=r"Fabrica_app\src\img\python.jpg"),
                            title=ft.Text("AULAS DE PYTHON", weight="bold"),
                            subtitle=ft.Text("70% DE APROVEITAMENTO DAS AULAS"),
                            trailing=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.GREEN)
                        ),
                        ft.ListTile(
                            leading=ft.Image(src=r"Fabrica_app\src\img\api.jpg"),
                            title=ft.Text("AULAS DE API", weight="bold"),
                            subtitle=ft.Text("30% DE APROVEITAMENTO DAS AULAS"),
                            trailing=ft.Container(
                                content=ft.Text("2", color=ft.Colors.WHITE, size=12, weight="bold"),
                                bgcolor=ft.Colors.RED,
                                width=24,
                                height=24,
                                border_radius=12,
                                alignment=ft.alignment.center
                            )
                        ),
                    ])
                )
            ]
        ),
        padding=20,
        margin=15,
        border_radius=15,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(0, 2)
        ),
        animate=ft.Animation(200, "easeInOut"),
    )

    # Função para tratar hover
    def on_hover_eventos(e):
        eventos.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST if e.data == "true" else ft.Colors.SURFACE_CONTAINER_HIGHEST
        page.update()

    eventos.on_hover = on_hover_eventos

    # Função para abrir links externos
    def abrir_link(e, url):
        page.launch_url(url)

    # Links melhorados
    links = ft.Container(
        content=ft.Column(
            spacing=20,
            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("SITES IMPORTANTES", size=18, weight="bold", ),
                ft.Row( 
                    alignment="spaceEvenly",
                    spacing=10,
                    controls=[
                        ft.Column(
                            spacing=8,
                            horizontal_alignment="center",
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src=r"Fabrica_app\src\img\santana.png",  
                                        width=70,
                                        height=70,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    width=70,
                                    height=70,
                                    border_radius=35,
                                    on_click=lambda e: abrir_link(e, "https://prefeitura.santanadeparnaiba.sp.gov.br/Plataforma/smti/fabrica-de-programadores"),
                                    ink=True,
                                ),
                                ft.Text("FÁBRICA", size=14, weight="bold")
                            ]
                        ),
                        ft.Column(
                            spacing=8,
                            horizontal_alignment="center",
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src=r"Fabrica_app\src\img\portifolio.jpg",
                                        width=70,
                                        height=70,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    width=70,
                                    height=70,
                                    border_radius=35,
                                    on_click=lambda e: abrir_link(e, "https://github.com"),
                                    ink=True,
                                ),
                                ft.Text("DEVS", size=14, weight="bold")
                            ]
                        ),
                        ft.Column(
                            spacing=8,
                            horizontal_alignment="center",
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src=r"Fabrica_app\src\img\senai.jpg",
                                        width=70,
                                        height=70,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    width=70,
                                    height=70,
                                    border_radius=35,
                                    on_click=lambda e: abrir_link(e, "https://www.sp.senai.br/"),
                                    ink=True,
                                ), 
                                ft.Text("SENAI", size=14, weight="bold")
                            ]
                        ),
                    ]
                )
            ]
        ),
        padding=20,
        margin=15,
        border_radius=15,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
    )
    
    # Container principal scrollável
    main_content = ft.ListView(
        controls=[
            perfil,
            carousel,
            eventos,
            links,
        ],
        spacing=10,
        padding=20,
        auto_scroll=True,
        expand=True,
    )

    # Criar a view com o layout vertical scrollável
    view = ft.View(
        route="/home",
        controls=[
            appbar,  # AppBar fixo no topo
            main_content,  # Conteúdo scrollável
            navbar,  # Navbar fixo embaixo
        ],
        spacing=0,
        padding=0
    )
    
    return view