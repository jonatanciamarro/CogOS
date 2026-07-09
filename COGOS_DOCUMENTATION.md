# CogOS — O Sistema Operacional Cognitivo (Mega Documentação)

> **"A Humanidade desenvolveu sistemas operacionais para computadores, bancos de dados para informação e inteligência artificial para raciocínio. O CogOS é a tentativa de estabelecer a Engenharia de Sistemas Cognitivos como uma disciplina operacional."**

Este documento é um guia definitivo de investigação e referência sobre o **CogOS**. Foi desenhado para que qualquer engenheiro ou IA compreenda perfeitamente o propósito, a arquitetura e os mecanismos do projeto, permitindo a continuidade e a evolução ininterrupta do ecossistema.

---

## 1. O Que é o CogOS?

O **CogOS** não é apenas um "simulador de agentes". É uma arquitetura de referência para a **Cognitive Systems Engineering (CSE)**. Ele funciona como um laboratório experimental que modela a evolução de ecossistemas cognitivos.

Em vez de focar apenas em como um agente pensa de forma isolada, o CogOS simula **como o conhecimento, a cultura, as crenças e a inteligência evoluem ao longo do tempo em uma sociedade através de instituições e pressão ambiental**. Ele implementa seleção natural, especiação de organizações, rastreabilidade memética e ciclos de colapso/renascimento.

---

## 2. A Hierarquia Arquitetural

O sistema respeita uma hierarquia rígida (Hierarchy Rule). Cada camada é dona da camada inferior e as responsabilidades não devem ser misturadas.

```text
Simulation
└── World
    └── Civilization
        └── Settlement
            └── Agent / Institution
```

* **Simulation**: Controla o loop de execução (kernel), os pipelines de ticks e os critérios de parada. Não possui lógica de domínio (economia, ciência, etc.).
* **World**: O contêiner físico e global. Gerencia eventos inter-civilizações e sistemas globais (ex: Clima, Fluxo de Recursos Globais).
* **Civilization**: Orquestra um agrupamento de settlements e gerencia épocas (eras temporais).
* **Settlement**: A comunidade local. Controla a população, o ambiente local e a execução do loop cognitivo dos agentes e instituições.
* **Agent**: Entidade individual (ex: um pesquisador). Possui modelo cognitivo, memória, orçamento (energia/atenção) e confiança.
* **Institution (Organization)**: Um grupo de agentes (ex: laboratórios ou universidades) que atuam coletivamente, possuem cultura (DNA), reputação e capacidade de produzir conhecimento.

---

## 3. Os 3 Pilares do Desacoplamento (Domain Isolation)

O CogOS possui uma regra estrita: **Nenhum módulo de domínio concreto pode importar outro módulo de domínio concreto.** (Ex: `economy` nunca importa `science` diretamente).

Toda a comunicação inter-domínios é feita por meio de:

1. **Protocols (`runtime/contracts/`)**: Interfaces estruturais (PEP 544) que definem como os subsistemas se comunicam.
2. **ServiceRegistry (`runtime/context/service_registry.py`)**: Um registro central para Injeção de Dependências. Se o módulo da economia precisar da ciência, ele resolve a interface da ciência através do `registry`.
3. **EventBus (`runtime/bus/event_bus.py`)**: O coração assíncrono/síncrono. Mudanças de estado e ações (como `ResearchCompletedEvent`, `ExtinctionEvent`) são publicadas aqui. Observadores (como a Telemetria ou Estágios de Pipeline) escutam e reagem, garantindo arquitetura orientada a eventos (*Event-Sourced*).

---

## 4. O Pipeline de Simulação (`PipelineStage`)

Cada tick do simulador não é um monolito de código. Ele é composto por uma sequência de **PipelineStages**.

A classe `ScienceInstitutionStage` (em `runtime/pipeline/science_institution_stage.py`), por exemplo, define exatamente o que as instituições fazem a cada tick de simulação:
1. Pagar os custos de manutenção (burocracia).
2. Pool de recursos coletivos e pesquisa científica.
3. Decadimento da memória (esquecimento do conhecimento antigo/não utilizado).
4. Decadimento de prestígio e loops de ciclo de vida (Declínio $\to$ Colapso ou Renascimento).

