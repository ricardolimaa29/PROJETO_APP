import flet as ft
# from desempenho import DesempenhoView
from app_settings import write_theme, apply_theme

def DetalhesView(page: ft.Page): 
    # Aplica o tema persistido
    try:
        apply_theme(page)
    except Exception:
        page.theme_mode = ft.ThemeMode.DARK
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.title = "DETALHES"
    page.window.width = 500
    page.window.height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.scroll = 'auto'


    page.padding = 0

    # ===================================== CRIANDO FUNÇÕES DOS ELEMENTOS
    def clicou_menu(e):
        item = e.control.text
        if item == "Suporte":
            print("Abrir suporte...")
        elif item == "Configurações":
            print("Abrir configurações...")
        elif item == "Tema":
            mudar_tema(None)

    def mudar_tema(a):
        try:
            if page.theme_mode == ft.ThemeMode.DARK:
                write_theme("light")
            else:
                write_theme("dark")
            apply_theme(page)
            print(f"Tema alterado para: {page.theme_mode}")
            page.update()
        except Exception as ex:
            print(f"Erro ao alterar tema: {ex}")


    appbar = ft.AppBar(
    leading=ft.IconButton(
        ft.Icons.ARROW_BACK,
        on_click=lambda _:page.go('/desempenho'),
    ), 
    title=ft.Text("DETALHES", weight="bold"),  
    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  
    actions=[  
        ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                ft.PopupMenuItem(),  # separador
                ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=lambda e:page.go("/")),
            ]
        ),
    ],
    )

    def aproveitamento():
        modulos = [
            {
                "modulo": "Módulo 1",
                "provas": [
                    {"nome": "Prova 1", "nota": 10.0},
                    {"nome": "Prova 2", "nota": 9.0}
                ]
            },
            {
                "modulo": "Módulo 2",
                "provas": [
                    {"nome": "Prova 1", "nota": 8.0},
                    {"nome": "Prova 2", "nota": 9.5},
                ]
            },
            {
                "modulo": "Módulo 3",
                "provas": [
                    {"nome": "Prova 1", "nota": 10.0},
                    {"nome": "Prova 2", "nota": 9.5},
                ]
            }
        ]

        expansion_panels = []
        for m in modulos:
            provas_coluna = ft.Column([
                ft.Container(
    content=ft.Row(
        [
            ft.Text(p["nome"]),
            ft.Text(f"{p['nota']:.2f}")
        ],
        alignment="spaceBetween",
    ),
    padding=ft.padding.symmetric(vertical=5, horizontal=15)
    )

                for p in m["provas"]
            ])

            media = sum(p["nota"] for p in m["provas"]) / len(m["provas"])
            expansion_panels.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(
                        title=ft.Text(m["modulo"], weight="bold"),
                        subtitle=ft.Text(f"Nota do módulo: {media:.2f}")
                    ),
                    content=provas_coluna
                )
            )

        return ft.ExpansionPanelList(
            controls=expansion_panels,
            # expand_icon_color="#0D47A1"
        )



    # ==================== FUNÇÃO FREQUÊNCIA ====================
    def frequencia():
        meses = [
            {"mes": "Janeiro", "faltas": 0},
            {"mes": "Fevereiro", "faltas": 1, "dias": ["02"]},
            {"mes": "Março", "faltas": 0},
            {"mes": "Abril", "faltas": 1, "dias": ["14"]},
            {"mes": "Junho", "faltas": 3, "dias": ["02", "06", "16"]},
            {"mes": "Julho", "faltas": 2, "dias": ["06", "08"]},
            {"mes": "Agosto", "faltas": 2, "dias": ["12", "20"]},
        ]

        expansion_panels = []
        for m in meses:
            dias_lista = m.get("dias", [])
            if dias_lista:
                dias = ft.Column([
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(dia, size=16),
                                # ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE)
                            ],
                            alignment="spaceBetween"
                        ),
                        padding=ft.padding.symmetric(vertical=5, horizontal=15)
                    )
                    for dia in dias_lista
                ])
            else:
                dias = ft.Container(
                    content=ft.Text("Sem faltas neste mês", italic=True),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15)
                )

            expansion_panels.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(
                        title=ft.Text(m["mes"], weight="bold", size=16),
                        subtitle=ft.Text(f"{m['faltas']} falta(s)")
                    ),
                    content=dias
                )
            )

        return ft.ExpansionPanelList(
            controls=expansion_panels,
            expand_icon_color="#0D47A1"
        )

    # ==================== ÁREA DE CONTEÚDO DINÂMICA ====================
    conteudo = ft.Column(expand=True)
    conteudo.controls.append(aproveitamento())  # instanciando desde o começo

    def trocar_segmento(e):
        conteudo.controls.clear()
        if e.control.selected_index == 0:
            conteudo.controls.append(aproveitamento())
        else:
            conteudo.controls.append(frequencia())
        conteudo.update()



    segmented_button = ft.CupertinoSlidingSegmentedButton(
        selected_index=0,
        width=480,
        height=30,
        thumb_color=ft.Colors.INDIGO,
        on_change=trocar_segmento,
        controls=[
            ft.Text("Aproveitamento"),
            ft.Text("Frequência")
        ]
    )

    # ==================== RETORNANDO VIEW ====================
    return ft.View(
        route="/detalhes",
        controls=[
            appbar,
            segmented_button,
            conteudo
        ]
    )

