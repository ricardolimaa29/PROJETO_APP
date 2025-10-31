import flet as ft

def aulas_view(page: ft.Page):
    page.title = "Fábrica do Programador - Aulas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 500
    page.bgcolor = ft.Colors.BLACK

    # Configuração da janela (modo retrato)
    page.window.min_width = 500
    page.window.max_width = 500
    page.window.min_height = 800
    page.window.max_height = 800
    page.window.center()
    page.padding = 0

    # ---------- Cores e Tema ----------
    primary_color = ft.Colors.CYAN_400
    card_color = ft.Colors.GREY_800

    # ---------- Dados dos módulos com explicações detalhadas ----------
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
            ],
            "explicacoes": [
                "Aprenda a estrutura fundamental do Python: como escrever código, usar variáveis para armazenar dados e entender a indentação que é única do Python.",
                "Explore os diferentes tipos de dados (strings, números, booleanos) e operadores para manipular informações e realizar cálculos.",
                "Domine if, else e elif para criar programas que tomam decisões baseadas em condições específicas.",
                "Aprenda a criar funções reutilizáveis, entender escopo local e global, e organizar seu código de forma eficiente."
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
            ],
            "explicacoes": [
                "Domine listas - a estrutura mais versátil do Python. Aprenda a adicionar, remover, acessar e modificar elementos de forma eficiente.",
                "Explore dicionários para armazenar dados em pares chave-valor. Ideal para dados estruturados como informações de usuários.",
                "Conheça tuplas (imutáveis) e sets (coleções não ordenadas sem duplicatas) e quando usar cada uma.",
                "Aprenda comprehensions para criar listas, dicionários e sets de forma concisa e elegante em uma única linha."
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
            ],
            "explicacoes": [
                "Entenda o paradigma OOP: crie classes como modelos e objetos como instâncias. Aprenda atributos e métodos para modelar o mundo real.",
                "Domine herança para criar hierarquias de classes e polimorfismo para tratar objetos diferentes de forma uniforme.",
                "Aprenda encapsulamento para proteger dados internos usando atributos privados e métodos getters/setters.",
                "Explore métodos especiais como __init__, __str__, __len__ para dar comportamentos especiais às suas classes."
            ]
        },
    ]

    # ---------- Variável para controlar qual módulo está expandido ----------
    modulo_expandido = None

    # ---------- Funções de lógica ----------
    def calcular_progresso():
        total = len(modulos)
        concluidos = sum(1 for m in modulos if m["concluido"])
        return total, concluidos, (concluidos / total) * 100 if total else 0

    def marcar_concluido(index):
        modulos[index]["concluido"] = not modulos[index]["concluido"]
        atualizar_tela()

    def alternar_conclusao(index):
        marcar_concluido(index)
        fechar_detalhes()

    def abrir_detalhes(index):
        modulo = modulos[index]

        # Criar conteúdo dos detalhes com explicações
        conteudos_com_explicacoes = []
        for i, (conteudo, explicacao) in enumerate(zip(modulo["conteudos"], modulo["explicacoes"])):
            conteudos_com_explicacoes.extend([
                ft.Row([
                    ft.Icon(ft.Icons.PLAY_ARROW, size=14, color=ft.Colors.CYAN_400),
                    ft.Column([
                        ft.Text(conteudo, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(explicacao, color=ft.Colors.GREY_300, size=12)
                    ], spacing=2)
                ], spacing=10),
                ft.Container(height=8)  # Espaço entre os itens
            ])

        detalhes_content = ft.Column([
            ft.Text(modulo["titulo"], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300),
            ft.Text(modulo["descricao"], color=ft.Colors.GREY_300, italic=True),
            
            # Informações do módulo
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("NÍVEL", size=12, color=ft.Colors.GREY_400),
                            ft.Text(modulo["nivel"], size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=8
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("DURAÇÃO", size=12, color=ft.Colors.GREY_400),
                            ft.Text(modulo["duracao"], size=14, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=8
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("STATUS", size=12, color=ft.Colors.GREY_400),
                            ft.Text("Concluído" if modulo["concluido"] else "Em andamento", 
                                   size=14, 
                                   color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.YELLOW,
                                   weight=ft.FontWeight.BOLD)
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.GREY_800,
                        border_radius=8
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                margin=ft.margin.only(top=10, bottom=15)
            ),
            
            ft.Divider(color=ft.Colors.GREY_600),
            
            # Conteúdos com explicações
            ft.Text("CONTEÚDOS DETALHADOS:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300),
            ft.Container(height=10),
            *conteudos_com_explicacoes,
            
            # Botões de ação
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "Fechar", 
                    on_click=fechar_detalhes, 
                    bgcolor=ft.Colors.RED_700, 
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(padding=15)
                ),
                ft.ElevatedButton(
                    "Marcar como Concluído" if not modulo["concluido"] else "Marcar como Pendente",
                    on_click=lambda e: alternar_conclusao(index),
                    bgcolor=ft.Colors.GREEN_700 if not modulo["concluido"] else ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(padding=15)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], scroll=ft.ScrollMode.AUTO)

        dialog = ft.AlertDialog(
            title=ft.Text("Detalhes do Módulo", color=ft.Colors.WHITE),
            content=detalhes_content,
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.Colors.GREY_900
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def fechar_detalhes(e=None):
        if page.dialog:
            page.dialog.open = False
            page.update()

    def toggle_resumo(index):
        nonlocal modulo_expandido
        if modulo_expandido == index:
            modulo_expandido = None
        else:
            modulo_expandido = index
        atualizar_tela()

    # ---------- Criação dos cards ----------
    def criar_card(modulo, index):
        # Criar resumo do conteúdo
        resumo_content = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Resumo do Conteúdo:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300),
                    ft.Container(height=5),
                    *[
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=12, color=ft.Colors.GREEN_400),
                            ft.Text(conteudo, size=12, color=ft.Colors.GREY_300, expand=True)
                        ], spacing=5)
                        for conteudo in modulo["conteudos"]
                    ]
                ]),
                padding=15,
                bgcolor=ft.Colors.GREY_900,
                border_radius=8,
                margin=ft.margin.only(top=10)
            )
        ]) if modulo_expandido == index else None

        card_content = [
            ft.Row([
                ft.Icon(modulo["icon"], color=ft.Colors.CYAN_400),
                ft.Text(modulo["titulo"], weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE, expand=True),
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if modulo["concluido"] else ft.Icons.RADIO_BUTTON_UNCHECKED,
                    color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.GREY_600
                )
            ]),
            ft.Text(modulo["descricao"], size=12, color=ft.Colors.GREY_400),
            ft.Row([
                ft.Text(f"⏱️ {modulo['duracao']}", size=10, color=ft.Colors.GREY_400),
                ft.Text(f"Nível: {modulo['nivel']}", size=10, color=ft.Colors.CYAN_300)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.ElevatedButton(
                    "Ver Detalhes" if modulo_expandido != index else "Ocultar Resumo", 
                    on_click=lambda e: toggle_resumo(index), 
                    bgcolor=ft.Colors.CYAN_700, 
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(padding=10)
                ),
                ft.IconButton(
                    icon=ft.Icons.CHECK,
                    icon_color=ft.Colors.GREEN if modulo["concluido"] else ft.Colors.GREY_400,
                    tooltip="Marcar como concluído",
                    on_click=lambda e: marcar_concluido(index)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]

        # Adicionar resumo se estiver expandido
        if resumo_content:
            card_content.append(resumo_content)

        return ft.Card(
            elevation=4,
            color=card_color,
            content=ft.Container(
                content=ft.Column(card_content),
                padding=15
            ),
            margin=ft.margin.only(bottom=10)
        )

    # ---------- Progresso ----------
    total, concluidos, progresso = calcular_progresso()

    progresso_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("PROGRESSO GERAL", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(f"{concluidos}/{total} módulos", size=14, color=ft.Colors.GREY_400)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Stack([
                    ft.Container(height=10, border_radius=5, bgcolor=ft.Colors.GREY_800),
                    ft.Container(width=progresso * 3, height=10, border_radius=5, bgcolor=ft.Colors.CYAN_400)
                ]),
                height=10,
                margin=ft.margin.only(top=5, bottom=10)
            ),
            ft.Text(f"{progresso:.1f}% concluído", size=12, color=ft.Colors.CYAN_300)
        ]),
        padding=20,
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
        margin=10
    )

    # Função para atualizar os cards
    def atualizar_cards():
        cards_container.controls = [criar_card(m, i) for i, m in enumerate(modulos)]
        page.update()

    cards_container = ft.Column(
        controls=[criar_card(m, i) for i, m in enumerate(modulos)],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def atualizar_tela():
        total, concluidos, progresso = calcular_progresso()
        progresso_container.content.controls[0].controls[1].value = f"{concluidos}/{total} módulos"
        atualizar_cards()

    # ---------- Layout final ----------
    return ft.View(
        route="/aulas_view",
        controls=[
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="WHITE",
                    tooltip="Voltar",
                    on_click=lambda e: page.go("/home")
                )
            ], alignment="left"),
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
