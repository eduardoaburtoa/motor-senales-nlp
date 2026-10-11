.PHONY: verify lint test
verify:
	python src/verify_integrity.py
	python src/evaluate.py --verificar
lint:
	python -m ruff check src tests
test: verify lint
	python -m unittest discover -s tests -v
