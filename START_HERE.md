# Roomors: Submission Guide

## Open the dashboard

Follow README.md to install the pinned packages, then run `streamlit run app.py` from this folder. The application and its prepared results run locally. The public dashboard is available at https://roomors-group42.streamlit.app/.

## Files for the assignment

| Part | Deliverable |
|---|---|
| A: Project foundation | `paper/Roomors_Part_A.pdf` |
| B: Interactive dashboard | `app.py`, `dashboard_utils.py`, `.streamlit/`, `data/`, `results/`, and `requirements.txt` together |
| C: Advanced analytics | `Roomors_Analysis.ipynb`, with `analysis.py` as the reproducible source |
| Dataset | `data/hotel_bookings.csv` (original) and `data/hotel_bookings_analysis.csv` (analytical extract) |
| D: IEEE paper | `paper/Roomors_IEEE_Report.pdf` |
| E: Presentation preparation | `presentation/Roomors_Recording_Script_7_Minutes.pdf` and editable `.md` |

The presentation still needs to be recorded by both members, with visible faces, the official JRU background, and voice narration. Aim for 6:15-6:45, export `Enriquez_Patron_FinalProject.mp4`, and upload it to the class Google Drive folder. Check playback after uploading. Review your instructor's deadline and submission permissions yourselves.

## Demonstration route

1. Reset all filters. Explain the five indicators and hotel comparison.
2. Select Resort only, then reset. Use the segment checkboxes to select Online TA, then click All.
3. Explain the six descriptive charts. Small selected groups (under 30 records) are listed separately; they remain in KPI totals.
4. Open Prediction results, then expand Detailed model results. Discuss both the strengths and missed cancellations. Open the interactive ROC and precision-recall curves; the selected model is blue. The saved three-model comparison remains available.
5. Open Bookings to review. At 10%, explain workload, cancellation concentration, capture, and the distinction from cancellations prevented. Show 20%, then restore 10%.

## Numbers to keep consistent

- Main descriptive sample: **87,396 records; 24,025 cancellations; 27.49% canceled**.
- Test sample: **17,561 records; 4,865 cancellations; 27.70% canceled**. Its denominator differs from the full descriptive sample.
- Selected model: **logistic regression**, chosen on validation average precision.
- Test ROC-AUC **0.7180**, average precision **0.4694**, precision **54.02%**, recall **21.52%**, F1 **0.3078** at threshold **0.50**.
- Top-10% test queue: **1,757 bookings; 977 historical cancellations; 55.61% queue rate; 20.08% of cancellations captured; 2.01x concentration**.
- Better concentration is not proof that follow-up prevented cancellations or increased revenue.

## Questions to be ready for

**Why logistic regression when random forest has higher final-test ranking scores?** Selection used validation AP (0.7031 vs 0.6986). The test reports the preselected model's later performance. Switching models based on that test would require a new independent evaluation.

**Why is recall low?** At the fixed 0.50 threshold, the model identifies 1,047 and misses 3,818 test cancellations. The prototype illustrates a capacity-limited review queue rather than comprehensive cancellation detection. No test-driven threshold optimization was performed.

**Does Part A contradict the model?** No. Part A identifies group-level associations, which motivate features and questions. It does not guarantee accurate predictions for every booking.

**Why remove repeated rows?** The main sample follows the earlier EDA. Identical records are not proven duplicate reservations; raw-record sensitivity results and the resulting prevalence change are explicitly reported.

**Are the review references real reservation IDs?** No. They identify rows in the historical test extract for consistent exports. There is no connection to a live hotel reservation system.

## Verification and remaining human actions

Run `python verify.py` for the data, model-score, filter, queue, and edge-case checks. The PDFs have been compiled and visually reviewed. The notebook contains saved study outputs; the current model was not retrained or tuned during the polishing pass.

Before submission, review both authors' names and section, follow your course's rules on attribution and assistance, make the recording, and submit the required files. No grade is guaranteed, and the analytical limitations remain part of the final report.
