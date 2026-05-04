import warnings

warnings.filterwarnings("ignore")

import typer
import questionary
import subprocess
import sys
import secrets
import shutil
import time

from context_intelligence.init_collection import run_init
from context_intelligence.config import load_config, save_config  # IMPORTANT

app = typer.Typer()
memory_app = typer.Typer()
skill_app = typer.Typer()
config_app = typer.Typer()

app.add_typer(memory_app, name="memory")
app.add_typer(skill_app, name="skill")
app.add_typer(config_app, name="config")


# ------------------------
# Dependency Handling
# ------------------------

def ensure_client_installed():
    try:
        import qdrant_client  # noqa
    except ImportError:
        print("Installing qdrant-client...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "qdrant-client[fastembed]"],
            check=True,
        )


def is_initialized():
    from context_intelligence.config import CONFIG_PATH
    import os
    return os.path.exists(CONFIG_PATH)


def mask_key(key):
    if not key:
        return "None"
    return key[:4] + "..." + key[-4:]


def require_init():
    if not is_initialized():
        print("Error: System not initialized. Please run: context-cli init")
        raise typer.Exit(1)

    config = load_config()
    status = detect_qdrant(config.get("url"), config.get("api_key"))
    if status == "needs_key_or_not_running":
        print("Error: Qdrant not reachable. Please run: context-cli init")
        raise typer.Exit(1)


def load_store():
    ensure_client_installed()

    from context_intelligence.qdrant_store import (
        get_client,
        store_memory,
        search_memory,
        store_skill,
        find_skill,
        list_skills,
        delete_memory,
        MEMORY_COLLECTIONS,
    )
    from context_intelligence.schemas import MemoryEntry, SkillEntry

    return {
        "get_client": get_client,
        "store_memory": store_memory,
        "search_memory": search_memory,
        "store_skill": store_skill,
        "find_skill": find_skill,
        "list_skills": list_skills,
        "delete_memory": delete_memory,
        "MEMORY_COLLECTIONS": MEMORY_COLLECTIONS,
        "MemoryEntry": MemoryEntry,
        "SkillEntry": SkillEntry,
    }


def get_client_instance():
    store = load_store()
    config = load_config()

    return store["get_client"](
        config.get("url", "http://localhost:6333"),
        config.get("api_key"),
    )


# ------------------------
# Utilities
# ------------------------

def run_command(command: str):
    try:
        print(f"\nRunning: {command}\n")
        subprocess.run(command, shell=True, check=True)
        print("\nDone!")
    except subprocess.CalledProcessError:
        print("\nCommand failed")


def generate_api_key():
    return secrets.token_urlsafe(32)


def run_qdrant(api_key: str):
    command = (
        f"docker run -d "
        f"--name qdrant "
        f"-p 6333:6333 "
        f"-v qdrant_data:/qdrant/storage "
        f"-e QDRANT__SERVICE__API_KEY={api_key} "
        f"qdrant/qdrant"
    )
    run_command(command)


def preload_embeddings():
    print("Preparing embedding model (first-time setup)...")
    from context_intelligence.embeddings import get_model
    get_model()
    print("Embedding model ready")


# ------------------------
# Detection
# ------------------------

def detect_qdrant(url="http://localhost:6333", api_key=None):
    ensure_client_installed()
    from qdrant_client import QdrantClient

    try:
        client = QdrantClient(url=url, api_key=api_key)
        client.get_collections()
        return "ok"
    except Exception:
        return "needs_key_or_not_running"


def handle_existing_qdrant():
    url = "http://localhost:6333"
    status = detect_qdrant(url)

    if status == "no_auth":
        print("Qdrant running (no API key)")
        return url, None

    print("Qdrant needs API key or is not reachable")

    choice = questionary.select(
        "What do you want to do?",
        choices=[
            "Enter API key",
            "Restart with new key",
            "Use custom URL",
            "Cancel",
        ],
    ).ask()

    if choice == "Enter API key":
        return url, questionary.password("API key:").ask()

    elif choice == "Restart with new key":
        api = generate_api_key()
        print(f"\nNew API Key:\n{api}\n")

        run_command("docker rm -f qdrant")
        run_qdrant(api)

        return url, api

    elif choice == "Use custom URL":
        url = questionary.text("URL:").ask()
        api = questionary.password("API key:").ask()
        return url, api

    else:
        raise typer.Exit()


# ------------------------
# DB Init
# ------------------------

def init_db(url, api):
    if not questionary.confirm("Initialize collections?").ask():
        return

    ensure_client_installed()

    for _ in range(6):
        try:
            run_init(url, api)
            print("Collections ready")
            break
        except Exception:
            print("Waiting for Qdrant...")
            time.sleep(2)

    # preload AFTER success
    preload_embeddings()

    # Save config
    save_config({
        "url": url,
        "api_key": api
    })


