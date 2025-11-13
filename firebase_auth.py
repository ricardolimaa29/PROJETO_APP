"""
Módulo de Autenticação Firebase para Flet Mobile App
Autor: Fábrica de Programadores
Data: 2025-01-13

Este módulo gerencia a autenticação com Firebase e Google Sign-In,
suportando tanto desktop quanto mobile.
"""

import os
import json
import time
import requests
import webbrowser
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


class FirebaseAuthConfig:
    """Configuração do Firebase Authentication"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Carrega configurações do Firebase de .env ou firebase_config.json"""
        # Tenta carregar do .env primeiro
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            self.api_key = os.getenv('FIREBASE_API_KEY')
            self.auth_domain = os.getenv('FIREBASE_AUTH_DOMAIN')
            self.project_id = os.getenv('FIREBASE_PROJECT_ID')
            self.client_id = os.getenv('GOOGLE_CLIENT_ID_WEB')
            self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
            
            if self.api_key:
                print("✅ Configuração carregada de .env")
                return
        except ImportError:
            print("⚠️ python-dotenv não instalado, tentando firebase_config.json")
        except Exception as e:
            print(f"⚠️ Erro ao carregar .env: {e}")
        
        # Fallback para firebase_config.json
        try:
            config_path = Path(__file__).parent / 'firebase_config.json'
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                self.api_key = config.get('apiKey')
                self.auth_domain = config.get('authDomain')
                self.project_id = config.get('projectId')
                self.client_id = config.get('clientId')
                self.client_secret = config.get('clientSecret')
                print("✅ Configuração carregada de firebase_config.json")
                return
        except Exception as e:
            print(f"⚠️ Erro ao carregar firebase_config.json: {e}")
        
        # Fallback para credenciais hardcoded (apenas desenvolvimento)
        print("⚠️ Usando credenciais padrão (atualize com suas credenciais!)")
        self.api_key = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.auth_domain = "seu-projeto.firebaseapp.com"
        self.project_id = "seu-projeto"
        self.client_id = "112683398839-pcj69aldjgo8497jaa82q0u654a64tp9.apps.googleusercontent.com"
        self.client_secret = "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"


