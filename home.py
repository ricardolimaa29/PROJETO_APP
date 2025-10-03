import flet as ft
from flet import *
import time
import threading

def Home(page: ft.Page):
    
    page.theme_mode = ft.ThemeMode.DARK 
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
    page.title = "PROGRAMADORES"
    page.window.width = 500
    page.window.height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.scroll = 'auto'

    # FilePicker para foto de perfil
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    # Variáveis para a foto de perfil
    profile_photo_ref = ft.Ref[ft.Image]()
    profile_initial_ref = ft.Ref[ft.Text]()

    def pick_file(e):
        file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)

    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files:
            # Atualiza a foto de perfil
            profile_photo_ref.current.src = e.files[0].path
            profile_photo_ref.current.visible = True
            profile_initial_ref.current.visible = False
            page.update()

    file_picker.on_result = on_file_selected

    # CARROSSEL MELHORADO
    carousel_images = [
        "img\programadores.jpg",
        "img\programa.jpeg", 
        "img\santana.jpg",
        "img\premio.png"
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

    # Auto-play do carrossel
    def auto_play():
        while True:
            time.sleep(4)
            next_slide()

    # Iniciar thread do auto-play
    threading.Thread(target=auto_play, daemon=True).start()

    # Botões do carrossel mais elegantes
    prev_button = ft.Container(
        content=ft.Icon(
            ft.Icons.ARROW_BACK_IOS_ROUNDED,
            size=20,
            color=ft.Colors.WHITE
        ),
        width=40,
        height=40,
        border_radius=20,
        bgcolor=ft.Colors.BLACK54,
        alignment=ft.alignment.center,
        on_click=prev_slide,
        margin=ft.margin.only(left=10)
    )
    
    next_button = ft.Container(
        content=ft.Icon(
            ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
            size=20,
            color=ft.Colors.WHITE
        ),
        width=40,
        height=40,
        border_radius=20,
        bgcolor=ft.Colors.BLACK54,
        alignment=ft.alignment.center,
        on_click=next_slide,
        margin=ft.margin.only(right=10)
    )

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
                    [prev_button, ft.Container(expand=True), next_button],
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
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_ORANGE)
        print(f"Tema alterado para: {page.theme_mode}")
        page.update()

    # ===================================== CRIANDO ELEMENTOS
    page.appbar = ft.AppBar(
        leading_width=10,
        title=ft.Text("FÁBRICA DE PROGRAMADORES", weight="bold"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                    ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                    ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=clicou_menu),        
                ]
            ),
        ],
    )
    
    # PERFIL MELHORADO - Design mais atraente
    perfil = ft.Container(
        content=ft.Row(
            spacing=20,
            controls=[
                # Container da foto de perfil
                ft.Stack([
                    # Foto de perfil (inicialmente invisível)
                    ft.Container(
                        content=ft.Image(
                            ref=profile_photo_ref,
                            src="",
                            width=110,
                            height=110,
                            fit=ft.ImageFit.COVER,
                            border_radius=55
                        ),
                        width=110,
                        height=110,
                        border_radius=55,
                        bgcolor=ft.Colors.GREY_700,
                        visible=False
                    ),
                    # Avatar com inicial (inicialmente visível)
                    ft.Container(
                        content=ft.CircleAvatar(
                            ref=profile_initial_ref,
                            content=ft.Text("U", size=36, weight="bold", color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.DEEP_ORANGE,
                            radius=55
                        ),
                        width=110,
                        height=110,
                        border_radius=55,
                    ),
                    # Botão da câmera
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.CAMERA_ALT_ROUNDED, 
                            icon_size=20, 
                            icon_color="white",
                            on_click=pick_file,
                            tooltip="Alterar Foto",
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.DEEP_ORANGE, 
                                shape=ft.CircleBorder(),
                                padding=8
                            )
                        ),
                        alignment=ft.alignment.bottom_right,
                    )
                ]),
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
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.DEEP_ORANGE,
                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
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

    page.padding = 0
    page.add(perfil)

    # NavBar inferior
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        indicator_color=ft.Colors.DEEP_ORANGE,
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
        on_change=lambda e: print(f"Você clicou na aba {e.control.selected_index}")
    )

    # Conteúdo restante - CORRIGIDO o Badge
    eventos = ft.Container(
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("MATERIAL DO CURSO", size=18, weight="bold"),
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CODE_ROUNDED, color=ft.Colors.DEEP_ORANGE),
                            title=ft.Text("Projeto Python Concluído", weight="bold"),
                            subtitle=ft.Text("Finalizado com sucesso - 95% de aproveitamento"),
                            trailing=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.GREEN)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.BUG_REPORT_ROUNDED, color=ft.Colors.ORANGE),
                            title=ft.Text("Problemas Identificados", weight="bold"),
                            subtitle=ft.Text("2 issues precisam de atenção"),
                            # Substituindo Badge por Container personalizado
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
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
    )

    # Função para abrir links externos
    def abrir_link(e, url):
        page.launch_url(url)

    # Links melhorados
    links = ft.Container(
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("SITES", size=18, weight="bold" ),
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
                                        src="img\logo.jpg",
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
                                        src="img\manutenção.jpg",
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
                                        src="img\senai.jpg",
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

    # Adicionar todos os componentes à página
    page.add(
        carousel,
        eventos,
        links
    )

ft.app(target=Home)
