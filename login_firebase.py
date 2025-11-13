"""
Tela de Login com Firebase Authentication e Google Sign-In
Versão melhorada com suporte a mobile e desktop

Autor: Fábrica de Programadores
Data: 2025-01-13
"""

import flet as ft
import webbrowser
import threading
import time
from firebase_auth import FirebaseAuth, OAuthServer


def LoginView(page: ft.Page):
    """
    Tela de login com autenticação Firebase e Google Sign-In
    Suporta tanto desktop quanto mobile
    """
    page.title = "Fabrica de programadores"
    page.theme_mode = "dark"
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900

    # Inicializa Firebase Auth
    firebase_auth = FirebaseAuth()
    oauth_server = None

    # Estado da autenticação
    auth_state = {
        'in_progress': False,
        'error': None
    }

    # === VERIFICAÇÃO DE LOGIN AUTOMÁTICO ===
    def check_auto_login():
        """Verifica se usuário já está logado e redireciona automaticamente"""
        if firebase_auth.is_logged_in():
            perfil = firebase_auth.load_user_profile()
            print(f"✅ Login automático: {perfil.get('email')}")
            
            # Armazena dados na sessão
            page.session.set("user_email", perfil.get('email'))
            page.session.set("user_name", perfil.get('nome'))
            page.session.set("user_picture", perfil.get('foto'))
            
            mensagem.value = f"✅ Bem-vindo de volta, {perfil.get('nome')}!"
            mensagem.color = ft.Colors.GREEN
            page.update()
            
            time.sleep(1.5)
            page.go("/home")
            return True
        return False

    # === FUNÇÃO DE LOGIN COM GOOGLE ===
    def login_google(e):
        """Inicia fluxo de autenticação com Google"""
        nonlocal oauth_server
        
        if auth_state['in_progress']:
            print("⚠️ Autenticação já em andamento")
            return
        
        auth_state['in_progress'] = True
        auth_state['error'] = None
        
        botao_google.disabled = True
        mensagem.value = "🔗 Abrindo Google Sign-In..."
        mensagem.color = ft.Colors.BLUE
        page.update()

        try:
            # Inicia servidor OAuth para desktop
            if not firebase_auth.is_mobile():
                oauth_server = OAuthServer(port=8000)
                oauth_server.start()
                time.sleep(0.5)  # Aguarda servidor iniciar
            
            # Gera URL de autenticação
            auth_url = firebase_auth.get_google_auth_url()
            print(f"🔗 URL de autenticação: {auth_url[:80]}...")
            
            # Abre navegador
            mensagem.value = "🌐 Navegador aberto. Faça login no Google..."
            mensagem.color = ft.Colors.BLUE
            page.update()
            
            # Abre URL no navegador (funciona tanto desktop quanto mobile)
            try:
                webbrowser.open(auth_url)
            except:
                # Fallback para Flet's launch_url
                page.launch_url(auth_url)
            
            # Monitora resposta
            threading.Thread(
                target=monitor_oauth_callback,
                daemon=True
            ).start()
            
        except Exception as ex:
            handle_auth_error(f"Erro ao iniciar autenticação: {ex}")

    # === MONITORAMENTO DO CALLBACK OAUTH ===
    def monitor_oauth_callback():
        """Monitora callback OAuth e processa autenticação"""
        max_wait = 120  # 2 minutos timeout
        start_time = time.time()
        check_interval = 1  # Verifica a cada 1 segundo
        
        print("⏳ Aguardando callback OAuth...")
        
        while auth_state['in_progress'] and (time.time() - start_time) < max_wait:
            # Desktop: verifica servidor local
            if oauth_server:
                code = oauth_server.get_code()
                if code:
                    print(f"✅ Código OAuth recebido do servidor")
                    process_oauth_code(code)
                    return
            
            # Mobile: verifica deep link (implementar quando necessário)
            # TODO: Implementar detecção de deep link para mobile
            
            time.sleep(check_interval)
        
        # Timeout
        if auth_state['in_progress']:
            handle_auth_error("Tempo esgotado. Tente novamente.")

    # === PROCESSAMENTO DO CÓDIGO OAUTH ===
    def process_oauth_code(code: str):
        """Processa código OAuth e obtém informações do usuário"""
        try:
            print("🔄 Processando código OAuth...")
            
            # Atualiza UI
            page.run_thread(lambda: update_message(
                "🔄 Autenticando com Google...",
                ft.Colors.BLUE
            ))
            
            # Troca código por token e obtém dados do usuário
            user_data, error = firebase_auth.exchange_code_for_token(code)
            
            if user_data and not error:
                # Salva perfil localmente
                firebase_auth.save_user_profile(user_data)
                
                # Armazena na sessão
                page.session.set("user_email", user_data.get('email'))
                page.session.set("user_name", user_data.get('name'))
                page.session.set("user_picture", user_data.get('picture'))
                
                # Sucesso!
                page.run_thread(lambda: handle_auth_success(user_data))
            else:
                page.run_thread(lambda: handle_auth_error(error or "Erro desconhecido"))
                
        except Exception as ex:
            page.run_thread(lambda: handle_auth_error(f"Erro ao processar: {ex}"))
        
        finally:
            # Fecha servidor OAuth
            if oauth_server:
                oauth_server.stop()

    # === HANDLERS DE SUCESSO E ERRO ===
    def handle_auth_success(user_data):
        """Trata sucesso na autenticação"""
        auth_state['in_progress'] = False
        
        user_name = user_data.get('name', 'Usuário')
        user_email = user_data.get('email', '')
        
        print(f"✅ Autenticação bem-sucedida: {user_email}")
        
        mensagem.value = f"✅ Bem-vindo, {user_name}!"
        mensagem.color = ft.Colors.GREEN
        botao_google.disabled = False
        page.update()
        
        # Aguarda 2 segundos e redireciona
        time.sleep(2)
        page.go("/home")

    def handle_auth_error(error_msg: str):
        """Trata erro na autenticação"""
        auth_state['in_progress'] = False
        auth_state['error'] = error_msg
        
        print(f"❌ Erro na autenticação: {error_msg}")
        
        mensagem.value = f"❌ {error_msg}"
        mensagem.color = ft.Colors.RED
        botao_google.disabled = False
        page.update()

    def update_message(text: str, color):
        """Atualiza mensagem na UI (thread-safe)"""
        mensagem.value = text
        mensagem.color = color
        page.update()

    # === COMPONENTES DA UI ===
    
    titulo = ft.Text("Login", size=30, weight=ft.FontWeight.BOLD)
    
    criar = ft.Text("Não tem uma conta?", size=15)
    
    entrada_email = ft.TextField(
        label="E-mail",
        width=300,
        border_color="WHITE",
        prefix_icon=ft.Icons.EMAIL
    )
    
    entrada_senha = ft.TextField(
        label="Senha",
        password=True,
        width=300,
        border_color="WHITE",
        prefix_icon=ft.Icons.LOCK,
        can_reveal_password=True
    )
    
    mensagem = ft.Text(size=16, text_align=ft.TextAlign.CENTER)
    
    # Botão de login tradicional (pode ser usado para login email/senha se implementar)
    botao_personalizado = ft.ElevatedButton(
        "Entrar",
        width=150,
        on_click=lambda _: page.go("/home"),  # Placeholder
        style=ft.ButtonStyle(
            color={
                ft.ControlState.HOVERED: ft.Colors.WHITE,
                ft.ControlState.DEFAULT: ft.Colors.WHITE
            },
            bgcolor={
                ft.ControlState.FOCUSED: ft.Colors.PINK_200,
                "": ft.Colors.GREEN
            },
            padding={ft.ControlState.HOVERED: 20},
            overlay_color=ft.Colors.TRANSPARENT,
            elevation={"pressed": 0, "": 1},
            animation_duration=500,
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.GREEN),
                ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.GREEN),
            },
            shape={
                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
            },
        ),
    )
    
    botao_cadastro = ft.ElevatedButton(
        "Cadastrar",
        bgcolor=None,
        on_click=lambda _: page.go("/cadastro")
    )
    
    # Botão Google Sign-In (design oficial do Google)
    botao_google = ft.Container(
        content=ft.Row([
            ft.Image(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png",
                width=20,
                height=20,
            ),
            ft.Text("Entrar com Google", color=ft.Colors.BLACK, size=14, weight=ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=300,
        height=40,
        border_radius=4,
        bgcolor=ft.Colors.WHITE,
        alignment=ft.alignment.center,
        on_click=login_google,
        ink=True,
        tooltip="Fazer login com sua conta Google",
    )
    
    # Animação de hover para botão Google
    def on_google_hover(e):
        if e.data == "true":
            botao_google.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        else:
            botao_google.shadow = None
        page.update()
    
    botao_google.on_hover = on_google_hover
    
    # Divisor "ou"
    divisor_ou = ft.Row([
        ft.Container(ft.Divider(height=1, color=ft.Colors.GREY_600), expand=True),
        ft.Text(" ou ", color=ft.Colors.GREY_400, size=12),
        ft.Container(ft.Divider(height=1, color=ft.Colors.GREY_600), expand=True),
    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    
    # Informação sobre Firebase
    info_firebase = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.SECURITY, size=16, color=ft.Colors.GREEN),
                ft.Text("Autenticação segura com Firebase", size=12, color=ft.Colors.GREY_400),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        ]),
        margin=ft.margin.only(top=20)
    )
    
    # === VIEW PRINCIPAL ===
    view = ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Container(height=50),
                    ft.Row([titulo], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=30),
                    ft.Row([entrada_email], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                    ft.Row([entrada_senha], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=20),
                    ft.Row([botao_personalizado], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=20),
                    ft.Row([divisor_ou], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=20),
                    ft.Row([botao_google], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=20),
                    ft.Row([criar, botao_cadastro], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                    ft.Row([mensagem], alignment=ft.MainAxisAlignment.CENTER),
                    info_firebase,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Verifica login automático ao carregar a view
    check_auto_login()
    
    return view


# === EXEMPLO DE USO ===
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Firebase Auth Test"
        page.add(LoginView(page))
    
    ft.app(target=main)
