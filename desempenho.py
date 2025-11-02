from flet import *
import flet as ft
from home import HomeView
from detalhes import DetalhesView

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
    # page.scroll = 'auto'
    page.scroll = ft.ScrollMode.AUTOpage.scroll = ft.ScrollMode.AUTO

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
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        print(f"Tema alterado para: {page.theme_mode}")
        page.update()

    
    def voltar_home(a):
        page.views.append(HomeView(page))

    
     
    


        #============================================================
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


    titulo_grafico = ft.Text(
    "Geral",
    # weight=ft.FontWeight.BOLD,
    size=22,
    # weight=ft.FontWeight.W_500,
    # color=ft.Colors.GREY_400,
    text_align=ft.TextAlign.CENTER,
    )


        # Dados dos módulos
    modulos = ["Módulo 1", "Módulo 2", "Módulo 3"]
    notas = [80, 90, 70]
    frequencias = [92, 87, 95]

    # Container do gráfico
    grafico_container = ft.Container(
        width=440,
        height=300,
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=12)
    )

    # Variável para controlar o segmento selecionado
    selected_index = ft.Ref[ft.CupertinoSlidingSegmentedButton]()




    def criar_grafico_barras(tipo="geral"):
        bar_groups = []

        for i in range(len(modulos)):
            if tipo == "geral":
                valor1 = notas[i]
                valor2 = frequencias[i]
                cor1 = ft.Colors.INDIGO
                cor2 = ft.Colors.GREEN
                tooltip1 = f"Nota: {valor1}%"
                tooltip2 = f"Frequência: {valor2}%"

            elif tipo == "frequencia":
                valor1 = frequencias[i]
                valor2 = 100 - frequencias[i]
                cor1 = ft.Colors.GREEN
                cor2 = ft.Colors.RED
                tooltip1 = f"Presentes: {valor1}%"
                tooltip2 = f"Ausentes: {valor2}%"

            elif tipo == "notas":
                prova1 = [70, 85, 60]  # exemplo
                prova2 = [80, 90, 75]  # exemplo
                valor1 = prova1[i]
                valor2 = prova2[i]
                cor1 = ft.Colors.INDIGO
                cor2 = ft.Colors.ORANGE
                tooltip1 = f"Prova 1: {valor1}%"
                tooltip2 = f"Prova 2: {valor2}%"

            bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(from_y=0, to_y=valor1, width=20, color=cor1, tooltip=tooltip1, border_radius=0),
                        ft.BarChartRod(from_y=0, to_y=valor2, width=20, color=cor2, tooltip=tooltip2, border_radius=0),
                    ],
                )
            )

        labels_eixo_y = [ft.ChartAxisLabel(value=i, label=ft.Text(f"{i}%", size=8)) for i in range(0, 110, 10)]

        chart = ft.BarChart(
            bar_groups=bar_groups,
            left_axis=ft.ChartAxis(labels=labels_eixo_y),
            bottom_axis=ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=j, label=ft.Text(modulos[j], size=12)) for j in range(len(modulos))]
            ),
            max_y=100,
            border=ft.border.all(1, ft.Colors.GREY_700),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.GREY_700, width=1, dash_pattern=[3,3]),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            expand=True,
            interactive=True
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

        # Atualizar o texto da faixa conforme o botão selecionado
        if tipo_selecionado == "geral":
            titulo_grafico.value = "Geral"
        elif tipo_selecionado == "notas":
            titulo_grafico.value = "Aproveitamento"
        else:
            titulo_grafico.value = "Frequência"

        legenda_container.content = criar_legenda(tipo_selecionado)
        page.update()

    
    # para ciar la legenda

    
    

    def criar_legenda(tipo="geral"):
        if tipo == "geral":
            legenda = ft.Row(
                [
                    ft.Row(
                        [ft.Container(width=15, height=15, bgcolor=ft.Colors.INDIGO, border_radius=2), ft.Text("Notas")],
                        spacing=5,
                    ),
                    ft.Row(
                        [ft.Container(width=15, height=15, bgcolor=ft.Colors.GREEN, border_radius=2), ft.Text("Frequência")],
                        spacing=5,
                    ),
                ],
                spacing=20,
            )

        elif tipo == "notas":  # ✅ Corrigido (antes era "aproveitamento")
            legenda = ft.Row(
                [
                    ft.Row(
                        [ft.Container(width=15, height=15, bgcolor=ft.Colors.INDIGO, border_radius=2), ft.Text("Prova 1")],
                        spacing=5,
                    ),
                    ft.Row(
                        [ft.Container(width=15, height=15, bgcolor=ft.Colors.ORANGE, border_radius=2), ft.Text("Prova 2")],
                        spacing=5,
                    ),
                ],
                spacing=20,
            )

        else:  # frequencia
            legenda = ft.Row(
                [
                    ft.Row(
                        [ft.Container(width=15, height=15, bgcolor=ft.Colors.GREEN, border_radius=2), ft.Text("Presente")],
                        spacing=5,
                    ),
                    ft.Row(
                        [ft.Container(width=15, height=15, bgcolor=ft.Colors.RED, border_radius=2), ft.Text("Ausente")],
                        spacing=5,
                    ),
                ],
                spacing=20,
            )

        return legenda
    
    def abrir_detalhes(e):
        page.views.append(DetalhesView(page))
        page.go("/detalhes")  # navega para a view recém adicionada
        #AeDfRyji

        

    botao_detalhes = ft.CupertinoButton(
            content=ft.Text("Detalhes", color="#d8d5d5"),
            bgcolor=ft.Colors.INDIGO,
            # disabled=True,
            expand=True,
            width=480,
            height=40,
            padding=1,
            # alignment=ft.alignment.top_left,
            opacity_on_click=0.5,
            on_click=abrir_detalhes
        )
    
    #AA
    legenda_container = ft.Container(
    content=criar_legenda("geral"),
    margin=ft.margin.only(top=10),
    
    )
    
    

    
    
    # Botão de controle com CupertinoSlidingSegmentedButton
    segmented_button = ft.CupertinoSlidingSegmentedButton(
        selected_index=0,
        width=480,
        thumb_color=ft.Colors.INDIGO,
        on_change=atualizar_grafico,
        controls=[
            ft.Text("Geral"),
            ft.Text("Aproveitamento"),
            ft.Text("Frequência"),
        ],
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
        # spacing=6,
    ),
    border=ft.border.all(1),
    border_radius=8,
    expand=True,  # faz o container expandir
    padding=15,
    
    )

    ocorenrias_card = ft.Row(
        controls=[card_ocorrencias],
        expand=True, 
         
    )

    

    topo = ft.Column(
            [
                card_colegio,
                ft.Container(height=10),
                card_situacao,
                titulo_grafico,
                grafico_container,
                legenda_container,
                ft.Container(height=10),
                segmented_button,
                ft.Container(height=10),
                botao_detalhes
                # grafico,
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
   
    # page.add(topo, appbar, navbar, ocorenrias_card)

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

# ft.app(target = DesempenhoView)