class FirebaseAuth:
    """Gerenciador de autenticação Firebase"""
    
    def __init__(self, config: Optional[FirebaseAuthConfig] = None):
        self.config = config or FirebaseAuthConfig()
        self.oauth_code = None
        self.auth_in_progress = False
        self.redirect_uri = "http://localhost:8000/callback"
        self.mobile_redirect_uri = "fabricaapp://auth/callback"
        
    def is_mobile(self) -> bool:
        """Detecta se está rodando em mobile"""
        # TODO: Implementar detecção real de plataforma mobile
        # Por enquanto, assume desktop
        return False
    
    def get_redirect_uri(self) -> str:
        """Retorna redirect URI apropriado para plataforma"""
        return self.mobile_redirect_uri if self.is_mobile() else self.redirect_uri
    
    def get_google_auth_url(self) -> str:
        """Gera URL de autenticação do Google"""
        params = {
            'client_id': self.config.client_id,
            'redirect_uri': self.get_redirect_uri(),
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Troca código OAuth por token de acesso
        
        Args:
            code: Código OAuth recebido do Google
            
        Returns:
            Tuple (user_data, error_message)
        """
        try:
            token_url = "https://oauth2.googleapis.com/token"
            
            data = {
                'client_id': self.config.client_id,
                'client_secret': self.config.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_redirect_uri()
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            print(f"🔄 Trocando código por token...")
            response = requests.post(token_url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                
                if access_token:
                    print("✅ Token recebido com sucesso")
                    return self.get_user_info(access_token)
                else:
                    return None, "Token de acesso não recebido"
            else:
                error_msg = f"Erro {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return None, error_msg
                
        except Exception as e:
            error_msg = f"Erro na comunicação: {str(e)}"
            print(f"❌ {error_msg}")
            return None, error_msg
    
    def get_user_info(self, access_token: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Obtém informações do usuário usando access token
        
        Args:
            access_token: Token de acesso do Google
            
        Returns:
            Tuple (user_data, error_message)
        """
        try:
            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            print("🔄 Buscando informações do usuário...")
            response = requests.get(userinfo_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Usuário autenticado: {user_data.get('email')}")
                return user_data, None
            else:
                error_msg = f"Erro ao obter dados do usuário: {response.status_code}"
                print(f"❌ {error_msg}")
                return None, error_msg
                
        except Exception as e:
            error_msg = f"Erro ao buscar informações: {str(e)}"
            print(f"❌ {error_msg}")
            return None, error_msg
    
    def save_user_profile(self, user_data: Dict[str, Any]) -> bool:
        """
        Salva perfil do usuário localmente
        
        Args:
            user_data: Dados do usuário do Google
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            perfil = {
                "nome": user_data.get('name', ''),
                "email": user_data.get('email', ''),
                "foto": user_data.get('picture', ''),
                "login_google": True,
                "google_id": user_data.get('id', ''),
                "verified_email": user_data.get('verified_email', False),
                "data_login": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ultimo_acesso": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Salva em arquivo JSON
            perfil_path = Path(__file__).parent / 'perfil_usuario.json'
            with open(perfil_path, 'w', encoding='utf-8') as f:
                json.dump(perfil, f, ensure_ascii=False, indent=2)
            
            print("✅ Perfil salvo automaticamente!")
            print(f"   📧 Email: {perfil['email']}")
            print(f"   👤 Nome: {perfil['nome']}")
            print(f"   📁 Arquivo: {perfil_path}")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar perfil: {e}")
            return False
    
    def load_user_profile(self) -> Optional[Dict[str, Any]]:
        """
        Carrega perfil do usuário salvo localmente
        
        Returns:
            Dict com dados do perfil ou None se não existir
        """
        try:
            perfil_path = Path(__file__).parent / 'perfil_usuario.json'
            if perfil_path.exists():
                with open(perfil_path, 'r', encoding='utf-8') as f:
                    perfil = json.load(f)
                print(f"📁 Perfil carregado: {perfil.get('email')}")
                return perfil
        except Exception as e:
            print(f"❌ Erro ao carregar perfil: {e}")
        return None
    
    def is_logged_in(self) -> bool:
        """Verifica se existe usuário logado"""
        perfil = self.load_user_profile()
        return perfil is not None and 'email' in perfil


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handler para capturar callback OAuth"""
    
    oauth_code = None
    
    def do_GET(self):
        if self.path.startswith('/callback'):
            try:
                parsed_url = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                if 'code' in query_params:
                    OAuthCallbackHandler.oauth_code = query_params['code'][0]
                    print(f"✅ Código OAuth recebido: {OAuthCallbackHandler.oauth_code[:20]}...")
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    html_response = """
                    <!DOCTYPE html>
                    <html lang="pt-BR">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Login Bem-sucedido - Fábrica de Programadores</title>
                            <style>
                                * {
                                    margin: 0;
                                    padding: 0;
                                    box-sizing: border-box;
                                }
                                body { 
                                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    min-height: 100vh;
                                    padding: 20px;
                                }
                                .container {
                                    background: white;
                                    padding: 50px 40px;
                                    border-radius: 20px;
                                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                                    max-width: 500px;
                                    width: 100%;
                                    text-align: center;
                                    animation: slideIn 0.5s ease-out;
                                }
                                @keyframes slideIn {
                                    from {
                                        opacity: 0;
                                        transform: translateY(-20px);
                                    }
                                    to {
                                        opacity: 1;
                                        transform: translateY(0);
                                    }
                                }
                                .success-icon {
                                    width: 80px;
                                    height: 80px;
                                    margin: 0 auto 30px;
                                    border-radius: 50%;
                                    background: linear-gradient(135deg, #4CAF50, #45a049);
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    animation: scaleIn 0.5s ease-out 0.2s both;
                                }
                                @keyframes scaleIn {
                                    from {
                                        transform: scale(0);
                                    }
                                    to {
                                        transform: scale(1);
                                    }
                                }
                                .success-icon svg {
                                    width: 50px;
                                    height: 50px;
                                    stroke: white;
                                    stroke-width: 3;
                                    fill: none;
                                    stroke-linecap: round;
                                    stroke-linejoin: round;
                                }
                                .success-icon svg path {
                                    stroke-dasharray: 100;
                                    stroke-dashoffset: 100;
                                    animation: drawCheck 0.5s ease-out 0.7s forwards;
                                }
                                @keyframes drawCheck {
                                    to {
                                        stroke-dashoffset: 0;
                                    }
                                }
                                h1 {
                                    color: #4CAF50;
                                    font-size: 32px;
                                    margin-bottom: 15px;
                                    font-weight: 600;
                                }
                                .subtitle {
                                    color: #666;
                                    font-size: 18px;
                                    margin-bottom: 30px;
                                    line-height: 1.5;
                                }
                                .info {
                                    background: #f5f5f5;
                                    padding: 20px;
                                    border-radius: 10px;
                                    margin-bottom: 30px;
                                }
                                .info p {
                                    color: #555;
                                    font-size: 15px;
                                    margin: 10px 0;
                                }
                                .countdown {
                                    font-size: 14px;
                                    color: #999;
                                    margin-bottom: 20px;
                                }
                                .countdown span {
                                    font-weight: bold;
                                    color: #667eea;
                                }
                                button {
                                    background: linear-gradient(135deg, #667eea, #764ba2);
                                    color: white;
                                    border: none;
                                    padding: 15px 40px;
                                    border-radius: 10px;
                                    cursor: pointer;
                                    font-size: 16px;
                                    font-weight: 600;
                                    transition: all 0.3s ease;
                                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                                }
                                button:hover {
                                    transform: translateY(-2px);
                                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                                }
                                button:active {
                                    transform: translateY(0);
                                }
                                .footer {
                                    margin-top: 30px;
                                    padding-top: 20px;
                                    border-top: 1px solid #eee;
                                    color: #999;
                                    font-size: 13px;
                                }
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="success-icon">
                                    <svg viewBox="0 0 50 50">
                                        <path d="M 10 25 L 20 35 L 40 15"/>
                                    </svg>
                                </div>
                                <h1>🎉 Login Realizado com Sucesso!</h1>
                                <p class="subtitle">Bem-vindo à Fábrica de Programadores</p>
                                
                                <div class="info">
                                    <p><strong>✅ Autenticação Concluída</strong></p>
                                    <p>Você está sendo redirecionado para o aplicativo...</p>
                                </div>
                                
                                <div class="countdown">
                                    Esta janela fechará automaticamente em <span id="timer">3</span> segundos
                                </div>
                                
                                <button onclick="window.close()">
                                    ✕ Fechar Janela Agora
                                </button>
                                
                                <div class="footer">
                                    🔒 Suas informações estão seguras e protegidas
                                </div>
                            </div>
                            
                            <script>
                                let countdown = 3;
                                const timerElement = document.getElementById('timer');
                                
                                const interval = setInterval(() => {
                                    countdown--;
                                    timerElement.textContent = countdown;
                                    
                                    if (countdown <= 0) {
                                        clearInterval(interval);
                                        window.close();
                                    }
                                }, 1000);
                                
                                // Tenta fechar após 3 segundos
                                setTimeout(() => {
                                    window.close();
                                }, 3000);
                            </script>
                        </body>
                    </html>
                    """
                    self.wfile.write(html_response.encode('utf-8'))
                    return
                    
            except Exception as e:
                print(f"❌ Erro no callback: {e}")
                
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suprime logs do servidor HTTP"""
        pass


class OAuthServer:
    """Servidor HTTP local para capturar callback OAuth"""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Inicia servidor em thread separada"""
        try:
            self.server = HTTPServer(('localhost', self.port), OAuthCallbackHandler)
            print(f"🌐 Servidor OAuth iniciado na porta {self.port}")
            self.server.timeout = 120  # 2 minutos timeout
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
    
    def _run(self):
        """Executa servidor"""
        try:
            self.server.handle_request()
        except Exception as e:
            print(f"❌ Erro no servidor: {e}")
    
    def get_code(self) -> Optional[str]:
        """Obtém código OAuth capturado"""
        return OAuthCallbackHandler.oauth_code
    
    def stop(self):
        """Para servidor"""
        if self.server:
            try:
                self.server.shutdown()
                print("🛑 Servidor OAuth parado")
            except:
                pass


def test_authentication():
    """Testa autenticação (apenas para desenvolvimento)"""
    print("🧪 Testando autenticação Firebase...")
    
    auth = FirebaseAuth()
    
    # Verifica se já está logado
    if auth.is_logged_in():
        print("✅ Usuário já está logado")
        perfil = auth.load_user_profile()
        print(f"   Email: {perfil.get('email')}")
        print(f"   Nome: {perfil.get('nome')}")
        return
    
    print("⚠️ Nenhum usuário logado")
    print("💡 Execute o app e faça login com Google")


if __name__ == "__main__":
    test_authentication()
