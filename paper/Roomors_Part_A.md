# Part A: Project Foundation
## Roomors: Hotel Booking Analytics and Cancellation Risk Prioritization

**Course:** ITC C307 - Foundations of Business Analytics  
**Prepared by:** Group 4.2 - Job Russel Enriquez and John Cyruz Patron  
**Program:** BSIT - 401I

## Dataset and Analytical Basis

We use the Hotel Booking Demand dataset introduced in our earlier Google Colab notebook. The original dataset contains 119,390 records and 32 variables for a City Hotel and a Resort Hotel in Portugal. Arrival dates cover July 2015 to August 2017. Our notebook removes 31,994 exact duplicate rows, leaving 87,396 records for EDA. It renames `adr` to `average_daily_rate`, converts the arrival month and reservation-status date to suitable types, fills missing children with 0, missing country with “Unknown,” and missing agent with 0, and drops the highly incomplete `company` column. It also creates total nights, total guests, and a family indicator.

The findings were initially taken from the earlier notebook's saved EDA outputs and have since been checked against the supplied source CSV and the reproducible final-project analysis. Cancellation rate means canceled records divided by all records in the stated group, multiplied by 100. These findings apply to the notebook's deduplicated sample; identical records can potentially represent separate bookings, so the effect of deduplication should be reviewed before operational use.

## Findings Summary

### Five Key Findings

1. **Cancellations affect more than one in four recorded bookings.** Of 87,396 analyzed records, 24,025 were canceled (27.49%), while 63,371 were not canceled (72.51%). This establishes a baseline for examining cancellation exposure and supports giving cancellation rate a prominent place in the planned dashboard.

**Table 1. Overall booking outcomes**

| Booking outcome | Records | Share of analyzed bookings |
|---|---:|---:|
| Not canceled | 63,371 | 72.51% |
| Canceled | 24,025 | 27.49% |
| **Total** | **87,396** | **100.00%** |

*Source: notebook cells 74 and 78.*

2. **City Hotel has a higher cancellation rate than Resort Hotel.** City Hotel recorded 16,049 cancellations among 53,428 bookings (30.04%), compared with 7,976 among 33,968 bookings at Resort Hotel (23.48%). The gap is approximately 6.56 percentage points. Managers should compare the properties separately and examine whether their different booking mixes help explain the gap.

**Table 2. Booking volume and cancellation rate by hotel**

| Hotel | Bookings | Booking share | Canceled | Not canceled | Cancellation rate |
|---|---:|---:|---:|---:|---:|
| City Hotel | 53,428 | 61.13% | 16,049 | 37,379 | 30.04% |
| Resort Hotel | 33,968 | 38.87% | 7,976 | 25,992 | 23.48% |
| **Total** | **87,396** | **100.00%** | **24,025** | **63,371** | **27.49%** |

*Source: notebook cells 74 and 78. The hotel cancellation-rate gap is approximately 6.56 percentage points.*

3. **Online travel agency bookings combine substantial volume with a high cancellation rate.** Online TA accounts for 51,618 bookings (59.06% of the sample), including 18,245 cancellations (35.35%). Direct bookings have 1,737 cancellations among 11,804 bookings (14.72%), while Corporate has 510 among 4,212 (12.11%). Online TA has the highest cancellation rate among named market segments and is a useful priority for closer monitoring. The Undefined segment is excluded from this ranking because it contains only two bookings, both canceled.

**Table 3. Cancellation rates across market segments**

| Market segment | Bookings | Canceled | Cancellation rate |
|---|---:|---:|---:|
| Online TA | 51,618 | 18,245 | 35.35% |
| Groups | 4,942 | 1,335 | 27.01% |
| Aviation | 227 | 45 | 19.82% |
| Offline TA/TO | 13,889 | 2,063 | 14.85% |
| Direct | 11,804 | 1,737 | 14.72% |
| Complementary | 702 | 88 | 12.54% |
| Corporate | 4,212 | 510 | 12.11% |
| Undefined (reported separately) | 2 | 2 | 100.00% |
| **Total** | **87,396** | **24,025** | **27.49%** |

*Source: notebook cells 74 and 78. Named segments are ordered by cancellation rate. TA means travel agency; TO means tour operator. Undefined is not included in the risk ranking because its two-record sample is too small for a reliable comparison.*

4. **Longer booking lead times are associated with higher cancellation rates.** The cancellation rate is 8.43% for bookings made 0-7 days before arrival (18,304 records), 32.01% for 31-90 days (22,744 records), and 39.68% for 181-365 days (11,200 records). It reaches 40.89% beyond 365 days, although that group has only 565 records. Lead time also has a modest positive Pearson correlation with cancellation (r = 0.185). These results justify examining advance-booking risk, but they do not establish causation or demonstrate model accuracy.

**Table 4. Cancellation rate by booking lead time**

| Lead time before arrival | Bookings | Cancellation rate |
|---|---:|---:|
| 0-7 days | 18,304 | 8.43% |
| 8-30 days | 16,340 | 25.37% |
| 31-90 days | 22,744 | 32.01% |
| 91-180 days | 18,243 | 34.98% |
| 181-365 days | 11,200 | 39.68% |
| Over 365 days | 565 | 40.89% |
| **Total** | **87,396** | **27.49%** |

*Source: notebook cell 79. The over-365-day group has substantially fewer records than other groups. The Pearson correlation between lead time and cancellation is approximately +0.185 (cell 95); this is an association, not a causal effect.*

5. **Booking notice is strongly skewed, so its average overstates the typical lead time.** Mean lead time is 79.89 days, compared with a median of 49 days. The middle half of bookings falls between 11 and 125 days (IQR = 114 days), and skewness is 1.43. The dashboard should therefore show median lead time alongside cancellation rates and practical lead-time groups.

