import flet as ft
import webbrowser
import threading
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os

def LoginView(page: ft.Page):
    page.title = "Fabrica de programadores"
    page.theme_mode = "dark"
    page.window.min_height = 900
    page.window.min_width = 500
    page.window.max_height = 900
    page.window.max_width = 500
    page.window.width = 500
    page.window.height = 900

    # === SUAS CREDENCIAIS AQUI ===
    CLIENT_ID = "112683398839-pcj69aldjgo8497jaa82q0u654a64tp9.apps.googleusercontent.com"
    CLIENT_SECRET = "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"
    REDIRECT_URI = "http://localhost:8080/callback"
    # =============================

    # Variáveis de estado
    oauth_code = None
    auth_in_progress = False

    # === FUNÇÃO NOVA: SALVAR PERFIL AUTOMATICAMENTE ===
    def salvar_perfil_usuario(user_data):
        """Salva automaticamente as informações do perfil do Google"""
        try:
            perfil = {
                "nome": user_data.get('name', ''),
                "email": user_data.get('email', ''),
                "foto": user_data.get('picture', ''),
                "login_google": True,
                "data_login": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Salva em arquivo JSON
            with open('perfil_usuario.json', 'w', encoding='utf-8') as f:
                json.dump(perfil, f, ensure_ascii=False, indent=2)
            
            print("✅ Perfil salvo automaticamente com dados do Google!")
            print(f"   Nome: {perfil['nome']}")
            print(f"   Email: {perfil['email']}")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar perfil: {e}")
            return False

    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal oauth_code
            
            if self.path.startswith('/callback'):
                try:
                    parsed_url = urllib.parse.urlparse(self.path)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    
                    if 'code' in query_params:
                        oauth_code = query_params['code'][0]
                        print(f"Código OAuth recebido: {oauth_code}")
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        html_response = """
                        <html>
                            <head>
                                <title>Login Bem-sucedido</title>
                                <style>
                                    body { 
                                        font-family: Arial, sans-serif; 
                                        text-align: center; 
                                        padding: 50px; 
                                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                        color: white;
                                    }
                                    .container {
                                        background: white;
                                        padding: 40px;
                                        border-radius: 15px;
                                        color: #333;
                                        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                                        max-width: 500px;
                                        margin: 0 auto;
                                    }
                                    .success { color: #4CAF50; font-size: 24px; }
                                    .info { color: #666; margin: 20px 0; }
                                </style>
                            </head>
                            <body>
                                <div class="container">
                                    <div class="success">Login realizado com sucesso!</div>
                                    <div class="info">Voce pode fechar esta janela e voltar para o aplicativo.</div>
                                    <button onclick="window.close()" style="
                                        background: #4285f4; 
                                        color: white; 
                                        border: none; 
                                        padding: 12px 30px; 
                                        border-radius: 8px; 
                                        cursor: pointer; 
                                        font-size: 16px;
                                    ">Fechar Janela</button>
                                </div>
                                <script>
                                    setTimeout(() => {
                                        window.close();
                                    }, 3000);
                                </script>
                            </body>
                        </html>
                        """
                        self.wfile.write(html_response.encode())
                        
                except Exception as e:
                    print(f"Erro no callback: {e}")
                    
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass

    def start_oauth_server():
        try:
            server = HTTPServer(('localhost', 8080), OAuthHandler)
            print("Servidor OAuth iniciado na porta 8080")
            server.timeout = 60
            server.handle_request()
        except Exception as e:
            print(f"Erro no servidor: {e}")

    def exchange_code_for_token(code):
        try:
            token_url = "https://oauth2.googleapis.com/token"
            
            data = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(token_url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                
                if access_token:
                    return get_user_info(access_token)
                else:
                    return None, "Token de acesso não recebido"
            else:
                error_msg = f"Erro {response.status_code}: {response.text}"
                return None, error_msg
                
        except Exception as e:
            return None, f"Erro na comunicação: {str(e)}"

    def get_user_info(access_token):
        try:
            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.get(userinfo_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                user_data = response.json()
                return user_data, None
            else:
                return None, f"Erro ao obter dados do usuário: {response.status_code}"
                
        except Exception as e:
            return None, f"Erro ao buscar informações: {str(e)}"

    def monitor_oauth():
        nonlocal oauth_code, auth_in_progress
        
        max_wait = 60
        start_time = time.time()
        
        while auth_in_progress and (time.time() - start_time) < max_wait:
            if oauth_code:
                print(f"Processando código OAuth: {oauth_code}")
                user_data, error = exchange_code_for_token(oauth_code)
                
                if user_data and not error:
                    # === AQUI: SALVA O PERFIL AUTOMATICAMENTE ===
                    salvar_perfil_usuario(user_data)
                    
                    page.session.set("user_email", user_data.get('email', ''))
                    page.session.set("user_name", user_data.get('name', ''))
                    page.session.set("user_picture", user_data.get('picture', ''))
                    
                    page.run_thread(lambda: login_success(user_data))
                    break
                else:
                    page.run_thread(lambda: login_error(error or "Erro desconhecido"))
                    break
            
            time.sleep(1)
        
        if not oauth_code and auth_in_progress:
            page.run_thread(lambda: login_error("Tempo esgotado. Tente novamente."))
        
        auth_in_progress = False

    def login_success(user_data):
        nonlocal auth_in_progress
        
        auth_in_progress = False
        user_name = user_data.get('name', 'Usuário')
        user_email = user_data.get('email', '')
        
        mensagem.value = f"✅ Bem-vindo, {user_name}!"
        mensagem.color = ft.Colors.GREEN
        botao_google.disabled = False
        page.update()
        
        time.sleep(2)
        page.go("/home")

    def login_error(error_msg):
        nonlocal auth_in_progress
        
        auth_in_progress = False
        mensagem.value = f"❌ {error_msg}"
        mensagem.color = ft.Colors.RED
        botao_google.disabled = False
        page.update()

    def login_google(e):
        nonlocal auth_in_progress, oauth_code
        
        if auth_in_progress:
            return
        
        auth_in_progress = True
        oauth_code = None
        botao_google.disabled = True
        
        params = {
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        
        mensagem.value = "🔗 Redirecionando para Google..."
        mensagem.color = ft.Colors.BLUE
        page.update()
        
        threading.Thread(target=start_oauth_server, daemon=True).start()
        threading.Thread(target=monitor_oauth, daemon=True).start()
        
        webbrowser.open(auth_url)

    # Botões da interface (mantenha igual)
    botao_personalizado = ft.ElevatedButton(
        "Entrar", width=150, on_click=lambda _: page.go("/home"),
        style=ft.ButtonStyle(
            color={ft.ControlState.HOVERED: ft.Colors.WHITE, ft.ControlState.DEFAULT: ft.Colors.WHITE},
            bgcolor={ft.ControlState.FOCUSED: ft.Colors.PINK_200, "": ft.Colors.GREEN},
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
        "Cadastrar", bgcolor=None, on_click=lambda _: page.go("/cadastro")
    )
    
    botao_google = ft.Container(
        content=ft.Row([
            ft.Image(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png",
                width=20,
                height=20,
            ),
            ft.Text("Entrar com Google", color=ft.Colors.BLACK, size=14),
        ], alignment="center", spacing=10),
        width=300,
        height=40,
        border_radius=4,
        bgcolor=ft.Colors.WHITE,
        alignment=ft.alignment.center,
        on_click=login_google,
    )
        
    titulo = ft.Text("Login", size=30)
    criar = ft.Text("Não tem um conta?", size=15)
    entrada_email = ft.TextField(label="E-mail", width=300, border_color="WHITE")
    entrada_senha = ft.TextField(label="Senha", password=True, width=300, border_color="WHITE")
    mensagem = ft.Text(size=16)
    
    divisor_ou = ft.Row([
        ft.Container(ft.Divider(height=1, color=ft.Colors.GREY_600), expand=True),
        ft.Text(" ou ", color=ft.Colors.GREY_400, size=12),
        ft.Container(ft.Divider(height=1, color=ft.Colors.GREY_600), expand=True),
    ], alignment="center", vertical_alignment="center")
    
    return ft.View(
        route="/",
        controls=[
            ft.Row([titulo], alignment="center"),
            ft.Row([entrada_email], alignment="center"),
            ft.Row([entrada_senha], alignment="center"),
            ft.Row([botao_personalizado], alignment="center"),
            ft.Row([divisor_ou], alignment="center"),
            ft.Row([botao_google], alignment="center"),
            ft.Row([criar, botao_cadastro], alignment="center"),
            ft.Row([mensagem], alignment="center")
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )


# === FUNÇÃO PARA CARREGAR PERFIL (use na HomeView) ===
def carregar_perfil_salvo():
    """Carrega o perfil salvo automaticamente"""
    try:
        if os.path.exists('perfil_usuario.json'):
            with open('perfil_usuario.json', 'r', encoding='utf-8') as f:
                perfil = json.load(f)
                print("📁 Perfil carregado:", perfil['email'])
                return perfil
    except Exception as e:
        print("❌ Erro ao carregar perfil:", e)
    return None

# === EXEMPLO de HomeView que usa o perfil salvo ===
def HomeView(page: ft.Page):
    # Carrega o perfil salvo automaticamente
    perfil = carregar_perfil_salvo()
    
    if perfil:
        # Perfil já configurado com dados do Google
        conteudo = [
            ft.Text("Meu Perfil", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"👤 Nome: {perfil['nome']}", size=18),
            ft.Text(f"📧 Email: {perfil['email']}", size=16),
            ft.Text("🔐 Login com Google", size=14, color=ft.Colors.GREEN),
            ft.Text(f"📅 Desde: {perfil['data_login']}", size=12, color=ft.Colors.GREY),
        ]
        
        # Adiciona foto se existir
        if perfil.get('foto'):
            conteudo.insert(2, ft.Image(
                src=perfil['foto'],
                width=80,
                height=80,
                fit=ft.ImageFit.COVER,
                border_radius=40
            ))
    else:
        # Perfil não configurado
        conteudo = [
            ft.Text("Perfil não configurado", size=20),
            ft.Text("Faça login com Google para configurar automaticamente", 
                   size=14, color=ft.Colors.BLUE),
        ]
    
    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(title=ft.Text("Home")),
            ft.Container(
                content=ft.Column(conteudo, spacing=15),
                padding=40,
                alignment=ft.alignment.center
            )
        ]
    )
