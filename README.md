# Roomors

*Every booking tells a story.*

[Open the live dashboard](https://roomors-group42.streamlit.app/)

Group 4.2 · Job Russel Enriquez and John Cyruz Patron · BSIT-401I

A Streamlit dashboard and reproducible cancellation-classification study for Foundations of Business Analytics. You can run it locally or deploy it from GitHub to Streamlit Community Cloud. Local use requires no hosting account or API key. GitHub Pages cannot execute this Streamlit application.

For the submission file map, demonstration route, and key numbers, read **START_HERE.md**.

## Start locally

Use Python 3.9-3.12. Open a terminal inside this folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py --browser.gatherUsageStats false
```

On Windows, activate with `.venv\Scripts\activate` instead. Visit the local URL printed by Streamlit (normally http://localhost:8501). Press Ctrl+C to stop. The prepared data and results are included, so model training is not needed just to open the dashboard.

## Reproduce the study

```sh
python analysis.py
```

The source CSV is `data/hotel_bookings.csv`. The script writes the deduplicated analytical CSV, model comparisons, held-out predictions, validation permutation importance, figures, and `results/summary.json`. Training uses a fixed seed and predeclared model settings; minor numerical changes across software or hardware are possible. Results in the paper reflect the included run. The final notebook contains the same analysis code and saved outputs and can be run in Colab after uploading the source CSV.

## Dashboard

The interface uses navy and blue on neutral surfaces, system sans-serif text and monospaced KPI numerals, rounded panels, and compact macOS-inspired navigation. Booking channels use a collapsible checkbox list with All and Clear controls; Reset filters restores the full sample. Prediction results and the follow-up queue have separate views.

- Five headline KPIs, six descriptive charts, and filters for hotel, segment, and arrival dates.
- Every descriptive chart has a conclusion and decision note.
- A model tab compares a majority baseline, logistic regression, and random forest.
- Small groups (fewer than 30 selected records) appear separately from segment rankings, while remaining in KPI totals. Segment hover details include counts and descriptive Wilson intervals.
- The selected model has interactive blue ROC and precision-recall plots, and the original all-model comparison remains available.
- A queue tab ranks held-out historical bookings by the validation-selected model. A capacity slider, cohort-specific enrichment and capture, and CSV download support a demo of reservation follow-up. Extract-level review references identify historical rows, not real reservation IDs.
- Empty selections return an explanation. Evaluation metrics are fixed; sidebar filters only affect descriptive views and queue membership.

## Evaluation and limits

The original CSV has 119,390 rows; exact deduplication leaves 87,396, matching Part A. Deduplication materially changes the cancellation rate from 37.04% to 27.49%; identical rows are not proven duplicates of the same real reservation. A raw-record sensitivity analysis is included.

Creation date is inferred as arrival date minus lead time. Date boundaries are September 21, 2016 and January 28, 2017. To avoid using labels not yet known, training and validation exclude records unresolved at their next scoring origin. The resulting sets contain 45,428 / 9,924 / 17,561 rows; 14,483 unresolved earlier records are excluded from model evaluation, not from descriptive data. The extraction's arrival-window boundaries may cause selection bias, particularly for long-lead future arrivals not present in the source.

Only 15 candidate booking-time variables are used. Final status, status date, assigned room, changes, deposit, ADR, agent, prior-history measures, parking, and requests are excluded. The snapshot dataset does not prove that retained values were unchanged after booking: this remains an offline prototype, not an audited prospective test.

Logistic regression was selected on validation average precision (0.7031 vs forest 0.6986). On test, its ROC-AUC is 0.7180, AP 0.4694, precision 0.5402 and recall 0.2152 at threshold 0.50. The forest performs better on final-test ranking metrics, but the model choice is not changed after seeing the test. The top 10% selected-model queue contains 977 cancellations among 1,757 bookings (55.61%), capturing 20.08% of test cancellations at 2.01x the overall rate. These are retrospective outcomes, not cancellations prevented or revenue earned.

Run `python verify.py` for data-integrity and dashboard-interaction checks.

## Put this folder on GitHub

Create an empty repository in your GitHub account and upload this folder's contents, or clone your empty repository and copy these contents into it before committing and pushing. Do not upload `.venv`. Keep the folder layout intact. The dataset is attributed to Antonio, de Almeida, and Nunes (2019), https://doi.org/10.1016/j.dib.2018.11.126; the supplied copy originated from the Kaggle source identified in Part A. Review the source's redistribution terms when publishing a repository.

## Deliverables

- `app.py`: local dashboard (Part B).
- `analysis.py`, `Roomors_Analysis.ipynb`, `results/`: implementation and evaluation (Part C).
- `data/`: source and analytical CSVs.
- `paper/`: IEEE paper and editable source (Part D), plus the completed Part A PDF.
- To rebuild the paper with Tectonic: open `paper/ieee` and run `tectonic main.tex --outdir ..`.
- `presentation/`: timed narration and demo instructions (Part E preparation).

The required face-on-camera recording with the official JRU background must be made by the group. The project does not fabricate a recorded presentation or upload to the class Drive.

## Publish the dashboard online

Use Streamlit Community Cloud to run the dashboard from this GitHub repository. Upload the contents of this folder, preserving `data/`, `results/`, and `.streamlit/`.

Deployment settings when this folder is the repository root:

- Branch: `main`
- Main file path: `app.py`
- Python version: **3.12** (matches the pinned dependency support)
- Dependency file: `requirements.txt`
- Secrets: none required

If the repository contains this folder under `final_project/`, use `final_project/app.py` as the main file instead. Configure viewer access so your professor can open the app, then share the generated `streamlit.app` URL. The computer does not need to stay on. Verify the overview, filters, model results, and queue on the deployed app before submitting its URL.

Official deployment guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

First-time users can open **New to Roomors? Start here** for a short guide. Prediction results lead with practical cancellation detection and missed cases; detailed scores and comparisons, ROC/precision-recall curves, and evaluation methods remain available in expandable sections. Bookings to review explains team capacity and offers detailed concentration and capture results.
