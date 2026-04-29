rmdir /s /q dist

uv build
uv publish uv publish --index testpypi