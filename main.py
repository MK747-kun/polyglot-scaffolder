import typer
import yaml
from pathlib import Path

app = typer.Typer(help="🚀 Polyglot Database Scaffolder CLI")

DEFAULT_CONFIG = """# Polyglot Scaffolder Configuration
project_name: "my_polyglot_app"

databases:
  sql: true
  mongodb: true
  neo4j: false
"""

# --- DATABASE TEMPLATE STRINGS ---

SQL_TEMPLATE = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./sql_database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_sql_db():
    \"\"\"Dependency utility to yield a database session and close it cleanly.\"\"\"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

MONGO_TEMPLATE = """from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["polyglot_document_db"]

def get_mongo_db():
    \"\"\"Returns the active MongoDB database instance.\"\"\"
    return db
"""

NEO4J_TEMPLATE = """from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "password")

class Neo4jConnection:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        \"\"\"Executes a Cypher query inside a secure transactional session.\"\"\"
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

graph_db = Neo4jConnection(NEO4J_URI, NEO4J_AUTH)
"""

# --- CLI COMMANDS ---

@app.command()
def init():
    """Initialize a default config.yaml file in the current directory."""
    config_path = Path("config.yaml")
    
    if config_path.exists():
        typer.secho("⚠️  config.yaml already exists in this directory!", fg=typer.colors.YELLOW)
        raise typer.Exit()
        
    config_path.write_text(DEFAULT_CONFIG)
    typer.secho("✨ Successfully created config.yaml!", fg=typer.colors.GREEN)


@app.command()
def generate():
    """Read config.yaml and scaffold the requested database connection files."""
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        typer.secho("❌ Error: config.yaml not found! Run 'python main.py init' first.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
    except Exception as e:
        typer.secho(f"❌ Error parsing config.yaml: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    db_choices = config.get("databases", {})
    project_name = config.get("project_name", "my_polyglot_app")
    
    output_dir = Path("database")
    output_dir.mkdir(exist_ok=True)
    
    # Track which packages the user actually needs
    requirements = []
    
    typer.secho(f"🏗️  Scaffolding databases for project: '{project_name}'...", fg=typer.colors.CYAN)
    
    # Generate SQL boilerplate
    if db_choices.get("sql"):
        sql_file = output_dir / "sql_db.py"
        sql_file.write_text(SQL_TEMPLATE)
        requirements.append("sqlalchemy")
        typer.echo("  ✅ Created database/sql_db.py (SQLAlchemy)")
        
    # Generate MongoDB boilerplate
    if db_choices.get("mongodb"):
        mongo_file = output_dir / "mongo_db.py"
        mongo_file.write_text(MONGO_TEMPLATE)
        requirements.append("pymongo")
        typer.echo("  ✅ Created database/mongo_db.py (PyMongo)")
        
    # Generate Neo4j boilerplate
    if db_choices.get("neo4j"):
        neo4j_file = output_dir / "neo4j_db.py"
        neo4j_file.write_text(NEO4J_TEMPLATE)
        requirements.append("neo4j")
        typer.echo("  ✅ Created database/neo4j_db.py (Neo4j Driver)")

    # Write dynamic requirements.txt file
    if requirements:
        req_file = Path("requirements.txt")
        # Join the list elements with newlines
        req_file.write_text("\n".join(requirements) + "\n")
        typer.echo("  ✅ Created requirements.txt with project dependencies")

    typer.secho("🚀 Scaffolding complete! Check your updated directory.", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()