# ------------------------
# Install Flow
# ------------------------

def install_qdrant():
    choice = questionary.select(
        "Setup type:",
        choices=["Docker", "Cloud", "Back"],
    ).ask()

    if choice == "Docker":
        if not shutil.which("docker"):
            print("Docker not installed")
            return

        api = generate_api_key()
        print(f"\nAPI Key:\n{api}\n")

        if not questionary.confirm("Start container?").ask():
            return

        run_qdrant(api)
        init_db("http://localhost:6333", api)

    elif choice == "Cloud":
        url = questionary.text("URL:").ask()
        api = questionary.password("API key:").ask()
        init_db(url, api)


# ------------------------
# Commands
# ------------------------

@app.command()
def init():
    if is_initialized():
        config = load_config()
        print(f"Existing setup detected")
        print(f"URL: {config.get('url')}")
        print(f"API Key: {mask_key(config.get('api_key'))}\n")

        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Use existing setup",
                "Reinitialize collections",
                "Change configuration",
                "Reset everything",
                "Exit",
            ],
        ).ask()

        if choice == "Use existing setup":
            print("Nothing to do")
            return

        elif choice == "Reinitialize collections":
            init_db(config["url"], config.get("api_key"))
            return

        elif choice == "Change configuration":
            url = questionary.text("Enter new URL:").ask()
            api = questionary.password("Enter API key:").ask()

            save_config({
                "url": url,
                "api_key": api,
            })

            print("Config updated")
            return

        elif choice == "Reset everything":
            confirm = questionary.confirm("This will overwrite config. Continue?").ask()
            if not confirm:
                return

            install_qdrant()
            return

        else:
            raise typer.Exit()

    # First-time setup
    choice = questionary.select(
        "Do you already have Qdrant running?",
        choices=["Yes", "No", "Exit"],
    ).ask()

    if choice == "Yes":
        url, api = handle_existing_qdrant()
        init_db(url, api)

    elif choice == "No":
        install_qdrant()

    else:
        raise typer.Exit()


@app.command()
def status():
    """Show current context intelligence status."""
    if not is_initialized():
        print("Status: Not initialized")
        print("Run 'context-cli init' to set up.")
        return

    config = load_config()
    print("Status: Initialized")
    print(f"Qdrant URL: {config.get('url')}")
    print(f"API Key: {mask_key(config.get('api_key'))}")

    qdrant_status = detect_qdrant(config.get("url"), config.get("api_key"))
    if qdrant_status == "ok":
        print("Qdrant: Reachable")
        try:
            client = get_client_instance()
            collections = client.get_collections().collections
            if collections:
                print("Collections:")
                for col in collections:
                    print(f"  - {col.name}")
            else:
                print("Collections: None")
        except Exception as e:
            print(f"Qdrant Error: {e}")
    else:
        print("Qdrant: Not reachable")


# ------------------------
# MEMORY
# ------------------------

@memory_app.command("add")
def add_memory(content: str, domain: str, type: str = "note"):
    require_init()
    store = load_store()

    # accept both formats
    if domain.startswith("memory_"):
        collection = domain
    else:
        collection = f"memory_{domain}"

    if collection not in store["MEMORY_COLLECTIONS"]:
        typer.echo("Invalid domain")
        raise typer.Exit()

    entry = store["MemoryEntry"](content=content, type=type)

    client = get_client_instance()
    point_id = store["store_memory"](client, collection, entry)

    typer.echo(f"Stored: {point_id}")


@memory_app.command("search")
def search_memory_cmd(query: str, domain: str):
    require_init()
    store = load_store()

    if domain.startswith("memory_"):
        collection = domain
    else:
        collection = f"memory_{domain}"

    client = get_client_instance()
    results = store["search_memory"](client, collection, query)

    for r in results:
        typer.echo(f"\n{r['content']} (score: {r['score']})")


# ------------------------
# CONFIG COMMANDS
# ------------------------

@config_app.command("show")
def show_config():
    config = load_config()
    if "api_key" in config:
        config["api_key"] = mask_key(config["api_key"])
    typer.echo(config)


@config_app.command("set-key")
def set_key(api_key: str):
    config = load_config()
    config["api_key"] = api_key
    save_config(config)
    print("API key saved")


@config_app.command("set-url")
def set_url(url: str):
    config = load_config()
    config["url"] = url
    save_config(config)
    print("URL saved")


# ------------------------

if __name__ == "__main__":
    app()

