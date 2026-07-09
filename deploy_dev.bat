@echo off
rmdir /s /q dist

uv build
uv run --no-project publish.py testpypi