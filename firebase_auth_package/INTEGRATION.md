# 🔥 Como Integrar Firebase Auth no App Existente

Este documento explica como integrar a nova autenticação Firebase no app existente.

## 📋 Opções de Integração

### Opção 1: Substituir login.py Completamente (Mais Fácil)

```bash
# 1. Faça backup do login atual
mv login.py login_original_backup.py

# 2. Renomeie o novo login
cp login_firebase.py login.py

# 3. Pronto! O main.py já vai usar automaticamente
python main.py
```

### Opção 2: Manter Ambos e Escolher no main.py (Flexível)

Edite `main.py` e modifique a importação:

```python
# No início do arquivo, escolha qual login usar:

# Para usar o login com Firebase:
from login_firebase import LoginView

# Para usar o login original:
# from login import LoginView

# O resto do código permanece igual
```

### Opção 3: Criar Toggle para Alternar (Avançado)

Edite `main.py`:

```python
import flet as ft
from home import HomeView
from desempenho import DesempenhoView

# Importa ambos os logins
from login import LoginView as LoginViewOriginal
from login_firebase import LoginView as LoginViewFirebase

# Escolhe qual usar (pode ser uma variável de configuração)
USE_FIREBASE = True  # Mude para False para usar o login original
LoginView = LoginViewFirebase if USE_FIREBASE else LoginViewOriginal

# ... resto do código permanece igual
```

---

## 🔧 Configuração Necessária

Antes de usar, configure suas credenciais:

### 1. Criar arquivo .env

```bash
cp .env.template .env
```

### 2. Editar .env com suas credenciais

```env
FIREBASE_API_KEY=sua-chave-aqui
FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
FIREBASE_PROJECT_ID=seu-projeto
GOOGLE_CLIENT_ID_WEB=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
```

### 3. Obter credenciais

Veja o guia completo: [QUICKSTART.md](QUICKSTART.md)

---

## 🎯 Funcionalidades Adicionadas

### Login Automático
O novo sistema mantém a sessão do usuário:

```python
# Se o usuário já fez login, entra automaticamente
if firebase_auth.is_logged_in():
    page.go("/home")
```

### Dados do Perfil
Os dados ficam salvos em `perfil_usuario.json`:

```json
{
  "nome": "João Silva",
  "email": "joao@gmail.com",
  "foto": "https://...",
  "login_google": true,
  "data_login": "2025-01-13 14:30:00"
}
```

### Integração com home.py
A `HomeView` já está preparada para carregar esses dados automaticamente!

O arquivo `home.py` possui:
- `load_profile_from_file()` - carrega perfil salvo
- `start_profile_watcher()` - monitora mudanças no arquivo
- Atualização automática quando perfil muda

---

## 📱 Diferenças entre Desktop e Mobile

### Desktop
- Abre navegador no sistema
- Usa `localhost:8000` para callback
- Funciona imediatamente

### Mobile
- Abre navegador nativo do dispositivo
- Usa deep link para retornar ao app
- Requer configuração adicional (ver guia)

---

## 🧪 Testando

### Teste Básico

```bash
# 1. Verifique a configuração
python test_firebase_setup.py

# 2. Execute o app
python main.py

# 3. Clique em "Entrar com Google"
# 4. Faça login
# 5. Deve redirecionar para /home automaticamente
```

### Verificar Dados Salvos

```bash
# Ver perfil salvo
cat perfil_usuario.json

# Ou no Python:
python -c "import json; print(json.dumps(json.load(open('perfil_usuario.json')), indent=2))"
```

---

## 🔄 Fluxo de Autenticação

```
1. Usuário clica "Entrar com Google"
   └─> login_firebase.py: login_google()

2. Abre navegador com URL do Google
   └─> firebase_auth.py: get_google_auth_url()

3. Usuário faz login no Google
   └─> Google retorna código OAuth

4. App captura código
   └─> OAuthServer (desktop) ou Deep Link (mobile)

5. Troca código por token
   └─> firebase_auth.py: exchange_code_for_token()

6. Obtém dados do usuário
   └─> firebase_auth.py: get_user_info()

7. Salva perfil localmente
   └─> firebase_auth.py: save_user_profile()
   └─> Arquivo: perfil_usuario.json

8. Redireciona para /home
   └─> page.go("/home")

9. HomeView carrega perfil
   └─> home.py: load_profile_from_file()
   └─> Exibe nome, email, foto do usuário
```

---

## 🐛 Problemas Comuns

### "No module named 'firebase_auth'"
```bash
# Certifique-se de estar no diretório correto
cd /caminho/do/projeto
python main.py
```

### "Invalid client ID"
```bash
# Verifique o .env
cat .env | grep CLIENT_ID

# Deve ter o Client ID correto do Google Cloud Console
```

### "Redirect URI mismatch"
```bash
# No Google Cloud Console, adicione:
# http://localhost:8000/callback
```

### Botão "Entrar com Google" não responde
```bash
# Verifique se o servidor inicia:
# Deve aparecer: "🌐 Servidor OAuth iniciado na porta 8000"

# Teste manualmente:
python -c "from firebase_auth import OAuthServer; s = OAuthServer(); s.start(); import time; time.sleep(60)"
```

---

## 📊 Estrutura de Arquivos

```
PROJETO_APP/
├── main.py                          # Arquivo principal (importa LoginView)
├── login.py                         # Login original (backup)
├── login_firebase.py                # ✨ Novo login com Firebase
├── home.py                          # Tela inicial (já integrado!)
├── firebase_auth.py                 # ✨ Módulo de autenticação
├── perfil_usuario.json             # Dados do usuário (criado após login)
├── .env                            # ✨ Suas credenciais (NÃO COMITAR!)
├── .env.template                   # Template de configuração
├── firebase_config.json.template   # Template alternativo
├── requirements.txt                # Dependências
├── test_firebase_setup.py         # ✨ Script de verificação
├── QUICKSTART.md                   # ✨ Guia rápido
├── FIREBASE_SETUP_GUIDE.md        # ✨ Guia completo
└── INTEGRATION.md                  # Este arquivo
```

---

## ✅ Checklist de Integração

- [ ] Backup do login.py original
- [ ] Criar arquivo .env com credenciais
- [ ] Executar test_firebase_setup.py
- [ ] Escolher método de integração (Opção 1, 2 ou 3)
- [ ] Testar login no desktop
- [ ] Verificar se perfil_usuario.json é criado
- [ ] Verificar se HomeView mostra dados do perfil
- [ ] (Opcional) Configurar para mobile

---

## 🎓 Próximos Passos

1. **Agora**: Configure e teste no desktop
2. **Depois**: Build para mobile e teste em dispositivo
3. **Futuro**: Adicione mais funcionalidades:
   - Logout
   - Refresh token
   - Múltiplos usuários
   - Sincronização com backend

---

## 📞 Suporte

- Problemas? Veja [FIREBASE_SETUP_GUIDE.md](FIREBASE_SETUP_GUIDE.md#troubleshooting)
- Dúvidas? Abra uma issue no GitHub

---

**Desenvolvido para a Fábrica de Programadores 🎓**

*Última atualização: 2025-01-13*
