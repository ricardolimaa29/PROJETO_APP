import flet as ft
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




    # Configurando o NavigationBar
    navbar = ft.NavigationBar(
        selected_index=1,  # Definindo como 1 para destacar a tela de Desempenho
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




    # Conteúdo principal da tela de Desempenho
    content = ft.Column(
        controls=[
            ft.Text("Tela de Desempenho", size=24, weight="bold"),
            ft.Text("Aqui você pode ver suas estatísticas e progresso."),
            # Adicione mais controles específicos da tela de desempenho aqui
        ],
        alignment="center",
        horizontal_alignment="center",
        expand=True
    )




    # REMOVA esta linha problemática:




    # ===============================================================================




    card_colegio = ft.ResponsiveRow([
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Instituição / Turma", size=14,
                    text_align=ft.TextAlign.LEFT,
                    color="#333333"),
                   
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
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E0E0E0"),
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
                    ft.Text("Situação", size=14, color="#333333"),
                    ft.Text("Cursando", size=16, weight=ft.FontWeight.BOLD),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            ),
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E0E0E0"),
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
            ft.Text("Ocorrências", size=14, color="#333333"),
            texto_ocorrencia,
        ],
        spacing=6,
    ),
    bgcolor="#FFFFFF",
    border=ft.border.all(1, "#E0E0E0"),
    border_radius=8,
    expand=True,  # faz o container expandir
    padding=15,
    )




    ocorenrias_card = ft.Row(
        controls=[card_ocorrencias],
        expand=True,  # deixa o row expandir na tela
    )




    # Gera o gráfico e o converte em imagem
    def gerar_grafico(tipo="geral"):
        fig, ax = plt.subplots(figsize=(5, 3))
        materias = ["Módulo 1", "Módulo 2", "Módulo 3"]
        notas = [80, 90, 70]
        frequencias = [92, 87, 95]


        if tipo == "geral":
            largura = 0.35
            x = range(len(materias))
            barras_notas = ax.bar([i - largura/2 for i in x], notas, width=largura, label="Notas", color="#FF7B00")
            barras_freq = ax.bar([i + largura/2 for i in x], frequencias, width=largura, label="Frequência", color="#1465A7")
            ax.set_xticks(x)
            ax.set_xticklabels(["Modulo 1", "Modulo 2", "Modulo 3"])


            # Adiciona valores em % no topo das barras de notas
            for barra in barras_notas:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', ha='center', va='bottom', fontsize=8)


            # Adiciona valores em % no topo das barras de frequência
            for barra in barras_freq:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', ha='center', va='bottom', fontsize=8)


        elif tipo == "notas":
            barras_notas = ax.bar(materias, notas, color="#FF7B00")
            ax.set_xticklabels(["Modulo 1", "Modulo 2", "Modulo 3"])
            ax.set_title("Notas")


            for barra in barras_notas:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', ha='center', va='bottom', fontsize=8)


        elif tipo == "frequencia":
            barras_freq = ax.bar(materias, frequencias, color="#1465A7")
            ax.set_xticklabels(["Modulo 1", "Modulo 2", "Modulo 3"])
            ax.set_title("Frequência")


            for barra in barras_freq:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 1, f'{altura}%', ha='center', va='bottom', fontsize=8)


        ax.set_ylim(0, 110)  # dá um espaço extra para o texto no topo
        plt.tight_layout()






        # Converte o gráfico em imagem
        buf = io.BytesIO()
        plt.savefig(buf, format="png", transparent=True)
        plt.close(fig)
        buf.seek(0)
        # Usa o módulo base64 correto para converter
        img_base64 = base64.b64encode(buf.read()).decode()
        return ft.Image(src_base64=img_base64)




    grafico = ft.Container(content=gerar_grafico("geral"), alignment=ft.alignment.center)




    texto_legenda = ft.Column(
        [
            ft.Row([
                ft.Container(width=15, height=15, bgcolor="#FF7B00", border_radius=3),
                ft.Text("Notas", size=13)
            ], spacing=8),
            ft.Row([
                ft.Container(width=15, height=15, bgcolor="#1465A7", border_radius=3),
                ft.Text("Frequência", size=13)
            ], spacing=8),
        ],
        spacing=6,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.START
    )




    def atualizar(tipo):
        grafico.content = gerar_grafico(tipo)
        page.update()




    botoes = ft.Row(
        [
            ft.ElevatedButton("Geral", on_click=lambda e: atualizar("geral"), bgcolor="#FF7B00", color="white"),
            ft.ElevatedButton("Notas", on_click=lambda e: atualizar("notas"), bgcolor="#FF7B00", color="white"),
            ft.ElevatedButton("Frequência", on_click=lambda e: atualizar("frequencia"), bgcolor="#FF7B00", color="white"),
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
   
   
    page.add(appbar, navbar)
    page.add(
            topo,
        ft.Column(
            [




                texto_legenda,
                botoes,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           
        )
    )
    page.add(ocorenrias_card)




    # ===============================================================================




    return ft.View(
        route="/desempenho",
        controls=[
            appbar,
            content,  # Adicione o conteúdo aqui
            navbar
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )




ft.app(target=DesempenhoView)











