# 🚀 INÍCIO RÁPIDO: Firebase + Google Sign-In

## ⚡ Passo a Passo Rápido (5 minutos)

### 1️⃣ Criar Projeto Firebase

1. Acesse: https://console.firebase.google.com/
2. Clique em **"Adicionar projeto"**
3. Nome: `flet-app-fabrica`
4. Clique em **"Criar projeto"**

### 2️⃣ Habilitar Google Authentication

1. No Firebase Console, vá em **Authentication**
2. Clique em **"Começar"**
3. Na aba **"Sign-in method"**, ative **Google**
4. Clique em **"Salvar"**

### 3️⃣ Obter Credenciais

1. Clique no ícone **Web** (`</>`) na página inicial
2. Nome: `Fabrica Web`
3. **COPIE** a configuração que aparece
4. Vá para **Google Cloud Console**: https://console.cloud.google.com/
5. Selecione o projeto
6. Vá em **APIs & Services > Credentials**
7. Clique em **"Create Credentials" > "OAuth client ID"**
8. Tipo: **Web application**
9. Nome: `Fabrica Web`
10. **Authorized redirect URIs**: `http://localhost:8000/callback`
11. **COPIE** o Client ID e Client Secret

### 4️⃣ Configurar Projeto

```bash
# 1. Copie o template
cp .env.template .env

# 2. Edite o .env com suas credenciais
# (Use um editor de texto)

# 3. Instale as dependências
pip install -r requirements.txt
```

### 5️⃣ Executar

```bash
# Modo de desenvolvimento (usa login_firebase.py)
python -c "import flet as ft; from login_firebase import LoginView; ft.app(target=lambda page: page.views.append(LoginView(page)) or page.go('/'))"

# Ou edite main.py para usar login_firebase no lugar de login
```

---

## 📝 Configuração Detalhada

### Arquivo .env

Edite o arquivo `.env` com suas credenciais:

```env
FIREBASE_API_KEY=sua-api-key-aqui
FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
FIREBASE_PROJECT_ID=seu-projeto
FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abcdef

GOOGLE_CLIENT_ID_WEB=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
```

### Como Obter Cada Valor

#### FIREBASE_API_KEY
- Firebase Console > Configurações do Projeto > Geral
- Seção "Seus apps" > Config (ícone de código)

#### GOOGLE_CLIENT_ID_WEB
- Google Cloud Console > APIs & Services > Credentials
- Seu OAuth 2.0 Client ID (Web)

#### GOOGLE_CLIENT_SECRET
- Mesmo local do Client ID
- Clique no nome do Client ID para ver o Secret

---

## 🔧 Integração com o App Existente

### Opção 1: Substituir login.py (Recomendado)

```bash
# Backup do login atual
mv login.py login_old.py

# Usar nova versão
mv login_firebase.py login.py
```

### Opção 2: Modificar main.py

Edite `main.py`:

```python
# Antes:
from login import LoginView

# Depois:
from login_firebase import LoginView
```

---

## 📱 Para Mobile (Android/iOS)

### Android

1. No Firebase Console, adicione app Android
2. Package name: `com.fabrica.programadores.app`
3. Baixe `google-services.json`
4. Build:

```bash
flet build apk
```

### iOS

1. No Firebase Console, adicione app iOS
2. Bundle ID: `com.fabrica.programadores.app`
3. Baixe `GoogleService-Info.plist`
4. Build:

```bash
flet build ipa
```

---

## ✅ Testando

### Desktop

```bash
python main.py
```

1. Clique em "Entrar com Google"
2. Navegador abre
3. Faça login
4. App redireciona automaticamente

### Problemas Comuns

#### "Invalid client ID"
- Verifique o `.env`
- Confirme Client ID no Google Cloud Console

#### "Redirect URI mismatch"
- Adicione `http://localhost:8000/callback` nos Authorized Redirect URIs

#### "Browser doesn't open"
- Verifique se tem webbrowser instalado
- Tente copiar a URL manualmente

---

## 📚 Documentação Completa

Para guia completo com screenshots: [FIREBASE_SETUP_GUIDE.md](FIREBASE_SETUP_GUIDE.md)

---

## 🆘 Suporte

Problemas? Veja o [Troubleshooting no guia completo](FIREBASE_SETUP_GUIDE.md#troubleshooting)

---

**Desenvolvido para a Fábrica de Programadores 🎓**
