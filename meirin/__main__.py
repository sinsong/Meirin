import sys
import argparse
import importlib

import uvicorn
from sqlalchemy.exc import SQLAlchemyError

import meirin

from meirin.log_config import log_config
from meirin.db import engine
from meirin.server.config import settings

def run_server():
    """Run Meirin WebAPI Server
    """

    # test SQL Server
    try:
        connection = engine.connect()
        connection.close()
    except SQLAlchemyError as e:
        print(f"Database Server `{settings.DATABASE_URL}` not available", file=sys.stderr)
        exit(1)

    # default: host="127.0.0.1" port=8000
    # example: host="x.x.x.x" port=xxxx log_level="info"
    uvicorn.run(meirin.server.app,
        server_header=False,
        headers=[
            ["Server", "Meirin"]
        ],
        log_config=log_config
    )

def version():
    """Print server and dependencies version, then exit
    """
    print(f"meirin {meirin.__version__}")

    dependencies = [
        "lark",
        "sqlalchemy",
        "fastapi",
        "uvicorn",
    ]

    for dependency in dependencies:
        module = importlib.import_module(dependency)
        print(f" {module.__name__ + ':' :12} {module.__version__}")

    exit(0)

def initdb():
    """Initialize Database Schema
    """
    exit_status = 0
    try:
        from meirin.db.create_all import create_all
        create_all()
    except Exception as e:
        print(f"Exception while initdb(): {e!s}")
        exit_status = 1
    finally:
        exit(exit_status)

def enable_debug():
    print("Meirin: ENABLE debug", file=sys.stderr)
    settings.DEBUG = True
    log_config["loggers"]["root"]["level"] = "DEBUG"

def main() -> int:
    """Entry Point
    """
    parser = argparse.ArgumentParser(description="Meirin ABAC System", add_help=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-h", "--help", action="help", help="print help message")
    group.add_argument("--version", action="store_true", help="print version message")
    group.add_argument("--initdb", action="store_true", help="initialize database")

    parser.add_argument("--debug", action="store_true", help="enable debug")

    args = parser.parse_args()

    if args.version:
        version()
        # unreachable

    if args.initdb:
        initdb()
        # unreachable

    if args.debug:
        enable_debug()
    
    run_server()
    
    # maybe unreachable
    return 0

# Entry Point
if __name__ == "__main__":
    exit(main())
