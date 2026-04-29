rmdir /s /q dist

uv build
uv publish --index testpypi