# 🚀 Antigravity Skills Repository

A curated collection of specialized skills designed to enhance the capabilities of Antigravity AI agents. These skills automate common workflows, maintain project context, and orchestrate complex development tasks.

## 🛠️ Installation

You can install any skill from this repository directly into your project using the following command:

```bash
npx skills add https://github.com/MarcRoviraP/skills --skill [skill-name]
```

Replace `[skill-name]` with the identifier of the skill you wish to activate.

---

## 📦 Available Skills

### 📂 [agente-context-logger](https://github.com/MarcRoviraP/skills/tree/main/skills/agente-context-logger)
**Purpose**: Maintains a session history in Markdown within a project's `logs_md_agente` folder.
- **Why use it**: Bridges the context gap between sessions or different agents. 
- **Trigger**: Session starts, major task completion, or session finalization.

### 🏗️ [project-orchestrator](https://github.com/MarcRoviraP/skills/tree/main/skills/project-orchestrator)
**Purpose**: Automates project initialization, documentation updates, and test generation.
- **Why use it**: Ensures project standards are met and context is retrieved from previous logs automatically.
- **Feature**: Integrated with `agente-context-logger` for automated transition between sessions.

### 🧠 [memory-orchestrator](https://github.com/MarcRoviraP/skills/tree/main/skills/memory-orchestrator)
**Purpose**: Integrates with Engram for long-term persistent memory.
- **Why use it**: Allows the agent to remember project-wide decisions and state across the entire development lifecycle.

### 🛠️ [skill-creator](https://github.com/MarcRoviraP/skills/tree/main/skills/skill-creator)
**Purpose**: A toolkit for building, testing, and optimizing new Antigravity skills.
- **Why use it**: Provides a standardized workflow for developing robust and verifiable skills.

---

## 📄 Usage & Best Practices

- **Context First**: Always use the `project-orchestrator` to catch up on recent work by reading the `logs_md_agente` folder.
- **Transitional Memory**: Use the `agente-context-logger` to leave "checkpoint" notes for the next session. This minimizes redundant planning time.
- **Isolation**: Skills are designed to be composable. Feel free to combine the orchestrator with specialized loggers for maximum efficiency.

---

## 🤝 Contributing

To add a new skill to this repository:
1. Use the `skill-creator` to draft and test your logic.
2. Ensure the `SKILL.md` file follows the standardized format.
3. Bundle any required scripts in a `scripts/` subdirectory.

---

*Automated with ❤️ by Antigravity Agents.*
