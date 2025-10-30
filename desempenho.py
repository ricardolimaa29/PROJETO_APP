from flet import *
import flet as ft
# import matplotlib.pyplot as plt
# import io
# import base64

def DesempenhoView(page: ft.Page):
   
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.title = "PROGRAMADORES"
    page.window.width = 500
    page.window.height = 800
    page.window.max_width = 500
    page.window.max_height = 800
    page.window.min_width = 500
    page.window.min_height = 800
    page.scroll = 'auto'

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
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        print(f"Tema alterado para: {page.theme_mode}")
        
        # # Atualizar o gráfico quando o tema mudar
        # grafico.content = gerar_grafico(tipo_grafico_atual)
        # page.update()

        # Dados dos módulos
    modulos = ["Modulo 1", "Modulo 2", "Modulo 3"]
    notas = [80, 90, 70]
    frequencias = [92, 87, 95]

    # Container do gráfico
    grafico_container = ft.Container(
        width=450,
        height=300,
        alignment=ft.alignment.center,
    )

    # Variável para controlar o segmento selecionado
    selected_index = ft.Ref[ft.CupertinoSlidingSegmentedButton]()

    def criar_grafico_barras(tipo="geral"):
        if tipo == "geral":
            # Gráfico com barras agrupadas (notas e frequência)
            grupos_barras = [
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=notas[i],
                            width=20,
                            color=ft.Colors.INDIGO,
                            border_radius=0,
                            tooltip=f"Nota: {notas[i]}%",
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=frequencias[i],
                            width=20,
                            color=ft.Colors.BLUE,
                            border_radius=0,
                            tooltip=f"Frequência: {frequencias[i]}%",
                        ),
                    ],
                )
                for i in range(3)
            ]
            
        elif tipo == "notas":
            # Gráfico apenas de notas
            grupos_barras = [
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=notas[i],
                            width=20,
                            color=ft.Colors.INDIGO,
                            border_radius=0,
                            tooltip=f"Nota: {notas[i]}%",
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=notas[i],
                            width=20,
                            color=ft.Colors.INDIGO,
                            border_radius=0,
                            tooltip=f"Nota: {notas[i]}%",
                        ),
                    ],
                )
                for i in range(3)
            ]
            
        elif tipo == "frequencia":
            # Gráfico apenas de frequência
            grupos_barras = [
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=frequencias[i],
                            width=20,
                            color=ft.Colors.BLUE,
                            border_radius=0,
                            tooltip=f"Frequência: {frequencias[i]}%",
                        ),
                        ft.BarChartRod(
                            from_y=0,
                            to_y=frequencias[i],
                            width=20,
                            color=ft.Colors.BLUE,
                            border_radius=0,
                            tooltip=f"Frequência: {frequencias[i]}%",
                        ),
                    ],
                )
                for i in range(3)
            ]
        
        # Criar labels de 10 em 10 de forma explícita
        labels_eixo_y = [
            ft.ChartAxisLabel(value=0, label=ft.Text("0%", size=10)),
            ft.ChartAxisLabel(value=10, label=ft.Text("10%", size=10)),
            ft.ChartAxisLabel(value=20, label=ft.Text("20%", size=10)),
            ft.ChartAxisLabel(value=30, label=ft.Text("30%", size=10)),
            ft.ChartAxisLabel(value=40, label=ft.Text("40%", size=10)),
            ft.ChartAxisLabel(value=50, label=ft.Text("50%", size=10)),
            ft.ChartAxisLabel(value=60, label=ft.Text("60%", size=10)),
            ft.ChartAxisLabel(value=70, label=ft.Text("70%", size=10)),
            ft.ChartAxisLabel(value=80, label=ft.Text("80%", size=10)),
            ft.ChartAxisLabel(value=90, label=ft.Text("90%", size=10)),
            ft.ChartAxisLabel(value=100, label=ft.Text("100%", size=10)),
        ]
        
        # Gráfico com eixo Y à esquerda
        chart = ft.BarChart(
            bar_groups=grupos_barras,
            border=ft.border.all(1, ft.Colors.GREY_700),
            left_axis=ft.ChartAxis(
                labels=labels_eixo_y,
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text(modulos[0], size=12)),
                    ft.ChartAxisLabel(value=1, label=ft.Text(modulos[1], size=12)),
                    ft.ChartAxisLabel(value=2, label=ft.Text(modulos[2], size=12)),
                ],
                labels_size=80,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_700, 
                width=1, 
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            max_y=100,
            interactive=True,
            expand=True,
        )
        
        return chart

    # Inicializar com gráfico geral
    grafico_container.content = criar_grafico_barras("geral")

    # Função para atualizar o gráfico
    def atualizar_grafico(e):
        tipos = ["geral", "notas", "frequencia"]
        tipo_selecionado = tipos[e.control.selected_index]
        grafico_container.content = criar_grafico_barras(tipo_selecionado)
        page.update()

    # Botão de controle com CupertinoSlidingSegmentedButton
    segmented_button = ft.CupertinoSlidingSegmentedButton(
        selected_index=0,
        on_change=atualizar_grafico,
        controls=[
            ft.Text("Geral"),
            ft.Text("Aproveitamento"),
            ft.Text("Frequência"),
        ],
    )

    # ===================================== CRIANDO ELEMENTOS
    from home import HomeView
    def voltar_home(a):
        page.views.append(HomeView(page))

    appbar = ft.AppBar(
    leading=ft.IconButton(
        ft.Icons.ARROW_BACK,
        on_click=voltar_home,
    ), 
    title=ft.Text("DESEMPENHO", weight="bold"),  # título da AppBar
    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,  # cor de fundo
    actions=[  # ações do lado direito
        ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="TEMA", icon="WB_SUNNY_OUTLINED", on_click=mudar_tema),
                ft.PopupMenuItem(text="CONFIGURAÇÕES", icon="SETTINGS_OUTLINED", on_click=clicou_menu),
                ft.PopupMenuItem(text="SUPORTE", icon="HELP_OUTLINE_ROUNDED", on_click=clicou_menu),
                ft.PopupMenuItem(),  # separador
                ft.PopupMenuItem(text="SAIR", icon="CLOSE_ROUNDED", on_click=clicou_menu),
            ]
        ),
    ],
    )
     
    # Função para mudar de tela conforme índice do NavigationBar    
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
        on_change=mudar_tela
    )

    

    card_colegio = ft.ResponsiveRow([
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Instituição / Turma", size=14,
                    text_align=ft.TextAlign.LEFT,
                    color="#888888"),
                   
                    ft.Text(
                        "FABRICA DE PROGRAMADORES\nSALA 03 - 14h",
                        size=15,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.LEFT
                    ),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border=ft.border.all(1),
            border_radius=8,
            padding=15,
            expand=True,
        )
    ])

    card_situacao = ft.ResponsiveRow(
    [
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Situação", size=14, color="#888888"),
                    ft.Text("Cursando", size=16, weight=ft.FontWeight.BOLD),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            ),
            border=ft.border.all(1),
            border_radius=8,
            padding=15,
            expand=True,
            alignment=ft.alignment.center,
        )
    ]
    )

    ocorrencias = []  # lista de ocorrências (vazia = nenhuma)

    texto_ocorrencia = (
        ft.Text("Nenhuma ocorrência registrada", color="#888888", size=14)
        if not ocorrencias
        else ft.Column([ft.Text(o, size=14) for o in ocorrencias])
    )

    card_ocorrencias = ft.Container(
    content=ft.Column(
        [
            ft.Text("Ocorrências", size=14),
            texto_ocorrencia,
        ],
        spacing=6,
    ),
    border=ft.border.all(1),
    border_radius=8,
    expand=True,  # faz o container expandir
    padding=15,
    )

    ocorenrias_card = ft.Row(
        controls=[card_ocorrencias],
        expand=True,  # deixa o row expandir na tela
    )


    topo = ft.Column(
            [
                card_colegio,
                ft.Container(height=10),
                card_situacao,
                grafico_container,
                segmented_button,
                # grafico,
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
   

    return ft.View(
        route="/desempenho",
        controls=[
            topo,
            appbar,
            navbar,
            ocorenrias_card
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )

