# Compare Two Performance Test Runs
# Compare P99
# Calculate degradation %
# Highlight APIs where degradation > 10%

from analyze_jmeter import calculate_per_sampler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


# Read input files
build1_file = sys.argv[1]   # baseline
build2_file = sys.argv[2]   # current run


# If baseline does not exist (first Jenkins run)
if not os.path.exists(build1_file):
    print("Baseline results not found.")
    print("Skipping comparison for first run.")
    sys.exit(0)


# Run analysis
build1 = calculate_per_sampler(build1_file)
build2 = calculate_per_sampler(build2_file)


# Merge on API label
comparison = pd.merge(
    build1[['label', 'P99']],
    build2[['label', 'P99']],
    on='label',
    suffixes=('_101', '_102')
)


# Calculate degradation %
comparison['Degradation_%'] = (
    (comparison['P99_102'] - comparison['P99_101'])
    / comparison['P99_101']
) * 100

comparison = comparison.round(2)


# Sort worst first
comparison = comparison.sort_values(by="Degradation_%", ascending=False)


print("\n===== Build Comparison (P99) =====\n")
print(comparison)


# Detect APIs with >10% degradation
problem_apis = comparison[comparison['Degradation_%'] > 10]

print("\n⚠ APIs with >10% degradation:\n")
for _, row in problem_apis.iterrows():
    print(f"{row['label']} shows {row['Degradation_%']}% degradation in P99")


# Save HTML report
comparison.to_html("performance_report.html", index=False)


##### Graph
labels = comparison['label']
x = np.arange(len(labels))
width = 0.35

plt.figure()

plt.bar(x - width/2, comparison['P99_101'], width, label='Baseline')
plt.bar(x + width/2, comparison['P99_102'], width, label='Current')

plt.xlabel("API Name")
plt.ylabel("P99 Response Time (ms)")
plt.title("P99 Comparison: Baseline vs Current")
plt.xticks(x, labels, rotation=45)
plt.legend()

plt.tight_layout()

# Save graph instead of showing
plt.savefig("p99_comparison.png")


# Save performance history
history_file = "performance_history.csv"

if os.path.exists(history_file):
    comparison.to_csv(history_file, mode='a', header=False, index=False)
else:
    comparison.to_csv(history_file, index=False)


# Jenkins build status
if len(problem_apis) > 0:
    print("\nPerformance regression detected")
    sys.exit(1)
else:
    print("\nPerformance OK")
    sys.exit(0)
