import logging
from typing import Dict, Any, Optional

try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    litellm = None
    LITELLM_AVAILABLE = False

from app.core.config import settings

logger = logging.getLogger(__name__)

# System prompts for the 6 Codex Vitae modules
MODULE_PROMPTS: Dict[str, Dict[str, str]] = {
    "maquina": {
        "title": "Módulo 1: A Máquina (Engenharia Corporal & Biologia)",
        "prompt": (
            "Você é o Especialista Chefe em Otimização Corporal do Codex Vitae. "
            "Gere um plano de Engenharia Humana focado no pilar 'A MÁQUINA'. "
            "Cubra: 1. Higiene do Sono & Ritmo Circadiano, 2. Protocolo de Treino & Mobilidade, "
            "3. Otimização de Postura & Biohacking Físico, 4. Métricas diárias de recuperação (HRV/VFC)."
        )
    },
    "processador": {
        "title": "Módulo 2: O Processador (Cognição & Foco Inabalável)",
        "prompt": (
            "Você é o Arquiteto de Neurociência & Cognição do Codex Vitae. "
            "Gere um plano de Engenharia Humana focado no pilar 'O PROCESSADOR'. "
            "Cubra: 1. Bloco de Deep Work & Estado de Flow, 2. Gestão de Dopamina & Detox Digital, "
            "3. Treinamento de Foco e Memória de Trabalho, 4. Protocolo Anti-Brain Fog."
        )
    },
    "tribo": {
        "title": "Módulo 3: A Tribo (Inteligência Social & Relacionamentos)",
        "prompt": (
            "Você é o Mentor de Inteligência Social & Liderança do Codex Vitae. "
            "Gere um plano de Engenharia Humana focado no pilar 'A TRIBO'. "
            "Cubra: 1. Comunicação Assertiva & Presença Executiva, 2. Otimização do Círculo Interno (Rede de Valor), "
            "3. Gestão de Conflitos & Limites Pessoais, 4. Protocolo de Empatia & Conexão Profunda."
        )
    },
    "combustivel": {
        "title": "Módulo 4: O Combustível (Nutrição & Bioenergética)",
        "prompt": (
            "Você é o Bioquímico & Nutricionista de Performance do Codex Vitae. "
            "Gere um plano de Engenharia Humana focado no pilar 'O COMBUSTÍVEL'. "
            "Cubra: 1. Macro & Micronutrientes Estratégicos, 2. Janelas de Alimentação & Jejum Intermitente, "
            "3. Stack de Suplementação Otimizada, 4. Hidratação Eletrolítica & Mitocôndrias."
        )
    },
    "escudo": {
        "title": "Módulo 5: O Escudo (Estoicismo & Resiliência Emocional)",
        "prompt": (
            "Você é o Mestre Estoico & Psicológico do Codex Vitae. "
            "Gere um plano de Engenharia Humana focado no pilar 'O ESCUDO'. "
            "Cubra: 1. Dicotomia do Controle & Memento Mori, 2. Protocolo de Gestão do Cortisol & Estresse, "
            "3. Requadramento Cognitivo de Adversidades, 4. Práticas Diárias de Diário & Reflexão."
        )
    },
    "bussola": {
        "title": "Módulo 6: A Bússola (Propósito & Arquitetura de Vida)",
        "prompt": (
            "Você é o Estrategista de Vida & Visão do Codex Vitae. "
            "Gere um plano de Engenharia Humana focado no pilar 'A BÚSSOLA'. "
            "Cubra: 1. Definição de Valores Inegociáveis, 2. OKRs Pessoais de Curto e Longo Prazo, "
            "3. Visão de Legado & Alinhamento Diário, 4. Matriz de Tomada de Decisão Estratégica."
        )
    }
}


