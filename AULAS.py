import flet as ft

def aulasView(page: ft.Page):
    page.title = "Fábrica do Programador - Aulas"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    
    # Forçar janela em proporção 9:16 (tipo celular)
    page.window.width = 460
    page.window.min_width = 460
    page.window.max_width = 460
    page.window.height = 800
    page.window.min_height = 800
    page.window.max_height = 800
    page.padding = 0

    # Dados dos módulos
    modulos = [
        {
            "titulo": "Módulo 1: Fundamentos do Python",
            "descricao": "Domine os conceitos básicos da programação Python",
            "icon": ft.Icons.PLAY_ARROW,
            "nivel": "Iniciante",
            "duracao": "2 semanas",
            "concluido": False,
            "conteudos": [
                "Sintaxe básica e variáveis",
                "Tipos de dados e operadores",
                "Estruturas condicionais",
                "Funções e escopo"
            ]
        },
        {
            "titulo": "Módulo 2: Estruturas de Dados",
            "descricao": "Trabalhe com listas, dicionários e tuplas",
            "icon": ft.Icons.DATA_OBJECT,
            "nivel": "Iniciante",
            "duracao": "3 semanas",
            "concluido": True,
            "conteudos": [
                "Listas e operações",
                "Dicionários e métodos",
                "Tuplas e sets",
                "Comprehensions"
            ]
        },
        {
            "titulo": "Módulo 3: Programação Orientada a Objetos",
            "descricao": "Aprenda OOP com Python",
            "icon": ft.Icons.CODE,
            "nivel": "Intermediário",
            "duracao": "4 semanas",
            "concluido": False,
            "conteudos": [
                "Classes e objetos",
                "Herança e polimorfismo",
                "Encapsulamento",
                "Métodos especiais"
            ]
        },
        {
            "titulo": "Módulo 4: Projetos Práticos",
            "descricao": "Aplique seus conhecimentos em projetos reais",
            "icon": ft.Icons.BUILD,
            "nivel": "Intermediário",
            "duracao": "5 semanas",
            "concluido": False,
            "conteudos": [
                "Projeto 1: Sistema de tarefas",
                "Projeto 2: Análise de dados",
                "Projeto 3: API simples",
                "Projeto final"
            ]
        }
    ]

    def calcular_progresso():
        total = len(modulos)
        concluidos = sum(1 for m in modulos if m["concluido"])
        return total, concluidos, (concluidos / total) * 100 if total else 0

    def marcar_concluido(index):
        modulos[index]["concluido"] = not modulos[index]["concluido"]
        atualizar_tela()

    def criar_card(modulo, index):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(modulo["icon"], color=ft.Colors.CYAN_400),
                        ft.Text(modulo["titulo"], weight=ft.FontWeight.BOLD, size=16, 
                               color=ft.Colors.WHITE, expand=True),
                        ft.Icon(ft.Icons.CHECK_CIRCLE if modulo["concluido"] else ft.Icons.RADIO_BUTTON_UNCHECKED,
                               color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.GREY_600)
                    ]),
                    ft.Text(modulo["descricao"], size=12, color=ft.Colors.GREY_400),
                    ft.Row([
                        ft.Container(
                            content=ft.Text(modulo["nivel"], size=10, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_700,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=10
                        ),
                        ft.Text(f"⏱️ {modulo['duracao']}", size=10, color=ft.Colors.GREY_400),
                    ]),
                    ft.Row([
                        ft.ElevatedButton(
                            "Ver Detalhes",
                            on_click=lambda e, idx=index: abrir_detalhes(idx),
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.CYAN_700
                            )
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CHECK,
                            icon_color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.GREY_400,
                            tooltip="Marcar como concluído",
                            on_click=lambda e, idx=index: marcar_concluido(idx)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                padding=15
            ),
            margin=10,
            color=ft.Colors.ON_SURFACE_VARIANT
        )

    def abrir_detalhes(index):
        modulo = modulos[index]
        
        # Fechar qualquer diálogo aberto
        if len(page.overlay) > 0:
            page.overlay.pop()
        
        detalhes_content = ft.Column([
            ft.Text(modulo["titulo"], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(modulo["descricao"], color=ft.Colors.GREY_300),
            ft.Divider(),
            ft.Row([
                ft.Container(
                    content=ft.Text(modulo["nivel"], size=12, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.BLUE_700,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=10
                ),
                ft.Text(f"⏱️ {modulo['duracao']}", size=12, color=ft.Colors.GREY_400),
                ft.Icon(ft.Icons.CHECK_CIRCLE if modulo["concluido"] else ft.Icons.RADIO_BUTTON_UNCHECKED,
                       color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.GREY_600),
                ft.Text("Concluído" if modulo["concluido"] else "Pendente", 
                       size=12, color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.GREY_400)
            ]),
            ft.Divider(),
            ft.Text("Conteúdos do Módulo:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300),
            *[ft.Row([
                ft.Icon(ft.Icons.PLAY_ARROW, size=12, color=ft.Colors.GREEN),
                ft.Text(conteudo, size=14, color=ft.Colors.GREY_300, expand=True)
            ]) for conteudo in modulo["conteudos"]],
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Fechar",
                    on_click=fechar_detalhes,
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700)
                ),
                ft.ElevatedButton(
                    "Marcar como Concluído" if not modulo["concluido"] else "Marcar como Pendente",
                    on_click=lambda e, idx=index: alternar_conclusao(idx),
                    style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], scroll=ft.ScrollMode.AUTO)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Detalhes do Módulo"),
            content=detalhes_content,
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()

    def fechar_detalhes(e=None):
        page.dialog.open = False
        page.update()

    def alternar_conclusao(index):
        marcar_concluido(index)
        fechar_detalhes()

    def atualizar_tela():
        total, concluidos, progresso = calcular_progresso()
        
        # Atualizar barra de progresso
        progresso_container.content = ft.Column([
            ft.Row([
                ft.Text("PROGRESSO GERAL", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"{concluidos}/{total} módulos", size=14, color=ft.Colors.GREY_400)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Stack([
                    ft.Container(
                        height=10,
                        border_radius=5,
                        bgcolor=ft.Colors.GREY_800
                    ),
                    ft.Container(
                        width=(progresso_container.width * progresso / 100) if progresso_container.width else 0,
                        height=10,
                        border_radius=5,
                        bgcolor=ft.Colors.CYAN_400,
                        animate_size=300
                    )
                ]),
                height=10,
                margin=ft.margin.only(bottom=10)
            ),
            ft.Text(f"{progresso:.1f}% concluído", size=12, color=ft.Colors.CYAN_300)
        ])
        
        # Atualizar cards
        cards_container.controls = [criar_card(m, i) for i, m in enumerate(modulos)]
        page.update()

    # Layout principal
    total, concluidos, progresso = calcular_progresso()
    
    progresso_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("PROGRESSO GERAL", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"{concluidos}/{total} módulos", size=14, color=ft.Colors.GREY_400)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Stack([
                    ft.Container(
                        height=10,
                        border_radius=5,
                        bgcolor=ft.Colors.GREY_800
                    ),
                    ft.Container(
                        width=0,
                        height=10,
                        border_radius=5,
                        bgcolor=ft.Colors.CYAN_400,
                        animate_size=300
                    )
                ]),
                height=10,
                margin=ft.margin.only(bottom=10)
            ),
            ft.Text(f"{progresso:.1f}% concluído", size=12, color=ft.Colors.CYAN_300)
        ]),
        padding=20,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        margin=10,
        border_radius=10
    )

    cards_container = ft.Column(
        controls=[criar_card(m, i) for i, m in enumerate(modulos)],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Adicionar tudo à página

    # Forçar atualização inicial da barra de progresso
    def on_resize(e):
        atualizar_tela()
    
    page.on_resize = on_resize
    atualizar_tela()

    return ft.View(
        route="/aulasView",
        controls=[ft.Row([ft.IconButton(
        icon="ARROW_BACK",
        icon_color="WHITE",
        tooltip="Voltar",
        on_click=lambda e: page.go("/home"))], alignment="left"),
           ft.Column([
            ft.Container(
                content=ft.Text("AULAS", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=20,
                alignment=ft.alignment.center
            ),
            progresso_container,
            cards_container
        ], expand=True)
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
