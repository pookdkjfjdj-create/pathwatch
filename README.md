<p align="center">
  <strong><code>pathwatch</code></strong><br>
  <em>Watch directories for file changes -- polling or event-based, zero config.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge&logo=opensourceinitiative" alt="License">
  <img src="https://img.shields.io/badge/Deps-optional-2ea44f?style=for-the-badge" alt="Optional deps">
</p>

---

## What It Does

Watches directories for file modifications and optionally runs commands on changes. Works with zero dependencies (polling mode) or with watchdog for real filesystem events.

## Quick Start

### Watch a directory (no deps)

```bash
python -m pathwatch ./src
```

```
Watching 142 files (Ctrl+C to stop)...
Modified: src/main.py
Modified: src/utils/helpers.py
```

### Watch + auto-run a command

```bash
pip install watchdog
python -m pathwatch ./src --run "pytest"
```

Every file change triggers pytest.

## Use Cases

| Scenario | Command |
|---|---|
| Live-reload dev | `pathwatch ./src --run "python app.py"` |
| Run tests on save | `pathwatch ./tests --run "pytest -x"` |
| Build on change | `pathwatch ./scss --run "sass scss:css"` |

## License

MIT

<p align="center">
  <a href="https://github.com/pookdkjfjdj-create">@pookdkjfjdj-create</a>
</p>
