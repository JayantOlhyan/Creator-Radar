# CreatorRadar — System Architecture

## Overview

CreatorRadar is an open-source creator-intelligence platform designed to monitor creators, detect new content, analyze content patterns, and generate original content opportunities tailored to the user's expertise.

## Core Product Loop

```text
WATCH → DETECT → INGEST → ANALYZE → EXTRACT PATTERN → PERSONALIZE → SCORE → NOTIFY → CREATE
```

## Architectural Principles

1. **Platform Agnostic Core**: The core domain model operates strictly on platform-agnostic concepts (`Creator`, `Post`, `PostMedia`, `PostAnalysis`, `ContentPattern`, `KnowledgeItem`, `ContentOpportunity`, `Notification`). Platform details are isolated into Source Adapters.
2. **Source Adapter Abstraction**: Uniform contract (`validate_creator`, `fetch_creator`, `fetch_latest_posts`, `fetch_post`) wrapping acquisition mechanisms for Instagram, LinkedIn, YouTube, X, and Reddit.
3. **AI Provider Abstraction**: Provider interface (`analyze_content`, `extract_pattern`, `personalize_opportunity`) supporting OpenAI, Gemini, Anthropic, Local (Ollama), and Mock implementations configured dynamically.
4. **Asynchronous Job Processing**: Decoupled asynchronous worker queue powered by Redis and Arq workers to execute pipeline jobs without blocking HTTP handlers.

## High-Level Topology

```text
               ┌───────────────────────┐
               │    Next.js Web UI     │
               └───────────┬───────────┘
                           │ HTTP / REST
                           ▼
               ┌───────────────────────┐
               │   FastAPI API Layer   │
               └───────────┬───────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
  ┌────────────────────┐      ┌────────────────────┐
  │ PostgreSQL Database│      │  Redis Queue (Arq) │
  └────────────────────┘      └──────────┬─────────┘
                                         │ Job Dispatch
                                         ▼
                              ┌────────────────────┐
                              │ Async Queue Worker │
                              └──────────┬─────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼                       ▼                       ▼
      ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
      │  Source Adapters   │  │    AI Providers    │  │    Notification    │
      │(IG, LI, YT, X, etc)│  │(OpenAI, Gemini,etc)│  │  (Telegram Bot)    │
      └────────────────────┘  └────────────────────┘  └────────────────────┘
```
