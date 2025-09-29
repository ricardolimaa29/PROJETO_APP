import flet as ft
import time
import threading

class HomeView:
    def __init__(self):
        # Cores
        self.cor_primaria = "#1E5FE9"
        self.cor_secundaria = "#2AC9A6"
        
        # Imagens do carrossel
        self.imagens_carrossel = [
            "img\\fabrica.jpg",
            "img\\premio.jpg",
            "img\\programa.jpg",
            "img\\santana.jpg"
        ]
        
        # Estados
        self.indice_carrossel = 0
        self.indice_selecionado = 0
        self.carrossel_auto = True
        self.menu_aberto = False

    def criar_menu_lateral(self, pagina):
        """Cria o menu lateral com animação"""
        
        def alternar_menu(e):
            self.menu_aberto = not self.menu_aberto
            menu_lateral.width = 280 if self.menu_aberto else 0
            fundo_escuro.opacity = 0.4 if self.menu_aberto else 0
            fundo_escuro.visible = self.menu_aberto
            pagina.update()

        def clicar_menu(e):
            texto_item = e.control.content.controls[1].value
            print(f"Item {texto_item} clicado!")
            alternar_menu(e)

        def mudar_tema(e):
            # Alternar entre claro e escuro
            if pagina.theme_mode == ft.ThemeMode.DARK:
                pagina.theme_mode = ft.ThemeMode.LIGHT
            else:
                pagina.theme_mode = ft.ThemeMode.DARK
            print(f"Tema alterado para: {pagina.theme_mode}")
            pagina.update()

        # Fundo escuro quando menu abre
        fundo_escuro = ft.Container(
            expand=True, 
            bgcolor="black", 
            opacity=0, 
            visible=False,
            on_click=alternar_menu, 
            animate_opacity=300
        )

        # Menu lateral
        menu_lateral = ft.Container(
            width=0, 
            height=pagina.height, 
            bgcolor="white",
            content=ft.Column([
                # Cabeçalho do menu
                ft.Container(
                    content=ft.Row([
                        ft.Text("MENU", size=20, weight="bold", color="white"),
                    ], alignment="center"),
                    bgcolor=self.cor_primaria, 
                    padding=15, 
                    height=70,
                    border_radius=3, 
                    margin=1
                ),
                
                # Itens do menu
                ft.Container(
                    content=ft.Column([
                        self.item_menu("HOME", "INÍCIO", clicar_menu),
                        ft.Divider(height=1),
                        self.item_menu("WB_SUNNY_OUTLINED", "TEMA", mudar_tema),
                        ft.Divider(height=1),
                        self.item_menu("SUPPORT", "SUPORTE", clicar_menu),
                        ft.Divider(height=1),
                        ft.Container(expand=True),  # Espaço vazio
                        self.item_menu("EXIT_TO_APP", "SAIR", clicar_menu, eh_saida=True),
                    ], spacing=0),
                    padding=10, 
                    expand=True
                )
            ], spacing=0),
            animate=300, 
            right=0, 
            top=0,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK54)
        )

        return fundo_escuro, menu_lateral, alternar_menu

    def item_menu(self, icone, texto, ao_clicar, eh_saida=False):
        """Cria um item do menu lateral"""
        cor = "#ef4444" if eh_saida else self.cor_primaria
        cor_fundo = "#fee2e2" if eh_saida else "#e0e7ff"
        
        return ft.Container(
            content=ft.Row([
                # Ícone
                ft.Container(
                    content=ft.Icon(icone, color=cor, size=20),
                    bgcolor=cor_fundo, 
                    padding=10, 
                    border_radius=10, 
                    width=40, 
                    height=40
                ),
                # Texto
                ft.Text(texto, weight="bold", color=cor, size=16)
            ], spacing=15),
            padding=15, 
            on_click=ao_clicar, 
            border_radius=10,
            bgcolor={"": "transparent", "hovered": "#f1f5f9"}
        )

    def criar_cabecalho(self, funcao_alternar_menu):
        """Cria o cabeçalho da aplicação"""
        return ft.Container(
            content=ft.Row([
                # Botão menu
                ft.IconButton(
                    icon="MENU", 
                    icon_color="#FFFFFF", 
                    icon_size=30,
                    on_click=funcao_alternar_menu, 
                    tooltip="Abrir Menu"
                ),
                # Título
                ft.Text("FÁBRICA DE PROGRAMADORES", 
                       size=22, 
                       weight="bold", 
                       color="#ffffff", 
                       text_align=ft.TextAlign.CENTER, 
                       expand=True),
            ], alignment=ft.MainAxisAlignment.START),
            bgcolor=self.cor_primaria, 
            padding=20, 
            height=70, 
            border_radius=10, 
            margin=1
        )

    def criar_secao_perfil(self, funcao_selecionar_foto):
        """Cria a seção de perfil do usuário"""
        return ft.Container(
            content=ft.Row([
                # Foto de perfil
                ft.Stack([
                    ft.Image(
                        src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200",
                        width=110, 
                        height=110, 
                        fit=ft.ImageFit.COVER, 
                        border_radius=110
                    ),
                    # Botão para alterar foto
                    ft.Container(
                        content=ft.IconButton(
                            icon="CAMERA_ALT", 
                            icon_size=20, 
                            icon_color="white",
                            on_click=funcao_selecionar_foto, 
                            tooltip="Adicionar Foto",
                            style=ft.ButtonStyle(
                                bgcolor={"": self.cor_primaria}, 
                                shape=ft.CircleBorder()
                            )
                        ),
                        alignment=ft.alignment.bottom_right,
                    )
                ]),
                # Informações do usuário
                ft.Column([
                    ft.Text("Usuário", size=18, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text("Programador Iniciante", size=12, color="#000000"),
                    ft.ElevatedButton(
                        "Editar Perfil", 
                        icon="EDIT", 
                        height=30,
                        style=ft.ButtonStyle(
                            bgcolor={"WHITE": self.cor_secundaria}, 
                            padding=10
                        )
                    )
                ], spacing=3, expand=True)
            ], alignment=ft.MainAxisAlignment.START),
            padding=15, 
            border_radius=15, 
            margin=10
        )

    def criar_carrossel(self, funcao_proxima, funcao_anterior):
        """Cria o carrossel de imagens"""
        
        imagem_carrossel = ft.Image(
            src=self.imagens_carrossel[0],
            width=400, 
            height=200, 
            fit=ft.ImageFit.COVER, 
            border_radius=15
        )
        
        def atualizar_imagem():
            imagem_carrossel.src = self.imagens_carrossel[self.indice_carrossel]

        carrossel = ft.Container(
            content=ft.Stack([
                imagem_carrossel,
                # Botão voltar
                ft.Container(
                    content=ft.IconButton(
                        icon="ARROW_BACK_IOS_NEW", 
                        icon_color="#ededed",
                        on_click=funcao_anterior,
                        style=ft.ButtonStyle(bgcolor={"": ft.Colors.BLACK54})
                    ), 
                    alignment=ft.alignment.center_left
                ),
                # Botão avançar
                ft.Container(
                    content=ft.IconButton(
                        icon="ARROW_FORWARD_IOS", 
                        icon_color="#efefef",
                        on_click=funcao_proxima,
                        style=ft.ButtonStyle(bgcolor={"": ft.Colors.BLACK54})
                    ), 
                    alignment=ft.alignment.center_right
                ),
            ]), 
            width=400, 
            height=200, 
            margin=10, 
            border_radius=15
        )
        
        return carrossel, atualizar_imagem

    def criar_app_clima(self):
        """Cria o widget de clima"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Clima em Santana de Parnaíba/SP", 
                       size=18, 
                       weight=ft.FontWeight.BOLD, 
                       text_align=ft.TextAlign.CENTER),
                
                # Temperatura atual
                ft.Container(
                    content=ft.Row([
                        ft.Icon("SUNNY", size=40, color="#FFA500"),
                        ft.Column([
                            ft.Text("25°C", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Ensolarado", size=14),
                        ], spacing=0)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    padding=15
                ),
                
                ft.Divider(height=10, color="transparent"),
                
                # Informações do clima
                ft.Row([
                    self.item_clima("UMIDADE", "65%"),
                    ft.VerticalDivider(width=20),
                    self.item_clima("VENTO", "15 km/h"),
                    ft.VerticalDivider(width=20),
                    self.item_clima("PRESSÃO", "1015 hPa"),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                
                ft.Divider(height=15, color="transparent"),
                
                # Previsão
                ft.Container(
                    content=ft.Text(
                        "Previsão: Ensolarado (22°C a 28°C)",
                        size=12, 
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=10,
                    bgcolor="#f0f8ff",
                    border_radius=10
                )
            ]),
            padding=20,
            bgcolor="#ffffff",
            border_radius=15,
            border=ft.border.all(2, "#e0e0e0"),
            margin=ft.margin.only(bottom=10)
        )

    def item_clima(self, titulo, valor):
        """Cria um item de informação do clima"""
        return ft.Column([
            ft.Text(titulo, size=12, color="gray"),
            ft.Text(valor, size=16, weight=ft.FontWeight.BOLD),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def criar_botao_site(self):
        """Cria botão para abrir site oficial"""
        def abrir_site(e):
            import webbrowser
            webbrowser.open("https://www.parnaiba.sp.gov.br")
        
        estilo_botao = ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=20,
            bgcolor=self.cor_primaria
        )
        
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon="LANGUAGE",
                    icon_color="white",
                    icon_size=30,
                    tooltip="Site Oficial",
                    on_click=abrir_site,
                    style=estilo_botao
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=15,
            margin=ft.margin.only(top=10, bottom=20)
        )

    def criar_menu_inferior(self, funcao_clique):
        """Cria o menu inferior"""
        
        def item_menu(icone, texto, indice):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icone, size=28, color="#012643"),
                    ft.Text(texto, size=11, color="#012643", text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                padding=10, 
                border_radius=10, 
                data=indice, 
                on_click=funcao_clique,
                width=70, 
                height=65, 
                animate=200
            )
        
        return ft.Container(
            content=ft.Row([
                item_menu("HOME", "Home", 0),
                item_menu("NOTIFICATIONS", "Notificações", 1),
                item_menu("BOOK", "Materiais", 2),
                item_menu("TRENDING_UP", "Desempenho", 3),
                item_menu("PERSON", "Perfil", 4),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            bgcolor="#F5F5F5", 
            padding=10, 
            height=80
        )

    def get_view(self, pagina: ft.Page):
        """Retorna a view completa da página home"""
        
        # Configuração da página
        pagina.theme_mode = ft.ThemeMode.DARK 
        pagina.title = "FÁBRICA DE PROGRAMADORES"
        pagina.window.width = 500
        pagina.window.height = 900
        pagina.window.max_width = 500
        pagina.window.max_height = 900

        # Seletor de arquivos para foto
        seletor_arquivos = ft.FilePicker()
        pagina.overlay.append(seletor_arquivos)

        def selecionar_foto(e):
            seletor_arquivos.pick_files(allow_multiple=False)

        # Funções do carrossel
        def proxima_imagem(e):
            self.indice_carrossel = (self.indice_carrossel + 1) % len(self.imagens_carrossel)
            atualizar_carrossel()
            pagina.update()

        def imagem_anterior(e):
            self.indice_carrossel = (self.indice_carrossel - 1) % len(self.imagens_carrossel)
            atualizar_carrossel()
            pagina.update()

        # Função do menu inferior
        def item_clicado(e):
            self.indice_selecionado = e.control.data
            pagina.update()

        # Criar todos os componentes
        fundo_escuro, menu_lateral, alternar_menu = self.criar_menu_lateral(pagina)
        cabecalho = self.criar_cabecalho(alternar_menu)
        secao_perfil = self.criar_secao_perfil(selecionar_foto)
        carrossel, atualizar_carrossel = self.criar_carrossel(proxima_imagem, imagem_anterior)
        app_clima = self.criar_app_clima()
        botao_site = self.criar_botao_site()
        menu_inferior = self.criar_menu_inferior(item_clicado)

        # Conteúdo principal
        conteudo_principal = ft.Column([
            cabecalho,
            ft.Container(
                content=ft.Column([
                    secao_perfil,
                    carrossel,
                    app_clima,
                    botao_site,
                    ft.Container(height=50),  # Espaço para o menu inferior
                ], scroll=ft.ScrollMode.ADAPTIVE, expand=True),
                padding=15, 
                expand=True
            )
        ], expand=True)

        # Layout final
        layout_completo = ft.Stack([
            conteudo_principal,
            fundo_escuro,
            menu_lateral,
            ft.Container(content=menu_inferior, bottom=0, left=0, right=0)
        ], expand=True)

        # Auto-play do carrossel
        def carrossel_automatico():
            while self.carrossel_auto:
                time.sleep(3)
                if self.carrossel_auto and pagina is not None:
                    self.indice_carrossel = (self.indice_carrossel + 1) % len(self.imagens_carrossel)
                    atualizar_carrossel()
                    try:
                        pagina.update()
                    except:
                        self.carrossel_auto = False

        # Iniciar carrossel automático
        thread_carrossel = threading.Thread(target=carrossel_automatico, daemon=True)
        thread_carrossel.start()

        return ft.View(
            route="/home",
            controls=[layout_completo],
            vertical_alignment="center",
            horizontal_alignment="center",
        )
