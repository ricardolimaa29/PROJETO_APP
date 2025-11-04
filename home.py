import flet as ft
from flet import *
import time
import threading
import json
from pathlib import Path
import os

def HomeView(page: ft.Page):
    
    page.theme_mode = ft.ThemeMode.DARK 
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.title = "PROGRAMADORES"

    # VARIÁVEL PARA CONTROLE DO TAMANHO DA FONTE
    current_font_scale = 1.0
    font_scales = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    current_font_index = 2  # Índice inicial (1.0)

    # DICIONÁRIO PARA ARMAZENAR OS CONTROLES DE TEXTO
    text_controls = {}

    # CONTROLES DO MODAL QUE PRECISAM SER ATUALIZADOS
    modal_current_percent_text = ft.Text(f"{int(current_font_scale * 100)}%", size=16, weight="bold")
    modal_scale_indicator = ft.Text(
        "Escala: " + " • ".join([
            f"{'●' if i == current_font_index else '○'} {int(scale * 100)}%" 
            for i, scale in enumerate(font_scales)
        ]),
        size=12,
        color=ft.Colors.WHITE
    )

    # Carrega perfil inicial do arquivo JSON
 
    # FUNÇÃO PARA ATUALIZAR O MODAL
    def update_modal_display():
        modal_current_percent_text.value = f"{int(current_font_scale * 100)}%"
        modal_scale_indicator.value = "Escala: " + " • ".join([
            f"{'●' if i == current_font_index else '○'} {int(scale * 100)}%" 
            for i, scale in enumerate(font_scales)
        ])

    # FUNÇÃO PARA MOSTRAR MODAL DE FONTE
    def show_font_modal(e):
        update_modal_display()  # Atualiza antes de abrir
        font_modal.open = True
        page.update()

    # FUNÇÃO PARA FECHAR MODAL
    def close_font_modal(e):
        font_modal.open = False
        page.update()

    # FUNÇÃO PARA AUMENTAR FONTE
    def increase_font(e):
        nonlocal current_font_index, current_font_scale
        if current_font_index < len(font_scales) - 1:
            current_font_index += 1
            current_font_scale = font_scales[current_font_index]
            apply_font_size()
            update_modal_display()  # Atualiza o modal
            page.update()

    # FUNÇÃO PARA DIMINUIR FONTE
    def decrease_font(e):
        nonlocal current_font_index, current_font_scale
        if current_font_index > 0:
            current_font_index -= 1
            current_font_scale = font_scales[current_font_index]
            apply_font_size()
            update_modal_display()  # Atualiza o modal
            page.update()

    # FUNÇÃO PARA RESETAR FONTE
    def reset_font(e):
        nonlocal current_font_index, current_font_scale
        current_font_index = 2
        current_font_scale = font_scales[current_font_index]
        apply_font_size()
        update_modal_display()  # Atualiza o modal
        page.update()

    # FUNÇÃO PARA APLICAR O TAMANHO DA FONTE EM TODOS OS TEXTOS
    def apply_font_size():
        for control_id, control_info in text_controls.items():
            original_size = control_info["original_size"]
            control = control_info["control"]
            
            if hasattr(control, 'size') and control.size is not None:
                control.size = int(original_size * current_font_scale)
            elif hasattr(control, 'title') and hasattr(control.title, 'size'):
                control.title.size = int(original_size * current_font_scale)
            elif hasattr(control, 'subtitle') and hasattr(control.subtitle, 'size'):
                control.subtitle.size = int(original_size * current_font_scale)

    # FUNÇÃO AUXILIAR PARA REGISTRAR CONTROLES DE TEXTO
    def register_text_control(control, original_size, control_id=None):
        if control_id is None:
            control_id = f"control_{len(text_controls)}"
        text_controls[control_id] = {
            "control": control,
            "original_size": original_size
        }
        return control

    # MODAL PARA CONTROLE DE FONTE 
    font_modal = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Text("Tamanho da Fonte", text_align=TextAlign.CENTER),
            alignment=ft.alignment.center
        ),
        content=ft.Column(
            width=300,
            tight=True,
            controls=[
                ft.Row(
                    alignment="center",
                    controls=[
                        ft.Text("Tamanho atual: ", size=16),
                        modal_current_percent_text,
                    ]
                ),
                ft.Divider(),
                ft.Row(
                    alignment="spaceEvenly",
                    controls=[
                        ft.IconButton(
                            ft.Icons.REMOVE_CIRCLE_OUTLINED,
                            icon_color=ft.Colors.RED,
                            icon_size=30,
                            tooltip="Diminuir fonte",
                            on_click=decrease_font
                        ),
                        ft.IconButton(
                            ft.Icons.REFRESH,
                            icon_color=ft.Colors.BLUE,
                            icon_size=30,
                            tooltip="Tamanho padrão",
                            on_click=reset_font
                        ),
                        ft.IconButton(
                            ft.Icons.ADD_CIRCLE_OUTLINED,
                            icon_color=ft.Colors.GREEN,
                            icon_size=30,
                            tooltip="Aumentar fonte",
                            on_click=increase_font
                        ),
                    ]
                ),
                ft.Container(height=10),
                modal_scale_indicator,
            ]
        ),
        actions=[
            ft.TextButton("Fechar", on_click=close_font_modal),
        ],
        actions_alignment="end",
    )

    # ADICIONAR MODAL À PÁGINA
    page.overlay.append(font_modal)

    # ... (o restante do código permanece igual)

    # SCROLL AUTOMÁTICO CONFIGURADO (SEM THREAD PROBLEMÁTICA)
    page.scroll = ft.ScrollMode.AUTO

    # Função de scroll automático segura
    def start_auto_scroll():
        # Espera a página estar completamente carregada
        def safe_auto_scroll():
            time.sleep(3)  # Aguarda 3 segundos para garantir que a página esteja carregada
            if page and hasattr(page, 'scroll_to'):
                try:
                    # Scroll suave para baixo
                    page.scroll_to(offset=0, duration=500)
                    time.sleep(1)
                    for i in range(1, 50):  # Reduzido para ser mais rápido
                        time.sleep(0.03)
                        page.scroll_to(offset=i * 20, duration=200, curve=ft.AnimationCurve.EASE_OUT)
                except Exception as e:
                    print(f"Scroll automático não pôde ser executado: {e}")
        
        # Inicia em uma thread separada
        threading.Thread(target=safe_auto_scroll, daemon=True).start()

    # CARROSSEL
    carousel_images = [
        "https://drive.google.com/uc?export=view&id=1zOqWMKlGG0mFQcfqeK_Pg5Ss-ajbnTsJ",
        "https://drive.google.com/uc?export=view&id=1LKs2OOezpofLzp31ids0VzfQTLLAZbdg",
        "https://drive.google.com/uc?export=view&id=12QvqtJIxNfYLqbnvOI35YhUaRGSCzVIw",
        "https://drive.google.com/uc?export=view&id=1jbHAk5kLxWOJ9WQzfAC5LzlhNOgNm6yB"
    ]
    carousel_index = 0

    carousel_image = ft.Image(
        src=carousel_images[0],
        width=450,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=15
    )

    def update_carousel():
        carousel_image.src = carousel_images[carousel_index]
        for i, dot in enumerate(dots.controls):
            dot.bgcolor = ft.Colors.INDIGO if i == carousel_index else ft.Colors.WHITE24
        page.update()

    def next_slide(e=None):
        nonlocal carousel_index
        carousel_index = (carousel_index + 1) % len(carousel_images)
        update_carousel()

    def prev_slide(e=None):
        nonlocal carousel_index
        carousel_index = (carousel_index - 1) % len(carousel_images)
        update_carousel()

    def auto_play():
        while True:
            time.sleep(3)
            next_slide()

    threading.Thread(target=auto_play, daemon=True).start()

    dots = ft.Row(
        controls=[
            ft.Container(width=10, height=10, border_radius=20,
                         bgcolor=ft.Colors.INDIGO if i == 0 else ft.Colors.WHITE24)
            for i in range(len(carousel_images))
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
    )
    dots.controls[0].bgcolor = ft.Colors.INDIGO

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

    # ===================================== FUNÇÕES PRINCIPAIS
    def ir_para_perfil(e):
        page.go("/perfil")

    def ir_para_aulas(e):
        page.go("/aulasView")

    def ir_para_suporte(e):
        page.go("/suporte")

    def mudar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        print(f"Tema alterado para: {page.theme_mode}")
        page.update()


    # TÍTULO DO APP BAR
    appbar_title = register_text_control(
        ft.Text("FÁBRICA DE PROGRAMADORES", weight="bold"),
        16,
        "appbar_title"
    )

    # BOTÃO ÚNICO PARA CONTROLE DE FONTE
    font_control_btn = ft.IconButton(
        ft.Icons.FONT_DOWNLOAD_ROUNDED,
        on_click=show_font_modal,
        tooltip="Ajustar tamanho da fonte"
    )

    appbar = ft.AppBar(
        leading_width=10,
        title=ft.Text("FÁBRICA DE PROGRAMADORES", weight="bold"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  
        actions=[ 
            font_control_btn,
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        text="TEMA",
                        icon="WB_SUNNY_OUTLINED", 
                        on_click=mudar_tema
                    ),
                    ft.PopupMenuItem(
                        text="FEEDBACK",
                        icon="SUN", 
                        on_click=lambda e: print("FEEDBACK")
                    ),
                    ft.PopupMenuItem(
                        text="CONFIGURAÇÕES",
                        icon="SETTINGS_OUTLINED", 
                        on_click=lambda e: print("CONFIGURAÇÕES")
                    ),
                    ft.PopupMenuItem(
                        text="SUPORTE",
                        icon="HELP_OUTLINE_ROUNDED", 
                        on_click=ir_para_suporte
                    ),
                    
                    ft.PopupMenuItem(
                        text="SAIR",
                        icon="CLOSE_ROUNDED", 
                        on_click=lambda e:page.go("/")
                    ),        
                ]
            ),
        ],
    )
    
    # PERFIL
    user_name = register_text_control(
        ft.Text("Usuário", size=20, weight="bold"),
        20,
        "user_name"
    )
    
    user_role = register_text_control(
        ft.Text("Programador Iniciante", size=14, color=ft.Colors.GREY_400),
        14,
        "user_role"
    )

    edit_profile_button = ft.ElevatedButton(
        text="Editar Perfil",
        icon=ft.Icons.EDIT_ROUNDED,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=ir_para_perfil
    )

    # Imagem do perfil (variável para permitir atualização dinâmica)
    profile_image = ft.Image(
        src=r"app\src\img\perfil.png",
        width=110,
        height=110,
        fit=ft.ImageFit.COVER,
    )

    # Funções para carregar e aplicar perfil do arquivo JSON
    def _perfil_json_path():
        try:
            base = Path(__file__).resolve().parent.parent
        except Exception:
            base = Path(os.getcwd())
        return base / "perfil_usuario.json"

    def load_profile_from_file():
        path = _perfil_json_path()
        if not path.exists():
            print(f"Arquivo de perfil não encontrado em: {path}")
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"Erro ao ler perfil: {e}")
            return {}

    def apply_profile_to_view(profile: dict):
        try:
            nome = profile.get("nome") or profile.get("Nome")
            email = profile.get("email") or profile.get("Email")
            foto = profile.get("foto") or profile.get("Foto")
            if nome:
                user_name.value = nome
            if email:
                user_role.value = email
            if foto:
                if isinstance(foto, str) and (foto.startswith("http://") or foto.startswith("https://")):
                    profile_image.src = foto
                else:
                    # tenta caminhos locais
                    local_path = Path(foto)
                    if not local_path.exists():
                        candidate = Path(__file__).resolve().parent / foto
                        if candidate.exists():
                            profile_image.src = str(candidate)
                        else:
                            profile_image.src = r"app\src\img\perfil.png"
                    else:
                        profile_image.src = str(local_path)
            page.update()
        except Exception as e:
            print(f"Erro ao aplicar perfil na view: {e}")

    def reload_profile(e=None):
        profile = load_profile_from_file()
        apply_profile_to_view(profile)

    # Watcher para perfil: monitora o arquivo perfil_usuario.json e recarrega quando mudar
    watcher_started = False

    def start_profile_watcher(poll_interval: float = 1.0):
        nonlocal watcher_started
        if watcher_started:
            return
        watcher_started = True

        def watcher():
            path = _perfil_json_path()
            try:
                last_mtime = path.stat().st_mtime if path.exists() else 0
            except Exception:
                last_mtime = 0
            while True:
                try:
                    time.sleep(poll_interval)
                    if not path.exists():
                        continue
                    mtime = path.stat().st_mtime
                    if mtime != last_mtime:
                        last_mtime = mtime
                        # schedule reload on the main thread
                        try:
                            page.call_later(lambda: reload_profile())
                        except Exception:
                            # fallback: call directly (may be unsafe in some environments)
                            try:
                                reload_profile()
                            except Exception as e:
                                print(f"Erro ao recarregar perfil pelo watcher: {e}")
                except Exception as e:
                    print(f"Erro no profile watcher: {e}")

        threading.Thread(target=watcher, daemon=True).start()

    perfil = ft.Container(
        content=ft.Row(
            spacing=20,
            controls=[
                ft.Container(
                    content=profile_image,
                    width=110,
                    height=110,
                    border_radius=55,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Column(
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        user_name,
                        user_role,
                        ft.Row(
                            spacing=8,
                            controls=[
                                edit_profile_button,
                                ft.IconButton(ft.Icons.REFRESH, tooltip="Atualizar perfil", on_click=reload_profile)
                            ]
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

    # MATERIAL DO CURSO
    material_title = register_text_control(
        ft.Text("MATERIAL DO CURSO", size=18, weight="bold"),
        18,
        "material_title"
    )

    python_title = register_text_control(
        ft.Text("AULAS DE PYTHON", weight="bold"),
        16,
        "python_title"
    )

    python_subtitle = register_text_control(
        ft.Text("70% DE APROVEITAMENTO DAS AULAS"),
        14,
        "python_subtitle"
    )

    api_title = register_text_control(
        ft.Text("AULAS DE API", weight="bold"),
        16,
        "api_title"
    )

    api_subtitle = register_text_control(
        ft.Text("30% DE APROVEITAMENTO DAS AULAS"),
        14,
        "api_subtitle"
    )

    notification_text = register_text_control(
        ft.Text("2", color=ft.Colors.WHITE, size=12, weight="bold"),
        12,
        "notification_badge"
    )

    eventos = ft.Container(
        on_click=lambda _:page.go("/aulasView"),
        ink=True,
        content=ft.Column(
            alignment=ft.alignment.center, 
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                material_title,
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Image(src="https://drive.google.com/uc?export=view&id=1oAQLNXquKlFrXdLdGKQjg1NbTw2i5J_D"),
                            title=python_title,
                            subtitle=python_subtitle,
                            trailing=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.GREEN)
                        ),
                        ft.ListTile(
                            leading=ft.Image(src="https://drive.google.com/uc?export=view&id=1VxIPRmy2Q0MTe8tU29uwhV2AxBiZay5D"),
                            title=api_title,
                            subtitle=api_subtitle,
                            trailing=ft.Container(
                                content=notification_text,
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

    def on_hover_eventos(e):
        eventos.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST if e.data == "true" else ft.Colors.SURFACE_CONTAINER_HIGHEST
        page.update()

    eventos.on_hover = on_hover_eventos

    # LINKS
    def abrir_link(e, url):
        page.launch_url(url)

    sites_title = register_text_control(
        ft.Text("SITES IMPORTANTES", size=18, weight="bold"),
        18,
        "sites_title"
    )

    fabrica_text = register_text_control(
        ft.Text("FÁBRICA", size=14, weight="bold"),
        14,
        "fabrica_text"
    )

    devs_text = register_text_control(
        ft.Text("DEVS", size=14, weight="bold"),
        14,
        "devs_text"
    )

    senai_text = register_text_control(
        ft.Text("SENAI", size=14, weight="bold"),
        14,
        "senai_text"
    )

    links = ft.Container(
        content=ft.Column(
            spacing=20,
            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                sites_title,
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
                                        src="https://drive.google.com/uc?export=view&id=1-sH8Vd08jPu8ZjwpkydJVtRGTSH1_3Ne",  
                                        width=90,
                                        height=90,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    width=80,
                                    height=80,
                                    border_radius=45,
                                    on_click=lambda e: abrir_link(e, "https://prefeitura.santanadeparnaiba.sp.gov.br/Plataforma/smti/fabrica-de-programadores"),
                                    ink=True,
                                ),
                                fabrica_text
                            ]
                        ),
                        ft.Column(
                            spacing=8,
                            horizontal_alignment="center",
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src="https://drive.google.com/uc?export=view&id=1DzOxTg51XO6DjMfzyD1u3YYmLI8rktLR",
                                        width=70,
                                        height=70,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    width=80,
                                    height=80,
                                    border_radius=15,
                                    on_click=lambda e: abrir_link(e, "https://anacastilhoathayde.github.io/Projeto_app/"),
                                    ink=True,
                                ),
                                devs_text
                            ]
                        ),
                        ft.Column(
                            spacing=8,
                            horizontal_alignment="center",
                            controls=[
                                ft.Container(
                                    content=ft.Image(
                                        src="https://drive.google.com/uc?export=view&id=1-q57xFQlgxe3TI_gZFuaOttBfNbmL_ic",
                                        width=70,
                                        height=70,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    width=80,
                                    height=80,
                                    border_radius=45,
                                    on_click=lambda e: abrir_link(e, "https://www.sp.senai.br/santanadeparnaiba"),
                                    ink=True,
                                ), 
                                senai_text
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

    # LISTVIEW PARA SCROLL VERTICAL
    content_listview = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        controls=[
            perfil,
            carousel,
            eventos,
            links,
        ]
    )

    # APLICA O TAMANHO INICIAL DA FONTE
    apply_font_size()

    # Carrega o perfil agora que todos os controles e funções foram definidos.
    try:
        reload_profile()
    except Exception as e:
        print(f"Falha ao carregar perfil na inicialização da view: {e}")

    # View final
    view = ft.View(
        route="/home",
        controls=[
            appbar,
            content_listview,
            navbar
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    # Inicia o scroll automático após a view estar pronta
    def on_view_loaded(e):
        start_auto_scroll()
        # inicia watcher para live-reload do perfil (ex.: login via Google atualiza perfil_usuario.json)
        try:
            start_profile_watcher()
        except Exception as ex:
            print(f"Não foi possível iniciar profile watcher: {ex}")
    
    # Adiciona um evento para quando a view for carregada
    view.on_load = on_view_loaded

    return view
