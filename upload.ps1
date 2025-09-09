rmdir dist/
python -m build
twine upload dist/*
rmdir dist/