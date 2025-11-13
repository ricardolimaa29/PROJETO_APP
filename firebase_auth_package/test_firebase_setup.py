"""
Script de teste para verificar configuração Firebase
Execute este script antes de rodar o app principal

python test_firebase_setup.py
"""

import sys
import os
from pathlib import Path

def print_status(icon, message, details=""):
    """Print colorful status messages"""
    print(f"{icon} {message}")
    if details:
        print(f"   {details}")

def check_file(filepath, required=True):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print_status("✅", f"{filepath} encontrado")
        return True
    else:
        status = "❌" if required else "⚠️"
        msg = "OBRIGATÓRIO" if required else "OPCIONAL"
        print_status(status, f"{filepath} não encontrado ({msg})")
        return not required

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Verificando dependências...")
    
    packages = {
        'flet': True,
        'requests': True,
        'dotenv': False,  # Optional
        'firebase_admin': False,  # Optional for now
    }
    
    all_ok = True
    for package, required in packages.items():
        try:
            __import__(package if package != 'dotenv' else 'dotenv')
            print_status("✅", f"{package} instalado")
        except ImportError:
            status = "❌" if required else "⚠️"
            msg = "OBRIGATÓRIO" if required else "OPCIONAL"
            print_status(status, f"{package} não instalado ({msg})")
            if required:
                all_ok = False
    
    return all_ok

def check_config_files():
    """Check configuration files"""
    print("\n📄 Verificando arquivos de configuração...")
    
    # Check templates
    has_env_template = check_file(".env.template", required=False)
    has_config_template = check_file("firebase_config.json.template", required=False)
    
    # Check actual config
    has_env = check_file(".env", required=False)
    has_config = check_file("firebase_config.json", required=False)
    
    if not has_env and not has_config:
        print_status("⚠️", "Nenhum arquivo de configuração encontrado")
        print_status("💡", "Copie .env.template para .env e preencha com suas credenciais")
        return False
    
    return True

def check_credentials():
    """Check if credentials are configured"""
    print("\n🔑 Verificando credenciais...")
    
    # Try to load from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'FIREBASE_API_KEY',
            'GOOGLE_CLIENT_ID_WEB',
            'GOOGLE_CLIENT_SECRET'
        ]
        
        all_set = True
        for var in required_vars:
            value = os.getenv(var)
            if value and value != "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" and "XXXXX" not in value:
                print_status("✅", f"{var} configurado")
            else:
                print_status("❌", f"{var} não configurado ou usando valor padrão")
                all_set = False
        
        return all_set
        
    except ImportError:
        print_status("⚠️", "python-dotenv não instalado, pulando verificação de .env")
        print_status("💡", "Instale com: pip install python-dotenv")
        return None
    except Exception as e:
        print_status("❌", f"Erro ao verificar credenciais: {e}")
        return False

def check_firebase_auth_module():
    """Check if firebase_auth module is accessible"""
    print("\n🔥 Verificando módulo firebase_auth...")
    
    try:
        from firebase_auth import FirebaseAuth, FirebaseAuthConfig
        print_status("✅", "firebase_auth.py importado com sucesso")
        
        # Try to initialize
        try:
            config = FirebaseAuthConfig()
            print_status("✅", "FirebaseAuthConfig inicializado")
            
            auth = FirebaseAuth(config)
            print_status("✅", "FirebaseAuth inicializado")
            
            return True
        except Exception as e:
            print_status("⚠️", f"Aviso ao inicializar: {e}")
            return True  # Still OK, might just be config issue
            
    except ImportError as e:
        print_status("❌", f"Erro ao importar firebase_auth: {e}")
        return False
    except Exception as e:
        print_status("❌", f"Erro inesperado: {e}")
        return False

def check_login_module():
    """Check if login_firebase module is accessible"""
    print("\n🔐 Verificando módulo login_firebase...")
    
    try:
        import flet as ft
        from login_firebase import LoginView
        print_status("✅", "login_firebase.py importado com sucesso")
        print_status("✅", "LoginView acessível")
        return True
    except ImportError as e:
        print_status("❌", f"Erro ao importar: {e}")
        return False
    except Exception as e:
        print_status("❌", f"Erro inesperado: {e}")
        return False

def print_summary(results):
    """Print summary and recommendations"""
    print("\n" + "="*60)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("="*60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print_status("✅", "TUDO OK! Pronto para usar Firebase Authentication")
        print("\n🚀 Próximos passos:")
        print("   1. Configure suas credenciais no arquivo .env")
        print("   2. Execute: python main.py")
        print("   3. Ou teste: python login_firebase.py")
    else:
        print_status("❌", "Alguns problemas encontrados. Veja acima.")
        print("\n📖 Para resolver:")
        
        if not results.get('dependencies'):
            print("   1. Instale dependências: pip install -r requirements.txt")
        
        if not results.get('config'):
            print("   2. Copie o template: cp .env.template .env")
            print("   3. Edite .env com suas credenciais do Firebase")
        
        if not results.get('credentials'):
            print("   4. Configure credenciais no .env")
            print("      Veja QUICKSTART.md para obter as credenciais")
        
        print("\n📚 Documentação:")
        print("   • Guia Rápido: QUICKSTART.md")
        print("   • Guia Completo: FIREBASE_SETUP_GUIDE.md")

def main():
    """Main verification function"""
    print("🔍 VERIFICAÇÃO DE CONFIGURAÇÃO FIREBASE")
    print("="*60)
    print("Este script verifica se tudo está configurado corretamente")
    print("para usar Firebase Authentication no seu app Flet.")
    print("="*60)
    
    results = {
        'dependencies': check_dependencies(),
        'config': check_config_files(),
        'credentials': check_credentials(),
        'firebase_auth': check_firebase_auth_module(),
        'login_module': check_login_module(),
    }
    
    print_summary(results)
    
    # Return exit code
    return 0 if all(v for v in results.values() if v is not None) else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Verificação cancelada pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
