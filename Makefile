.PHONY: run test image

run:
	streamlit run app.py

test:
	pytest

image:
	docker build -t yucacore-dashboard .
