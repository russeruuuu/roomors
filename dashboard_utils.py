"""Statistical summaries used by the dashboard; no model training occurs here."""
import numpy as np

def wilson_interval(canceled, bookings):
    """95% Wilson interval for an observed binomial proportion (descriptive)."""
    k, n = np.asarray(canceled, dtype=float), np.asarray(bookings, dtype=float)
    safe_n = np.where(n > 0, n, np.nan)
    p = k / safe_n
    z = 1.959963984540054
    center = (p + z*z/(2*safe_n)) / (1 + z*z/safe_n)
    half = z*np.sqrt(p*(1-p)/safe_n + z*z/(4*safe_n*safe_n))/(1+z*z/safe_n)
    return np.maximum(0, center-half), np.minimum(1, center+half)

def queue_summary(frame, capacity):
    """Rank a retrospective cohort and quantify capacity, lift and capture."""
    from math import ceil
    if frame.empty:
        return frame.copy(), dict(n=0, rate=0., baseline=0., lift=None, capture=None)
    count = max(1, ceil(len(frame)*capacity/100))
    queue = frame.sort_values('predicted_cancellation_risk', ascending=False, kind='stable').head(count)
    baseline = float(frame.is_canceled.mean())
    rate = float(queue.is_canceled.mean())
    cancellations = int(frame.is_canceled.sum())
    return queue, dict(n=count, rate=rate, baseline=baseline,
                       lift=rate/baseline if baseline else None,
                       capture=float(queue.is_canceled.sum()/cancellations) if cancellations else None)
