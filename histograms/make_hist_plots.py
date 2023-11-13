import os

import matplotlib.pyplot as plt
import pandas as pd

file_path = "dataset_evaluation/input/tad_classification.bed"

df = pd.read_csv(
    file_path,
    sep="\t",
    header=None,
    names=["Label", "Start", "End", "Status", "Score", "Dot", "Start2", "End2", "RGB"],
)

df["Length"] = df["End"] - df["Start"]

# INDIVIDUAL GENOMES
grouped = df.groupby("Label")

fig, axes = plt.subplots(nrows=len(grouped), ncols=1, figsize=(10, 5 * len(grouped)))

for (key, group), ax in zip(grouped, axes.flatten()):
    group["Length"].plot(kind="hist", ax=ax, bins=30, title=f"Lengths of {key} Genomes")
    ax.set_xlabel("Length")
    ax.set_ylabel("Frequency")


histograms_dir = "histograms"
os.makedirs(histograms_dir, exist_ok=True)

for key, group in grouped:
    fig, ax = plt.subplots(figsize=(10, 8))
    group["Length"].plot(kind="hist", ax=ax, bins=30, title=f"Lengths of {key} Genomes")
    ax.set_xlabel("Length")
    ax.set_ylabel("Frequency")
    histogram_path = os.path.join(histograms_dir, f"{key}_genome_lengths_histogram.png")
    fig.savefig(histogram_path)
    plt.close(fig)

# ALL GENOMES
fig, ax = plt.subplots(figsize=(10, 8))
df["Length"].plot(kind="hist", ax=ax, bins=30, title="Lengths of All Genomes")
ax.set_xlabel("Length")
ax.set_ylabel("Frequency")

all_genomes_histogram_path = os.path.join(
    histograms_dir, "all_genomes_lengths_histogram.png"
)
fig.savefig(all_genomes_histogram_path)
plt.close(fig)