### Three Supporting Findings

6. **City Hotel contributes most of the analyzed booking volume.** Its 53,428 records represent 61.13% of the sample, while Resort Hotel contributes 33,968 (38.87%). Overall results are therefore influenced more heavily by City Hotel, making a hotel filter and within-hotel rates necessary for fair comparison.

7. **August has the largest pooled arrival-booking count.** It contains 11,257 records (12.88%), followed by July with 10,057 (11.51%). These totals support examining demand by arrival month, but they do not measure occupancy. July and August each appear in three observed years, while other months appear in only two; unequal coverage prevents treating the pooled ranking as proof of seasonality.

**Table 5. Pooled booking volume by arrival month**

| Arrival month | Bookings | Share of analyzed bookings | Observed years containing this month |
|---|---:|---:|---:|
| January | 4,693 | 5.37% | 2 |
| February | 6,098 | 6.98% | 2 |
| March | 7,513 | 8.60% | 2 |
| April | 7,908 | 9.05% | 2 |
| May | 8,355 | 9.56% | 2 |
| June | 7,765 | 8.88% | 2 |
| July | 10,057 | 11.51% | 3 |
| August | 11,257 | 12.88% | 3 |
| September | 6,690 | 7.65% | 2 |
| October | 6,934 | 7.93% | 2 |
| November | 4,995 | 5.72% | 2 |
| December | 5,131 | 5.87% | 2 |
| **Total** | **87,396** | **100.00%** | **July 2015-August 2017** |

*Source: notebook cell 74; calendar coverage is verified against cell 92. Monthly percentages may not sum to exactly 100% because of rounding. Unequal calendar coverage means these pooled totals cannot establish seasonality or occupancy.*

8. **Daily rates contain substantial extremes.** The mean average daily rate is 106.34, compared with a median of 98.10; the middle half lies between 72 and 134. Recorded values range from -6.38 to 5,400, with skewness of 10.92. These results support reporting median and IQR and reviewing unusual rates before using them in financial estimates. Canceled bookings and their recorded rates alone cannot establish actual lost revenue.

**Table 6. Numerical summaries for lead time and daily rate**

| Measure | Lead time (days) | Average daily rate (dataset units) |
|---|---:|---:|
| Mean | 79.89 | 106.34 |
| Median | 49.00 | 98.10 |
| First quartile (Q1) | 11.00 | 72.00 |
| Third quartile (Q3) | 125.00 | 134.00 |
| Interquartile range (IQR) | 114.00 | 62.00 |
| Minimum | 0.00 | -6.38 |
| Maximum | 737.00 | 5,400.00 |
| Skewness | 1.43 | 10.92 |

*Source: notebook cells 66, 67, 70, and 71. Rate units are retained as reported in the notebook. Extreme values remain in these summaries and require review before financial interpretation.*

## Problem Statement

Our project addresses the business question: **How can reservation and revenue managers at the two hotels identify booking groups with elevated cancellation risk and prioritize reservation follow-up before arrival?** In the analyzed sample, 24,025 of 87,396 bookings were canceled (27.49%), with higher rates at City Hotel, in the Online TA segment, and among bookings made further in advance. We will use an interactive dashboard to compare booking counts and cancellation rates by hotel, market segment, arrival period, and lead-time group, then develop and evaluate a classification model that estimates cancellation risk using information available when a booking is made. The analysis will support decisions about which reservations warrant earlier confirmation and closer monitoring. Success will be assessed through held-out precision, recall, F1, and ROC-AUC against a baseline, together with the observed cancellation rate and number of bookings in prioritized risk groups; any actual reduction in cancellations or financial benefit will require a later operational evaluation.

## Intended Dashboard Audience and Decisions

The primary audience is the **reservation and revenue managers of City Hotel and Resort Hotel**. They need to identify groups with high cancellation exposure, compare each hotel's booking mix, and prioritize confirmation and follow-up activity. The planned dashboard will support comparisons by hotel, market segment, arrival period, and lead-time group, always showing booking counts alongside cancellation percentages.

## Chosen Advanced Analytics Type

We propose **predictive analytics through binary classification**, using `is_canceled` as the target (1 = canceled; 0 = not canceled). This choice follows the observed differences across hotels, market segments, and lead-time groups. Logistic regression and a random forest are proposed for comparison against a majority-class baseline. Classification directly addresses reservation-level prioritization; forecasting would instead focus on future aggregate demand.

Candidate predictors include hotel, lead time, market segment, planned arrival details, reserved room type, and planned stay length, subject to confirming their availability at booking time. Final reservation status and its date must be excluded because they reveal the outcome. Assigned room type, booking changes, and other fields that may change after booking require an availability review. Existing scaled EDA columns will not be reused for evaluation: preprocessing must be fitted only on the training data. Model development and dashboard construction belong to later project parts and are not completed here.

## Evidence and Limitations

The numerical evidence is traceable to the supplied notebook: duplicate handling (cell 46), missing-value handling (cell 48), central tendency and dispersion (cells 66-71), frequency tables (cell 74), cancellation cross-tabulations (cell 78), lead-time comparisons (cell 79), arrival coverage (cell 92), and correlations (cell 95). Cell numbers here use the notebook's zero-based cell order, not execution counts.

The dataset source and hotel context follow the supplied notebook's description. Findings are historical, observational, and limited to two properties. Missing-value assumptions, deduplication, small groups, unusual prices, and incomplete calendar years should be considered when interpreting results. The source CSV was subsequently available and the main counts and summaries were recomputed. The final model pipeline fits imputation, scaling, and encoding on training data only; it does not reuse globally transformed EDA columns. The original EDA cleaning decisions are documented above for continuity. The final analytical CSV retains original fields and missing values for reproducible split-specific preprocessing.
