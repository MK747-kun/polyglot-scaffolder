# 🚀 Polyglot Database Scaffolder CLI

A lightweight, developer-focused Command Line Interface (CLI) built with **Python** and **Typer** designed to automatically scaffold clean, production-ready database connection boilerplates based on a simple configuration file.

## ✨ Features

- **YAML-Driven Architecture:** Configure your multi-database environment using a clean `config.yaml` file.
- **Dynamic Boilerplate Generation:** Generates valid architectural code patterns for:
  - 🗄️ **SQL** (SQLAlchemy with a zero-config SQLite prototype)
  - 🍃 **MongoDB** (PyMongo instance setup)
  - 🕸️ **Neo4j** (Transactional driver connection class)
- **Smart Dependency Tracking:** Automatically builds a custom, minimal `requirements.txt` file tailored exclusively to your activated databases.
- **Fail-Safe Integrity:** Prevents destructive file overwrites with localized warnings.

---

## 🛠️ Installation & Setup

1. **Clone the repository and navigate inside:**
   ```bash
   git clone [https://github.com/MK747-kun/polyglot-scaffolder.git](https://github.com/MK747-kun/polyglot-scaffolder.git)
   cd polyglot-scaffolder