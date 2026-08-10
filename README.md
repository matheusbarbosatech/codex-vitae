# 🛡️ Codex Vitae — PWA Life OS & SaaS Fullstack com Notificações Push Nativas VAPID (Python, Biometria & IA)

<div align="center">

![GitHub Actions Workflow](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-Progressive%20Web%20App-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)
![Web Push](https://img.shields.io/badge/Web_Push-VAPID%20Nativo-FF6F00?style=for-the-badge&logo=googlechrome&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Modo%20Sentinela-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Biometria Nativa](https://img.shields.io/badge/Biometria-Nativa-FF4500?style=for-the-badge&logo=apple&logoColor=white)
![LiteLLM](https://img.shields.io/badge/LiteLLM-Proxy%20%26%20Routing-10B981?style=for-the-badge&logo=openai&logoColor=white)

</div>

---

## 📌 Visão Geral do Produto, PWA & Modo Sentinela

**Codex Vitae (Life OS)** é um **SaaS B2C Progressive Web App (PWA)** fullstack construído em Python 3.11+ com FastAPI que combina:

1. **Progressive Web App (PWA) Instalável:** Manifesto `manifest.json` e `sw.js` (Service Worker) permitindo instalação direta na tela inicial ("Add to Home Screen").
2. **Notificações Push Nativas via VAPID (Modo Sentinela):** O worker do Celery monitora a variabilidade de frequência cardíaca (rMSSD/HF-HRV) e carga alostática do usuário em segundo plano. Ao detectar anomalias, a IA (LiteLLM) gera mentorias que são entregues diretamente na tela de bloqueio do usuário via **Web Push API** com protocolo de criptografia **VAPID**.
3. **6 Módulos Científicos:** Calibração Fótica 480nm, Biofeedback de Ressonância (5,5 bpm), Auditoria Semântica NLP, Análise Fractal de Dunbar, Contratos de Ulisses Criptográficos (SHA-256), Simulador do Caos (*Premeditatio Malorum*) e Memento Mori Biométrico.
4. **Máquina de Aquisição PLG:** Reverse Trial com 14 dias de Pro grátis automático e a ferramenta viral **Auditor de Burnout Biométrico (`/auditor-burnout`)**.

👉 **Desenvolvido por:** [Matheus Barbosa](https://github.com/matheusbarbosatech/)

---

## 🔑 Gerador de Chaves VAPID

Para gerar suas chaves VAPID públicas e privadas para autenticação de Web Push Notifications:

```bash
python scripts/generate_vapid_keys.py
```

Cole o resultado no seu arquivo `.env`:
```env
VAPID_PUBLIC_KEY="BEl62iUYgUivxIkv69yViEuiBIa45xV8_..."
VAPID_PRIVATE_KEY="mM8v-U0130X-w0_7xJ0ElnX_..."
VAPID_CLAIM_EMAIL="mailto:sentinel@codexvitae.io"
```

---

## ⚡ Guia de Teste Local das Notificações Push (localhost)

As notificações Push via Service Worker funcionam nativamente em `localhost` sem necessidade de HTTPS:

```bash
# 1. Iniciar o Servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Em outro terminal, iniciar o Worker do Celery (opcional para tarefas em background)
celery -A app.workers.celery_worker.celery_app worker --loglevel=info
```

### Passo a Passo no Navegador:
1. Acesse [http://localhost:8000/dashboard](http://localhost:8000/dashboard).
2. Clique no botão **"Inscrever Dispositivo para Push NATIVO"** ou **"Ativar Modo Sentinela"**.
3. Permita a notificação no pop-up do navegador. O Service Worker registrará a chave pública VAPID e salvará a assinatura no backend (`/api/v1/notifications/subscribe`).
4. Clique no botão **"Testar Push"**. O Modo Sentinela simulará uma anomalia biométrica, gerará a mentoria via IA e disparará a notificação nativa diretamente na sua área de trabalho/tela de bloqueio!

---

## 🧪 Suíte de Testes Automatizados

```bash
python -m pytest -v
```
*Resultado: 18 testes executados com 100% de aprovação (7.21s).*

---

## 👤 Autor & Contato

<div align="center">

**Matheus Barbosa**  
*Engenheiro Full-Stack | Cloud Architect | PWA & AI Specialist*

[![GitHub](https://img.shields.io/badge/GitHub-matheusbarbosatech-181717?style=for-the-badge&logo=github)](https://github.com/matheusbarbosatech/)

</div>

---

## 📄 Licença

Este projeto está sob a licença **MIT** - consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.
