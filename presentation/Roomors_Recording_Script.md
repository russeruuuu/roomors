# Final Presentation Script: Roomors

**Presenters:** Job Russel Enriquez and John Cyruz Patron  
**Course and section:** Foundations of Business Analytics · BSIT-401I · Group 4.2  
**Target duration:** 6 minutes 30 seconds, including live demonstrations  
**Maximum requested duration:** 7 minutes  
**Final filename:** `Enriquez_Patron_FinalProject.mp4`

Read only the **Say** paragraphs. Follow the **On screen** steps while speaking when possible. Pause briefly when the dashboard updates. Rehearse with a timer and aim for **6:15-6:45**. Keep the final video between **5 and 7 minutes**; the script alone cannot guarantee its length.

## Before recording

- Start the local dashboard, maximize the browser, click **Reset all filters**, and open **Booking overview**. Confirm **87,396** bookings.
- Prepare screen sharing, clear microphone audio, visible faces, and the **official JRU background**, as required by the assignment. Keep each speaker visible during their section.
- Decide who controls the mouse during the handoff. Keep the script outside the shared dashboard window.

## 0:00-0:45 | Business problem and audience

**Speaker: Enriquez**

**On screen:** Show the dashboard header and KPI cards. Introduce both members with cameras visible.

**Say:**

Good day. We are Group 4.2: Job Russel Enriquez and John Cyruz Patron from BSIT-401I. Our project is called Roomors.

Canceled bookings make hotel planning harder. Managers may expect guests who never arrive, which makes room and staff planning less reliable. Roomors is for reservation and revenue managers who need to understand cancellation patterns and decide which guests to contact first.

It shows past booking patterns and estimates cancellation risk. It helps managers make decisions, but it cannot tell with certainty which guests will cancel.

## 0:45-1:25 | Dataset and main findings

**Speaker: Enriquez**

**On screen:** Point to the booking and cancellation KPIs, then the hotel comparison.

**Say:**

We use the Hotel Booking Demand dataset from two hotels in Portugal, with arrivals from July 2015 to August 2017.

We checked the original CSV and followed our earlier notebook's removal of identical rows. This leaves 87,396 records. Of these, 24,025 were canceled, or 27.49 percent.

The overall cancellation rate describes the full cleaned dataset. Later, our model results use a separate test period, so its cancellation rate is slightly different.

City Hotel has a higher cancellation rate than Resort Hotel. Online travel agency bookings also have many records and a high cancellation rate.

## 1:25-2:45 | Live dashboard demonstration

**Speaker: Enriquez**

**On screen — perform these steps while explaining:**

1. Remove **City** from **Hotel properties**, leaving **Resort**. Show **33,968 bookings** and approximately **23.5% cancellation rate**.
2. Click **Reset all filters**.
3. Expand **Booking channels**, click **Clear**, and check **Online TA**. The temporary empty-selection message after Clear is expected. Show **51,618 bookings** and approximately **35.3% cancellation rate**.
4. Click **All**, then collapse the segment panel.
5. Scroll briefly through the four remaining descriptive charts. Return to the top.

**Say:**

The Booking overview has five key measures, or KPIs, and six charts. Selecting Resort shows 33,968 bookings, with about 23.5 percent canceled. Reset brings back both hotels.

Selecting only Online TA shows 51,618 bookings, with about 35.3 percent canceled. These filters let managers compare groups. We look at both the number of bookings and the cancellation rate, because a high rate in a very small group may be less useful for planning. The arrival-period filter lets them choose a date range.

Other charts show bookings over time, days between booking and arrival, daily room rates, and monthly cancellations. Bookings made further ahead have higher cancellation rates in this data.

These Part A patterns guide our model, but do not guarantee correct predictions for each booking or prove what caused a cancellation. Booking counts are not occupied rooms, and room rates are not actual hotel earnings. John Cyruz will explain our prediction method.

## 2:45-4:20 | Advanced analytics and key results

**Speaker: Patron**

