# Travel Agent Orchestrator

A multi-turn conversational travel planning agent built using OpenAI function/tool calling, structured JSON outputs, and schema-driven orchestration.

This project explores how to design deterministic LLM workflows that combine:
- conversational reasoning
- structured tool invocation
- profile-aware planning
- persistent output generation

The system simulates a lightweight agent runtime where the LLM orchestrates tools to iteratively gather context, brainstorm travel ideas, and generate finalized travel plans.

---

# Problem Overview

The objective of this project is to build a conversational travel assistant that can:

1. Hold multi-turn conversations with users
2. Load and interpret user travel preference profiles
3. Brainstorm travel ideas interactively
4. Generate structured travel plans
5. Persist generated plans to storage

The implementation focuses heavily on:
- deterministic orchestration
- schema validation
- structured outputs
- clean separation between orchestration logic and LLM reasoning

---

# High-Level Architecture

```text
User
  ↓
Agent Orchestrator
  ↓
LLM + Tool Calling
  ↓
Tool Execution Layer
```

The agent acts as the orchestration layer responsible for:
- maintaining conversation flow
- exposing tools to the LLM
- validating structured outputs
- coordinating execution between user interactions and backend functions

---

# Core Workflow

```text
Agent starts
    ↓
LLM loads available user profiles
    ↓
User selects a profile
    ↓
LLM gathers travel preferences through multi-turn interaction
    ↓
Conversation continues iteratively
    ↓
User requests final itinerary
    ↓
LLM generates structured travel plan
    ↓
Travel plan persisted to output file
```

---

# Features

## Multi-Turn Conversational Flow

Supports iterative brainstorming and refinement of travel ideas across multiple conversational turns.

## Structured Tool Calling

Uses function/tool calling patterns to allow the LLM to invoke backend operations deterministically.

## Schema Validation

All LLM outputs are constrained through structured JSON schemas to reduce ambiguity and improve reliability.

## Profile-Aware Planning

User preferences are loaded dynamically from profile files and incorporated into planning decisions.

## Persistent Output Generation

Generated travel plans are saved as structured artifacts for downstream processing or review.

---

# Example Tools

## `load_user_profiles()`

Loads available traveler profiles from disk.

## `read_user_input(prompt)`

Collects user input interactively during conversation flow.

## `save_travel_plan(plan, output_path)`

Persists finalized structured travel plans to storage.

---

# Design Goals

This project intentionally focuses on orchestration and workflow reliability rather than UI complexity.

Key engineering goals include:
- deterministic LLM interactions
- explicit orchestration boundaries
- structured state transitions
- schema-driven validation
- extensible tool integration patterns

---

# Concepts Explored

- OpenAI tool/function calling
- Multi-turn conversational agents
- Structured JSON outputs
- Schema enforcement
- Agent orchestration loops
- Stateful interaction management
- Workflow-driven LLM systems
- Human-in-the-loop execution flows

---

# Tech Stack

- Python
- OpenAI API
- JSON Schema Validation
- Command-Line Interface (CLI)

---

# Running the Project

```bash
python main.py
```

The agent will:
1. Load available user profiles
2. Begin interactive conversation flow
3. Generate a structured travel plan
4. Save the final output to disk

---

# Future Improvements

Potential future enhancements include:
- memory persistence across sessions
- retrieval-augmented profile enrichment
- streaming responses
- async tool execution
- multi-agent planning flows
- web-based interaction interfaces

---

# Purpose of the Project

This repository was built as an exploration of modern LLM orchestration patterns and deterministic conversational workflow design.

The focus is not simply generating text responses, but designing reliable agent execution flows where:
- tools
- structured outputs
- user interaction
- orchestration logic

work together cohesively.
