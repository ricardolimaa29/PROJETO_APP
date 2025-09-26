import flet as ft
import time
import threading

class HomeView:
    def __init__(self):
        self.primary_color = "#1E5FE9"
        self.secondary_color = "#2AC9A6"
        self.carousel_images = [
            "img\\fabrica.jpg",
            "img\\premio.jpg",
            "img\\programa.jpg",
            "img\\santana.jpg"
        ]
        self.carousel_index = 0
        self.selected_index = 0
        self.auto_play_enabled = True
        self.drawer_open = False

    def create_drawer(self, page):
        
        """ANIMAÇÃO DO MENU LATERAL DO APLICATIVO"""
        
        def toggle_drawer(e):
            self.drawer_open = not self.drawer_open
            drawer.width = 280 if self.drawer_open else 0
            overlay.opacity = 0.4 if self.drawer_open else 0
            overlay.visible = self.drawer_open
            page.update()

        def menu_clicked(e):
            item_text = e.control.content.controls[1].value
            print(f"Item {item_text} clicado!")
            toggle_drawer(e)

        # Overlay
        overlay = ft.Container(
            expand=True, bgcolor="black", opacity=0, visible=False,
            on_click=toggle_drawer, animate_opacity=300
        )

        # mensagem dos button do menu lateral 
        drawer = ft.Container(
            width=0, height=page.height, bgcolor="white",
            content=ft.Column([
                # Header do drawer
                ft.Container(
                    content=ft.Row([
                        ft.Text("MENU", size=20, weight="bold", color="white" ),
                    ], alignment="center"),
                    bgcolor=self.primary_color, padding=15, height=70,border_radius=3, margin=1
                ),
                         #  """ICONES E TEXTOS DA ABA DO MENU LATERAL """
                
                ft.Container(
                    content=ft.Column([
                        self.create_menu_item("HOME", "INÍCIO", menu_clicked),
                        ft.Divider(height=1),
                        self.create_menu_item("SUPPORT", "SUPORTE", menu_clicked),
                        ft.Divider(height=1),
                        ft.Container(expand=True),  # Espaço flexível
                        self.create_menu_item("EXIT_TO_APP", "SAIR", menu_clicked, is_exit=True),
                    ], spacing=0),
                    padding=10, expand=True
                )
            ], spacing=0),
            animate=300, right=0, top=0,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK54)
        )

        return overlay, drawer, toggle_drawer

    def create_menu_item(self, icon, text, on_click, is_exit=False):
        """Cria um item do menu"""
        color = "#ef4444" if is_exit else self.primary_color
        bg_color = "#fee2e2" if is_exit else "#e0e7ff"
        
        """return dos itens do meenu lateral"""
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=color, size=20),
                    bgcolor=bg_color, padding=10, border_radius=10, width=40, height=40
                ),
                ft.Text(text, weight="bold", color=color, size=16)
            ], spacing=15),
            padding=15, on_click=on_click, border_radius=10,
            bgcolor={"": "transparent", "hovered": "#f1f5f9"}
        )

    def create_header(self, toggle_drawer):
        
        """modificar o cabeçalho do aplicativo"""
        
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon="MENU", icon_color="#FFFFFF", icon_size=30,
                    on_click=toggle_drawer, tooltip="Abrir Menu"
                ),
                ft.Text("FÁBRICA DE PROGRAMADORES", size=22, weight="bold", 
                       color="#ffffff", text_align=ft.TextAlign.CENTER, expand=True),
            ], alignment=ft.MainAxisAlignment.START),
            bgcolor=self.primary_color, padding=20, height=70, border_radius=10, margin=1
        )

    def create_profile_section(self, pick_file):
        
        """mudar a seção de perfil do aplicativo"""
        
        return ft.Container(
            content=ft.Row([
                ft.Stack([
                    ft.Image(
                        src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200",
                        width=110, height=110, fit=ft.ImageFit.COVER, border_radius=110
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            icon="CAMERA_ALT", icon_size=20, icon_color="white",
                            on_click=pick_file, tooltip="Adicionar Foto",
                            style=ft.ButtonStyle(bgcolor={"": self.primary_color}, shape=ft.CircleBorder())
                        ),
                        alignment=ft.alignment.bottom_right,
                    )
                ]),
                ft.Column([
                    ft.Text("Usuário", size=18, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text("Programador Iniciante", size=12, color="#000000"),
                    ft.ElevatedButton(
                        "Editar Perfil", icon="EDIT", height=30,
                        style=ft.ButtonStyle(bgcolor={"WHITE": self.secondary_color}, padding=10)
                    )
                ], spacing=3, expand=True)
            ], alignment=ft.MainAxisAlignment.START),
             padding=15, border_radius=15, margin=10
        )

    def create_carousel(self, next_image, previous_image):
        
        """carrosel de imagens do aplicativo"""
        
        carousel_image = ft.Image(
            src=self.carousel_images[0],
            width=400, height=200, fit=ft.ImageFit.COVER, border_radius=15
        )
        """""container do carrosel e função de atualizar o carrosel"""
        def update_carousel():
            carousel_image.src = self.carousel_images[self.carousel_index]

        carousel = ft.Container(
            content=ft.Stack([
                carousel_image,
                ft.Container(
                    content=ft.IconButton(
                        icon="ARROW_BACK_IOS_NEW", icon_color="#ededed",
                        on_click=previous_image,
                        style=ft.ButtonStyle(bgcolor={"": ft.Colors.BLACK54})
                    ), alignment=ft.alignment.center_left
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon="ARROW_FORWARD_IOS", icon_color="#efefef",
                        on_click=next_image,
                        style=ft.ButtonStyle(bgcolor={"": ft.Colors.BLACK54})
                    ), alignment=ft.alignment.center_right
                ),
            ]), width=400, height=200, margin=10, border_radius=15
        )
        
        """"return o carrosel e a função de atualizar o carrosel"""
        
        return carousel, update_carousel

    def create_weather_app(self):
        """Cria o aplicativo de clima para Santana de Parnaíba/SP"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Clima em Santana de Parnaíba/SP", 
                       size=18, weight=ft.FontWeight.BOLD, 
                       text_align=ft.TextAlign.CENTER),
                
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
                
                ft.Row([
                    ft.Column([
                        ft.Text("UMIDADE", size=12, color="gray"),
                        ft.Text("65%", size=16, weight=ft.FontWeight.BOLD),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    
                    ft.VerticalDivider(width=20),
                    
                    ft.Column([
                        ft.Text("VENTO", size=12, color="gray"),
                        ft.Text("15 km/h", size=16, weight=ft.FontWeight.BOLD),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    
                    ft.VerticalDivider(width=20),
                    
                    ft.Column([
                        ft.Text("PRESSÃO", size=12, color="gray"),
                        ft.Text("1015 hPa", size=16, weight=ft.FontWeight.BOLD),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                
                ft.Divider(height=15, color="transparent"),
                
                ft.Container(
                    content=ft.Text("Previsão para os próximos dias: Ensolarado com temperaturas entre 22°C e 28°C.",
                                   size=12, text_align=ft.TextAlign.CENTER),
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

    def create_circular_button(self):
        """Cria apenas um botão circular centralizado"""
        def open_url(e):
            import webbrowser
            webbrowser.open("https://www.parnaiba.sp.gov.br")
        
        button_style = ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=20,
            bgcolor=self.primary_color
        )
        
        return ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon="LANGUAGE",
                    icon_color="white",
                    icon_size=30,
                    tooltip="Site Oficial",
                    on_click=open_url,
                    style=button_style
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=15,
            margin=ft.margin.only(top=10, bottom=20)
        )

    def create_bottom_menu(self, menu_item_clicked):
        
        """aplicação do menu inferior"""
        
        def create_menu_item(icon, label, index):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icon, size=28, color="#012643"),
                    ft.Text(label, size=11, color="#012643", text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                padding=10, border_radius=10, data=index, on_click=menu_item_clicked,
                width=70, height=65, animate=200
            )
        
        """"retorun o menu inferior (icones e textos)"""
        
        return ft.Container(
            content=ft.Row([
                create_menu_item("HOME", "Home", 0),
                create_menu_item("NOTIFICATIONS", "Notificações", 1),
                create_menu_item("BOOK", "Materiais", 2),
                create_menu_item("TRENDING_UP", "Desempenho", 3),
                create_menu_item("PERSON", "Perfil", 4),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            bgcolor="#F5F5F5", padding=10, height=80
        )

    def get_view(self, page: ft.Page):
        """Retorna a view da página home"""
        
        # Configuração da página
        page.bgcolor = "#ffffff"
        page.title = "FÁBRICA DE PROGRAMADORES"
        page.window.width = 500
        page.window.height = 900
        page.window.max_width = 500
        page.window.max_height = 900

        """"File Picker(button de adicionar foto de perfil)"""
        
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)

        def pick_file(e):
            file_picker.pick_files(allow_multiple=False)

        # Carrossel functions
        def next_image(e):
            self.carousel_index = (self.carousel_index + 1) % len(self.carousel_images)
            update_carousel()
            page.update()

        def previous_image(e):
            self.carousel_index = (self.carousel_index - 1) % len(self.carousel_images)
            update_carousel()
            page.update()

        # Menu função 
        def menu_item_clicked(e):
            self.selected_index = e.control.data
            page.update()

        """"todos os componentes da página para rodar o layout do aplicativo"""
        
        overlay, drawer, toggle_drawer = self.create_drawer(page)
        header = self.create_header(toggle_drawer)
        profile_section = self.create_profile_section(pick_file)
        carousel, update_carousel = self.create_carousel(next_image, previous_image)
        weather_app = self.create_weather_app()
        circular_button = self.create_circular_button()
        bottom_menu = self.create_bottom_menu(menu_item_clicked)

        """Conteúdo principal da página"""
        
        content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    profile_section,
                    carousel,
                    weather_app,
                    circular_button,
                    ft.Container(height=50),
                ], scroll=ft.ScrollMode.ADAPTIVE, expand=True),
                padding=15, expand=True
            )
        ], expand=True)

        # Layout final
        main_content = ft.Stack([
            content,
            overlay,
            drawer,
            ft.Container(content=bottom_menu, bottom=0, left=0, right=0)
        ], expand=True)

        """função de rodar o carrosel automaticamente"""
        
        def auto_play():
            while self.auto_play_enabled:
                time.sleep(3)
                if self.auto_play_enabled and page is not None:
                    self.carousel_index = (self.carousel_index + 1) % len(self.carousel_images)
                    update_carousel()
                    try:
                        page.update()
                    except:
                        self.auto_play_enabled = False

        # Iniciar a thread do carrossel
        auto_play_thread = threading.Thread(target=auto_play, daemon=True)
        auto_play_thread.start()

        # Retorna a View corretamente
        return ft.View(
            route="/home",
            controls=[main_content],
            vertical_alignment="center",
            horizontal_alignment="center",
        )
