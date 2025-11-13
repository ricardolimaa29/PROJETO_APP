# 🔥 Guia Completo: Firebase + Google Sign-In para Flet Mobile

## 📋 Índice
1. [Visão Geral](#visao-geral)
2. [Pré-requisitos](#pre-requisitos)
3. [Configuração do Firebase](#configuracao-firebase)
4. [Configuração do Google Cloud Console](#configuracao-google)
5. [Instalação de Dependências](#instalacao-dependencias)
6. [Configuração do Projeto Flet](#configuracao-flet)
7. [Implementação do Código](#implementacao-codigo)
8. [Teste e Deploy](#teste-deploy)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral {#visao-geral}

Este guia mostra como integrar Firebase Authentication com Google Sign-In em um aplicativo **Flet mobile**. O fluxo de autenticação funciona da seguinte forma:

```
1. Usuário clica em "Entrar com Google"
2. App abre navegador com página de login do Google
3. Usuário faz login e autoriza o app
4. Firebase processa a autenticação
5. Token retorna para o app mobile
6. Dados do usuário são salvos localmente
7. App redireciona para tela inicial
```

---

## ✅ Pré-requisitos {#pre-requisitos}

- Python 3.10 ou superior instalado
- Conta Google (Gmail)
- Conta Firebase (gratuita)
- Editor de código (VSCode recomendado)
- Flet instalado: `pip install flet`

---

## 🔧 Configuração do Firebase {#configuracao-firebase}

### Passo 1: Criar Projeto no Firebase

1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Clique em **"Adicionar projeto"**
3. Digite o nome do projeto: `flet-app-fabrica` (ou outro nome)
4. Desabilite Google Analytics se não precisar (opcional)
5. Clique em **"Criar projeto"**
6. Aguarde a criação e clique em **"Continuar"**

### Passo 2: Habilitar Google Authentication

1. No menu lateral, clique em **"Authentication"**
2. Clique em **"Começar"** (Get Started)
3. Na aba **"Sign-in method"**, clique em **"Google"**
4. Ative o provedor Google (toggle para ON)
5. Configure o email de suporte do projeto
6. Clique em **"Salvar"**

### Passo 3: Adicionar App ao Firebase

#### Para Android:
1. Na página inicial do projeto, clique no ícone **Android**
2. Preencha:
   - **Package name**: `com.fabrica.programadores.app` (ou seu package)
   - **App nickname**: `Fabrica App`
   - **SHA-1**: Obtenha rodando: `keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android`
3. Clique em **"Registrar app"**
4. Baixe o arquivo **`google-services.json`**
5. Salve na pasta do projeto

#### Para iOS:
1. Clique no ícone **iOS**
2. Preencha:
   - **iOS bundle ID**: `com.fabrica.programadores.app`
   - **App nickname**: `Fabrica App`
3. Baixe o arquivo **`GoogleService-Info.plist`**
4. Salve na pasta do projeto

#### Para Web (teste no navegador):
1. Clique no ícone **Web** (`</>`)
2. Preencha o App nickname: `Fabrica Web`
3. Não marque Firebase Hosting
4. Clique em **"Registrar app"**
5. **COPIE** a configuração Firebase Config (firebaseConfig)
6. Salve em um arquivo chamado `firebase_config.json`:

```json
{
  "apiKey": "SUA_API_KEY_AQUI",
  "authDomain": "seu-projeto.firebaseapp.com",
  "projectId": "seu-projeto",
  "storageBucket": "seu-projeto.appspot.com",
  "messagingSenderId": "123456789",
  "appId": "1:123456789:web:abcdef123456",
  "measurementId": "G-XXXXXXXXXX"
}
```

### Passo 4: Configurar Domínios Autorizados

1. Em **Authentication > Settings > Authorized domains**
2. Adicione os seguintes domínios:
   - `localhost` (para testes)
   - Seu domínio se tiver

---

## 🔑 Configuração do Google Cloud Console {#configuracao-google}

### Passo 1: Acessar Google Cloud Console

1. Vá para [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione o projeto do Firebase (mesmo nome)
3. No menu, vá em **APIs & Services > Credentials**

### Passo 2: Configurar OAuth Consent Screen

1. Clique em **"OAuth consent screen"**
2. Selecione **"External"** (para testes) ou **"Internal"** (se tiver Google Workspace)
3. Preencha:
   - **App name**: `Fábrica de Programadores`
   - **User support email**: seu email
   - **Developer contact**: seu email
4. Em **Scopes**, adicione:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
5. Em **Test users**, adicione os emails que vão testar
6. Salve e continue

### Passo 3: Criar OAuth 2.0 Client IDs

#### Para Android:
1. Clique em **"Create Credentials" > "OAuth client ID"**
2. Selecione **Android**
3. Preencha:
   - **Name**: `Fabrica Android`
   - **Package name**: `com.fabrica.programadores.app`
   - **SHA-1**: (mesmo do passo anterior)
4. Clique em **"Create"**
5. **COPIE** o Client ID gerado

#### Para Web (teste):
1. Crie novo **OAuth client ID**
2. Selecione **Web application**
3. Preencha:
   - **Name**: `Fabrica Web`
   - **Authorized JavaScript origins**: 
     - `http://localhost`
     - `http://localhost:8000`
   - **Authorized redirect URIs**:
     - `http://localhost:8000/callback`
     - `https://seu-projeto.firebaseapp.com/__/auth/handler`
4. Clique em **"Create"**
5. **COPIE** Client ID e Client Secret

### Passo 4: Salvar Credenciais

Crie um arquivo `.env` na raiz do projeto:

```env
# Firebase Config
FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
FIREBASE_PROJECT_ID=seu-projeto
FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abcdef123456

# Google OAuth
GOOGLE_CLIENT_ID_WEB=123456789-xxxxxxxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_CLIENT_ID_ANDROID=123456789-yyyyyyyyyyyyyyyy.apps.googleusercontent.com
```

⚠️ **IMPORTANTE**: Adicione `.env` ao `.gitignore` para não versionar credenciais!

---

## 📦 Instalação de Dependências {#instalacao-dependencias}

### Passo 1: Criar arquivo requirements.txt

Crie ou atualize o `requirements.txt`:

```txt
flet>=0.24.0
firebase-admin>=6.5.0
python-dotenv>=1.0.0
requests>=2.31.0
```

### Passo 2: Instalar dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração do Projeto Flet {#configuracao-flet}

### Passo 1: Estrutura de Pastas

```
PROJETO_APP/
├── .env                    # Credenciais (NÃO VERSIONAR)
├── .gitignore              # Ignorar .env e arquivos sensíveis
├── firebase_config.json    # Config Firebase (NÃO VERSIONAR)
├── google-services.json    # Android config (NÃO VERSIONAR)
├── GoogleService-Info.plist # iOS config (NÃO VERSIONAR)
├── requirements.txt        # Dependências Python
├── main.py                 # Arquivo principal
├── login.py               # Tela de login com Firebase
├── home.py                # Tela inicial
├── firebase_auth.py       # Módulo de autenticação (NOVO)
└── perfil_usuario.json    # Dados do usuário salvos
```

### Passo 2: Atualizar .gitignore

Adicione ao `.gitignore`:

```gitignore
# Credenciais e configurações sensíveis
.env
firebase_config.json
google-services.json
GoogleService-Info.plist
perfil_usuario.json
session.json
usuarios.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
```

---

## 💻 Implementação do Código {#implementacao-codigo}

### Passo 1: Criar módulo firebase_auth.py

Este arquivo contém toda a lógica de autenticação Firebase:

```python
# Ver firebase_auth.py no projeto
```

### Passo 2: Atualizar login.py

Modifique o `login.py` para usar Firebase:

```python
# Ver login_firebase.py no projeto
```

### Passo 3: Como Funciona o Fluxo

#### Desktop/Web:
1. Abre navegador com URL de autenticação Google
2. Usuário faz login
3. Redirect volta para localhost:8000/callback
4. Servidor local captura o código OAuth
5. Troca código por token Firebase
6. Salva dados do usuário

#### Mobile (Android/iOS):
1. Abre navegador nativo com URL de autenticação
2. Usuário faz login
3. Usa custom URL scheme (deep link) para retornar ao app
4. App captura o token
5. Valida com Firebase
6. Salva dados do usuário

---

## 🧪 Teste e Deploy {#teste-deploy}

### Teste Local (Desktop)

```bash
# Rodar o app
python main.py
```

1. Clique em "Entrar com Google"
2. Navegador abre página de login Google
3. Faça login com sua conta
4. Autorize o app
5. Navegador mostra "Login bem-sucedido"
6. App redireciona para /home
7. Dados do perfil aparecem na tela

### Build para Android

```bash
# Instalar Flet build tools
pip install flet

# Criar build Android
flet build apk

# Output: build/apk/app-release.apk
```

**Configurações necessárias no `flet build`:**
- Adicione `google-services.json` na pasta correta
- Configure deep links no AndroidManifest.xml
- Adicione permissões de internet

### Build para iOS

```bash
# Criar build iOS (requer Mac)
flet build ipa

# Output: build/ipa/app-release.ipa
```

**Configurações necessárias:**
- Adicione `GoogleService-Info.plist` ao projeto
- Configure URL schemes no Info.plist
- Configure signing certificate

---

## 🔍 Troubleshooting {#troubleshooting}

### Problema: "Redirect URI mismatch"

**Solução**: 
- Verifique se o redirect URI está autorizado no Google Cloud Console
- Para mobile, use o custom URL scheme correto

### Problema: "Invalid client ID"

**Solução**:
- Verifique se está usando o Client ID correto (Android vs Web)
- Confira o `.env` e `firebase_config.json`

### Problema: "App not authorized"

**Solução**:
- Adicione seu email como Test User no OAuth Consent Screen
- Se for Android, verifique o SHA-1 fingerprint

### Problema: "Token expired"

**Solução**:
- Implemente refresh token
- Re-autentique o usuário

### Problema: "Browser doesn't open on mobile"

**Solução**:
- Use `page.launch_url()` do Flet
- Configure deep links corretamente

### Problema: "Firebase initialization error"

**Solução**:
- Verifique se o arquivo de config existe
- Confirme que as credenciais estão corretas
- Veja os logs do Firebase

---

## 📱 Deep Links para Mobile

### Android (AndroidManifest.xml)

```xml
<activity android:name=".MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="fabricaapp"
            android:host="auth" />
    </intent-filter>
</activity>
```

**URL de callback**: `fabricaapp://auth/callback`

### iOS (Info.plist)

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>fabricaapp</string>
        </array>
        <key>CFBundleURLName</key>
        <string>com.fabrica.programadores.app</string>
    </dict>
</array>
```

**URL de callback**: `fabricaapp://auth/callback`

---

## 🎓 Resumo do Fluxo Completo

### Para Mobile (Produção)

```
1. App Flet Mobile inicia
2. Usuário clica "Entrar com Google"
3. page.launch_url() abre navegador nativo
4. URL: https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=fabricaapp://auth/callback
5. Usuário faz login no Google
6. Google redireciona para: fabricaapp://auth/callback?code=xyz123
7. Sistema operacional abre o app novamente
8. App captura o código (code=xyz123)
9. App envia código para Firebase via API
10. Firebase valida e retorna ID Token
11. App busca dados do usuário (email, nome, foto)
12. App salva em perfil_usuario.json
13. App redireciona para /home
14. Tela inicial mostra dados do perfil
```

### Para Desktop/Web (Desenvolvimento)

```
1. App Flet Desktop inicia
2. Usuário clica "Entrar com Google"
3. Servidor local inicia em localhost:8000
4. webbrowser.open() abre navegador padrão
5. URL: https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=http://localhost:8000/callback
6. Usuário faz login no Google
7. Google redireciona para: http://localhost:8000/callback?code=xyz123
8. Servidor local captura o código
9. Servidor troca código por token Firebase
10. Servidor busca dados do usuário
11. Servidor salva em perfil_usuario.json
12. Servidor fecha e notifica o app
13. App redireciona para /home
14. Tela inicial mostra dados do perfil
```

---

## 🔒 Segurança

### Boas Práticas:

1. **NUNCA** comite credenciais no Git
2. Use `.env` para variáveis sensíveis
3. Adicione `.env` ao `.gitignore`
4. No mobile, use Keychain (iOS) ou Keystore (Android) para tokens
5. Implemente refresh token para sessões longas
6. Valide tokens no backend se tiver servidor
7. Use HTTPS em produção
8. Rotacione credenciais periodicamente

---

## 📚 Recursos Adicionais

- [Documentação Firebase Auth](https://firebase.google.com/docs/auth)
- [Documentação Google Sign-In](https://developers.google.com/identity/sign-in/web)
- [Documentação Flet](https://flet.dev/docs)
- [Firebase Console](https://console.firebase.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

---

## 💡 Dicas Finais

1. **Teste primeiro no desktop** antes de buildar para mobile
2. **Use Test Users** durante desenvolvimento
3. **Monitore o Firebase Console** para ver autenticações em tempo real
4. **Implemente logout** para limpar dados locais
5. **Adicione loading indicators** durante autenticação
6. **Trate erros** de rede e autenticação
7. **Salve estado** para reconectar usuário automaticamente

---

## ✅ Checklist de Implementação

- [ ] Criar projeto no Firebase
- [ ] Habilitar Google Authentication
- [ ] Registrar app (Android/iOS/Web)
- [ ] Baixar arquivos de configuração
- [ ] Configurar OAuth Consent Screen
- [ ] Criar OAuth Client IDs
- [ ] Criar arquivo .env com credenciais
- [ ] Instalar dependências (requirements.txt)
- [ ] Criar firebase_auth.py
- [ ] Atualizar login.py
- [ ] Testar no desktop
- [ ] Configurar deep links (mobile)
- [ ] Build e teste em dispositivo real
- [ ] Publicar no Google Play / App Store

---

**Desenvolvido para a Fábrica de Programadores 🎓**

*Última atualização: 2025-01-13*
