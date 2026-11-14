#!/bin/bash
# Run from the project folder with the Python 3.11 environment active.
set -e
python src/build_signals.py
python src/build_labels.py
python src/build_dataset.py
python src/evaluate.py
python src/shap_stability.py
python src/grouped_cv.py