**On screen:** Open **Prediction results**. Point to the practical result cards, then expand **Detailed model results** for the scores and comparison chart. Briefly show the importance chart, then expand **ROC & precision-recall curves**. Keep the default Selected model view and point to logistic regression, the blue line. Explain while scrolling; skip the detailed evaluation table. Technical terms are kept in the spoken text where they name the actual method or metric.

**Say:**

We compared logistic regression and random forest with a simple baseline that predicts no cancellations.

Inputs include hotel, market segment, and days before arrival. We left out final booking status and details that might reveal later events.

We split bookings by date into training, validation, and test sets. Training data teaches the model. Validation data helps us choose between models. The test set checks the chosen model on later bookings. Cleaning steps were learned from training data only. Earlier bookings were used only if their outcomes were known before the next stage.

We chose logistic regression using validation average precision, before checking the test results. Its test ROC-AUC is 0.718 and average precision is 0.469. These measure risk ranking, not the percentage of correct predictions. Ranking means placing bookings that are more likely to cancel nearer the top of the list. The blue curves show how results change with different score cutoffs.

At a cutoff of 0.50, about 54 of every 100 flagged bookings canceled. But the model finds only about 22 of every 100 cancellations, so it misses most.

Random forest has better test ranking scores. We kept our original choice instead of choosing a model based on the test results.

## 4:20-5:25 | Live follow-up queue demonstration

**Speaker: Patron**

**On screen:**

1. Confirm all filters are restored and open **Bookings to review**.
2. At **10%** capacity, show **1,757 bookings**, **977 historical cancellations**, and **55.6% queue cancellation rate**.
3. Move capacity to **20%** and show **3,513 bookings to contact**.
4. Return to **10%** and point to **Export follow-up queue**. Skip the actual download to save time.

**Say:**

The queue lists test bookings from highest to lowest predicted risk. Its size depends on staff capacity, rather than the fixed score cutoff.

At ten percent capacity, it has 1,757 bookings. Of these, 977 actually canceled: a rate of 55.6 percent. That is about twice the test rate of 27.7 percent, but covers only about twenty percent of all test cancellations.

At twenty percent capacity, the list grows to 3,513 bookings. Managers can export it for review. A larger queue lets staff review more bookings, but also needs more time. Managers should choose a size their team can handle.

This shows a more focused contact list. It does not prove that calls prevent cancellations or increase earnings. Staff would not know the final outcomes when contacting guests.

## 5:25-6:30 | Limitations, recommendations, and closing

**Speaker: Patron, then Enriquez**

**On screen:** Return to **Booking overview**. Keep the speakers visible for the closing.

**Patron — Say:**

Our data is old and covers only two hotels. Some details may have changed after booking, and performance drops in the later test period. Identical rows may also be separate bookings, so we checked results with those rows kept.

We recommend trying Roomors with a small follow-up team. Staff can politely check guests' plans and booking details. A high risk score alone should not lead to a penalty or automatic cancellation.

To test whether follow-up helps, randomly assign some bookings to follow-up and others to normal service. Compare cancellations, completed stays, contact costs, and guest feedback.

**Enriquez — Say:**

To conclude, Roomors helps hotel managers understand booking patterns and decide which reservations to review first. By combining data, clear charts, and cancellation risk estimates, it supports better planning and more focused guest follow-up.

We are Group 4.2. Thank you for your time.

## Recording and submission checklist

- **Duration:** Rehearse for 6:15-6:45. The assignment allows 5-10 minutes; your requested maximum is 7 minutes.
- **Content:** State the problem and audience; demonstrate both hotel and segment filters; show model results, briefly open the restored curves, and demonstrate the capacity slider; end with recommendations.
- **Delivery:** Clear narration, readable screen, visible faces, and official JRU background.
- **File:** Export as `Enriquez_Patron_FinalProject.mp4`.
- **Submission:** Check playback, upload to the class Google Drive folder by your instructor's deadline, and check the uploaded video again.

If rehearsal exceeds 6:45, shorten the descriptive-chart scroll and skip optional explanations. Keep the two filter demonstrations, model results, recommendations, and closing. Do not rush the narration or cut the video below the assignment's five-minute minimum.
