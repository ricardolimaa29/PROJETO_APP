from flet import *
import flet as ft
import matplotlib.pyplot as plt
import io
import base64

def DesempenhoView(page: ft.Page):
   
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
        
        # Atualizar o gráfico quando o tema mudar
        grafico.content = gerar_grafico(tipo_grafico_atual)
        page.update()

    # ===================================== CRIANDO ELEMENTOS
    appbar = ft.AppBar(
        leading_width=10,
        title=ft.Text("DESEMPENHO", weight="bold"),
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
     
    # Função para mudar de tela conforme índice do NavigationBar
    def mudar_tela(e):
        num = e.control.selected_index
        if num == 0:
            print("Indo para Início...")
        elif num == 1:
            print("Indo para Desempenho...")
        elif num == 2:
            print("Indo para Notificações...")
        elif num == 3:
            print("Indo para Perfil...")
        page.update()


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

    # Variável para controlar o tipo de gráfico atual
    tipo_grafico_atual = "geral"

    # Gera o gráfico e o converte em imagem
    def gerar_grafico(tipo="geral"):
        global tipo_grafico_atual
        tipo_grafico_atual = tipo
        
        # Define cores baseadas no tema
        if page.theme_mode == ft.ThemeMode.DARK:
            # Tema escuro: texto branco, fundo transparente
            cor_texto = "white"
            cor_fundo = "none"
            cor_grade = "#444444"
        else:
            # Tema claro: texto preto, fundo transparente
            cor_texto = "black"
            cor_fundo = "none"
            cor_grade = "#dddddd"
        
        # Configurar estilo do matplotlib baseado no tema
        plt.rcParams.update({
            'text.color': cor_texto,
            'axes.labelcolor': cor_texto,
            'axes.edgecolor': cor_texto,
            'axes.facecolor': cor_fundo,
            'figure.facecolor': cor_fundo,
            'xtick.color': cor_texto,
            'ytick.color': cor_texto,
            'grid.color': cor_grade
        })
        
        fig, ax = plt.subplots(figsize=(5, 3))
        
        # Definir cores das barras baseadas no tema
        if page.theme_mode == ft.ThemeMode.DARK:
            cor_notas = "#FF7B00"  # Laranja
            cor_frequencia = "#1465A7"  # Azul
        else:
            cor_notas = "#FF7B00"  # Laranja (mantém as cores originais no tema claro)
            cor_frequencia = "#1465A7"  # Azul
        
        materias = ["Módulo 1", "Módulo 2", "Módulo 3"]
        notas = [80, 90, 70]
        frequencias = [92, 87, 95]

        if tipo == "geral":
            largura = 0.35
            x = range(len(materias))
            barras_notas = ax.bar([i - largura/2 for i in x], notas, width=largura, label="Notas", color=cor_notas)
            barras_freq = ax.bar([i + largura/2 for i in x], frequencias, width=largura, label="Frequência", color=cor_frequencia)
            ax.set_xticks(x)
            ax.set_xticklabels(["Modulo 1", "Modulo 2", "Modulo 3"])
            ax.legend()

            # Adiciona valores em % no topo das barras de notas
            for barra in barras_notas:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', 
                       ha='center', va='bottom', fontsize=8, color=cor_texto)

            # Adiciona valores em % no topo das barras de frequência
            for barra in barras_freq:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', 
                       ha='center', va='bottom', fontsize=8, color=cor_texto)

        elif tipo == "notas":
            barras_notas = ax.bar(materias, notas, color=cor_notas)
            ax.set_xticklabels(["Modulo 1", "Modulo 2", "Modulo 3"])
            ax.set_title("Notas", color=cor_texto)

            for barra in barras_notas:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', 
                       ha='center', va='bottom', fontsize=8, color=cor_texto)

        elif tipo == "frequencia":
            barras_freq = ax.bar(materias, frequencias, color=cor_frequencia)
            ax.set_xticklabels(["Modulo 1", "Modulo 2", "Modulo 3"])
            ax.set_title("Frequência", color=cor_texto)

            for barra in barras_freq:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', 
                       ha='center', va='bottom', fontsize=8, color=cor_texto)

        ax.set_ylim(0, 110)  # dá um espaço extra para o texto no topo
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        # Converte o gráfico em imagem
        buf = io.BytesIO()
        plt.savefig(buf, format="png", transparent=True, bbox_inches='tight', 
                   facecolor=cor_fundo, edgecolor='none')
        plt.close(fig)
        buf.seek(0)
        # Usa o módulo base64 correto para converter
        img_base64 = base64.b64encode(buf.read()).decode()
        return ft.Image(src_base64=img_base64)

    grafico = ft.Container(content=gerar_grafico("geral"), alignment=ft.alignment.center)

    def atualizar(tipo):
        grafico.content = gerar_grafico(tipo)
        page.update()

    botoes = ft.Row(
        [
            ft.ElevatedButton("Geral", on_click=lambda e: atualizar("geral")),
            ft.ElevatedButton("Aproveitamento", on_click=lambda e: atualizar("notas")),
            ft.ElevatedButton("Frequência", on_click=lambda e: atualizar("frequencia")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    topo = ft.Column(
            [
                card_colegio,
                ft.Container(height=10),
                card_situacao,
                grafico,
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    return ft.View(
    route="/desempenho",
    controls=[
        appbar,
        navbar,
        topo,
        ft.Column(
            controls=[botoes],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ocorenrias_card,
    ]
)


