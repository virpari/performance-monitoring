# Groups by label (sampler name)
# Calculates:Average,P95,P99,Error %,Total requests
# Sorts slowest APIs first

import pandas as pd
import numpy as np


def calculate_per_sampler(file_path):

    df = pd.read_csv(file_path)

    # Convert numeric columns
    df['elapsed'] = pd.to_numeric(df['elapsed'], errors='coerce')
    df['success'] = df['success'].astype(str)

    grouped = df.groupby('label')

    results = []

    for sampler, data in grouped:

        avg = data['elapsed'].mean()
        p95 = np.percentile(data['elapsed'].dropna(), 95)
        p99 = np.percentile(data['elapsed'].dropna(), 99)

        total = len(data)
        failures = len(data[data['success'] == 'false'])
        error_pct = (failures / total) * 100 if total > 0 else 0

        results.append({
            "label": sampler,
            "Avg": round(avg, 2),
            "P95": round(p95, 2),
            "P99": round(p99, 2),
            "Error_%": round(error_pct, 2),
            "Total_Requests": total
        })

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(by="P99", ascending=False)

    return result_df