A `Simulation` apenas itera sobre os estágios configurados no `config.tick_pipeline` e executa a função `run()` de cada um deles.

---

## 5. Ecologia Institucional e Evolução Cognitiva (Sprint 5.x)

Um dos sistemas mais avançados do CogOS é a sua camada evolutiva de instituições (Sprints 5.0 a 5.4). As organizações no CogOS evoluem como uma ecologia de espécies.

### 5.1. DNA Institucional (`InstitutionDNA`)
Cada instituição não é apenas uma lista de membros, ela possui um **DNA (Genoma Institucional)** que define *como ela pensa*:
* `procedural_traits`: Metodologias (ex: empirismo).
* `cognitive_traits`: Vetor numérico (abstração, tolerância a risco, exploração).
* `preferred_niches`: Nichos científicos preferidos (ex: física, biologia).

### 5.2. Especiação (`speciation_profile`)
Com base nos traços cognitivos do DNA, as instituições são automaticamente classificadas em **Espécies Cognitivas**:
* `INNOVATIVE_EXPLORER` (alta exploração e risco)
* `CONSERVATIVE_ARCHIVE` (baixa exploração, focado em retenção)
* `APPLIED_PRACTITIONER` (alta prática, baixa abstração)
* `ACADEMIC_THEORIST` (alta abstração)

Essas espécies possuem modificadores (`SPECIES_MODIFIERS`) que afetam custo de energia, velocidade de descoberta, taxa de inovação e retenção de memória.

### 5.3. Árvore Filogenética (`PhylogenyTracker`) e Fósseis (`FossilRecord`)
O sistema mantém memória de quem veio de quem:
* Quando uma instituição colapsa, ela gera um **Fóssil** persistente no `FossilRecord` e um `ExtinctionEvent` é disparado.
* Instituições "filhas" colonizadas formam uma **Árvore Filogenética**, mapeada pelo `PhylogenyTracker`. Mutações geram `AdaptationEvent`.

### 5.4. Pressão de Nicho (Niche Congestion) e Conhecimento Rastreável
Múltiplas instituições operando no mesmo nicho sofrem **Pressão Ambiental**, aumentando os custos de pesquisa. Artefatos de conhecimento gerados carregam a propriedade `origin_species` para mapearmos como uma descoberta científica (memética) evoluiu a partir do DNA da instituição.

---

## 6. Observabilidade e Métricas (Sprints 4.7 e 5.x)

O CogOS não seria científico se não pudesse ser mensurado.
O módulo `runtime.observability` usa o `EventBus` para compilar métricas ecológicas (Telemetry):
* **IDI (Institution Diversity Index)**: Entropia de Shannon normalizada que mede a diversidade de espécies no ecossistema (evitando o domínio de um único perfil cognitivo).
* **ICR (Institution Churn Rate)**: Taxa de natalidade vs mortalidade institucional.
* **IRI (Institutional Recovery Index)**: O quão rápido a sociedade volta a inovar após um colapso cataclísmico.

---

## 7. Como Evoluir o CogOS? (Guia para IAs e Desenvolvedores)

Se você é a próxima Inteligência Artificial ou Desenvolvedor pegando este projeto, siga estas regras de ouro:

1. **Nunca quebre o Domain Isolation**: Use sempre Protocolos e o Registry se for acoplar módulos diferentes.
2. **Eventos primeiro**: Se algo importante acontecer (uma entidade nascer, aprender ou morrer), crie um `@dataclass(frozen=True)` em `*_events.py` e publique no `EventBus`.
3. **Mantenha a Hierarquia**: Se quiser adicionar "Governos" ou "Políticas", coloque-as sob a `Civilization` ou `Settlement`.
4. **Use e amplie os Benchmarks**: Cada grande feature é validada por um `cbXXX_runner.py` no diretório `simulator/`. (Ex: `cb015_runner.py` valida o Jardim Evolutivo). Use os benchmarks para validar estabilidade após grandes refatorações.
5. **Evolua a Telemetria**: Se criar um novo comportamento emergente, crie uma classe de métrica que herde de `Metric` em `runtime/observability/` para medir isso.

---
**Fim do Documento.**  
*O futuro do CogOS é simular a origem da linguagem, mercados baseados em confiança e modelos preditivos de civilizações. Siga adiante.*