def generate_mock_plan(module_key: str, user_context: Optional[str] = None) -> str:
    """Fallback generator when no cloud API keys are present"""
    mod_info = MODULE_PROMPTS.get(module_key, {
        "title": "Módulo de Otimização Geral",
        "prompt": "Gere um protocolo de otimização."
    })
    
    ctx_str = f"\n* Contexto fornecido: '{user_context}'" if user_context else ""
    
    return f"""# 🛡️ Codex Vitae — Plan de Engenharia Humana
## {mod_info['title']}
*Status: Otimizado via IA Open-Source (Modelo: {settings.DEFAULT_LLM_MODEL})*{ctx_str}

---

### 1. DIAGNÓSTICO E OBJETIVOS PRIMÁRIOS
- **Diagnóstico Inicial:** Identificamos gargalos na eficiência do seu pilar **{module_key.upper()}**.
- **Meta Operacional:** Elevar o nível de consistência em +40% nos próximos 30 dias através de micro-hábitos estruturados.

---

### 2. PROTOCOLO DE AÇÃO PASSO A PASSO

#### 🎯 Fase A: Fundação (Dias 1 a 7)
- **Ação 1:** Estabelecer gatilho ambiental às 07:00 da manhã.
- **Ação 2:** Eliminar fricção cognitiva inicial removendo distrações primárias.
- **Métrica:** Cumprir o ritual diário por pelo menos 5 dias seguidos.

#### ⚡ Fase B: Intensificação (Dias 8 a 21)
- **Ação 3:** Expandir o bloco de foco ou estímulo físico para 90 minutos ininterruptos.
- **Ação 4:** Aplicar feedback loop noturno registrando métricas no diário de alta performance.

#### 👑 Fase C: Mastery & Automação (Dias 22 a 30)
- **Ação 5:** Consolidar a rotina como um sistema padrão não-negociável.
- **Ação 6:** Avaliação de resultados e ajuste fino dos parâmetros.

---

### 3. REGRAS INEGOCIÁVEIS DO CODEX
1. **Sem Desculpas:** A execução supera a intenção.
2. **Consistência > Intensidade:** 1% de progresso diário gera 37x no ciclo de 1 ano.
3. **Mede o que Importa:** Se você não mede, não gerencia.

---
*Gere um novo plano no Codex Vitae a qualquer momento para recalibrar seus objetivos.*
"""


async def generate_codex_plan(module_key: str, user_context: Optional[str] = None) -> str:
    """
    Generates a personalized Codex Vitae human engineering plan.
    Uses LiteLLM if API keys are present, otherwise uses mock generator.
    """
    module_info = MODULE_PROMPTS.get(module_key)
    if not module_info:
        raise ValueError(f"Módulo '{module_key}' é inválido.")

    system_prompt = module_info["prompt"]
    user_prompt = f"Contexto e Objetivos do Usuário: {user_context or 'Solicito protocolo padrão de alta performance.'}"

    has_api_key = bool(settings.GROQ_API_KEY or settings.OPENROUTER_API_KEY or settings.OPENAI_API_KEY)

    if not LITELLM_AVAILABLE or not has_api_key:
        logger.info(f"LiteLLM ou API key de IA não disponível. Utilizando gerador simulado para o módulo {module_key}.")
        return generate_mock_plan(module_key, user_context)

    try:
        # Prepare parameters for LiteLLM
        model = settings.DEFAULT_LLM_MODEL
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500
        }

        if settings.GROQ_API_KEY:
            kwargs["api_key"] = settings.GROQ_API_KEY
        elif settings.OPENROUTER_API_KEY:
            kwargs["api_key"] = settings.OPENROUTER_API_KEY
        elif settings.OPENAI_API_KEY:
            kwargs["api_key"] = settings.OPENAI_API_KEY

        response = await litellm.acompletion(**kwargs)
        content = response.choices[0].message.content
        return content

    except Exception as e:
        logger.error(f"Erro ao chamar LiteLLM: {e}. Alternando para fallback mock plan.")
        return generate_mock_plan(module_key, user_context)
