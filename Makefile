.PHONY: test eval demo validate

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

eval:
	PYTHONPATH=src python3 evals/run.py

demo:
	PYTHONPATH=src python3 -m bilingual_tax_advisor.demo

validate:
	python3 scripts/validate_metadata.py

