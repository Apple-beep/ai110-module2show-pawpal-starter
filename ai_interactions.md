# AI Interactions Log

## Agent Workflow: Data Persistence Extension

Task requested of the agent:

I asked the AI agent to add a data persistence layer to PawPal+ so that owner, pet, and task data could be saved between application runs.

Files modified:

- `pawpal_system.py`
- `app.py`
- `tests/test_pawpal.py`
- `README.md`
- `ai_interactions.md`

What the agent completed:

- Added `to_dict()` and `from_dict()` methods for the `Task`, `Pet`, and `Owner` classes.
- Added `Scheduler.save_to_json()` to save project data into a local `data.json` file.
- Added `Scheduler.load_from_json()` to load saved data back into the app.
- Updated the Streamlit app so it loads saved data when the app starts.
- Updated the Streamlit app so it saves data after owner updates, pet creation, task creation, and task completion.
- Added a pytest test to verify JSON save/load behavior.
- Updated the README to explain the persistence workflow and files modified.

What I had to verify or fix manually:

- I manually ran `python -m py_compile pawpal_system.py main.py app.py` to check for syntax errors.
- I manually ran `python -m pytest` to confirm all 15 tests passed.
- I fixed an indentation issue in `app.py`.
- I checked the Streamlit UI to confirm that pets and tasks stayed after app actions.
- I kept the persistence design simple by using custom dictionary conversion instead of adding a new library like marshmallow.
- I reviewed the final code to make sure the persistence layer matched the existing OOP structure.

## Prompt Comparison: Scheduling Logic

| Category | Option A | Option B |
|---|---|---|
| Model or tool used | ChatGPT | AI coding assistant in VS Code |
| Prompt or task | Asked for a pet care scheduler with sorting, filtering, recurrence, and conflict detection | Asked for help connecting the scheduling logic into the existing project files and Streamlit UI |
| Response summary | Suggested scheduler features such as sorting by due time, filtering by pet/status/priority, detecting overlapping tasks, and creating recurring tasks | Suggested implementation edits that connected backend scheduling logic to user-facing app behavior |
| What was useful | The output helped me plan the main algorithms before coding and made the class responsibilities clearer | The output helped integrate the scheduler into `app.py`, especially schedule display, pending tasks, and task completion |
| Problems noticed | Some ideas were more complex than needed, such as automatic rescheduling or extra helper classes | Some generated edits needed manual fixes, especially indentation and Markdown formatting |
| Decision | I used the simpler scheduling design because it matched the rubric and was easier to test | I used the integration approach but manually verified the final code with CLI output and pytest |

Final student decision:

I used the simpler readable scheduling design instead of adding automatic rescheduling. The final implementation uses priority sorting, due-time sorting, filtering, conflict detection, recurring task creation, and JSON persistence. This approach matched the project rubric, worked across multiple pets, and was easy to verify using both the CLI demo and automated pytest tests.


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
