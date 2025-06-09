from fastapi import FastAPI

from src.app import setup


def application() -> FastAPI:
    return setup()
