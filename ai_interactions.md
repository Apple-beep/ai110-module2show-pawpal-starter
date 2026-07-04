# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->

## Agent Workflow: Data Persistence Extension

Task requested of the agent:
Add JSON persistence so PawPal+ can remember owner, pet, and task data between app runs.

Files modified:
- `pawpal_system.py`
- `app.py`
- `tests/test_pawpal.py`
- `README.md`
- `ai_interactions.md`

What the agent completed:
- Added dictionary conversion methods for `Task`, `Pet`, and `Owner`.
- Added `Scheduler.save_to_json()` and `Scheduler.load_from_json()`.
- Connected the Streamlit app to `data.json`.
- Added a pytest case for save/load behavior.
- Updated documentation to explain the persistence workflow.

Manual corrections made:
- Fixed an indentation issue in `app.py`.
- Kept persistence simple with custom dictionary conversion instead of adding a new serialization library.
- Used `data.json` as a local project file to keep the extension easy to test and explain.
- Preserved the existing OOP design instead of adding extra storage classes.
