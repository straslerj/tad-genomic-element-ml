import argparse

import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 150

import pandas as pd

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input",
                        type=str,
                        required=True)

    parser.add_argument("--plot",
                        type=str,
                        required=True)

    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\\s+", names=["Chromosome", "Start", "End", "Score", "Chromosome_starr", "Start_starr", "End_starr"],
                     usecols=[0, 1, 2, 4, 5, 6, 7], header=None)

    print(len(df))

    print(df.head())

    overlap_mask = df["Start_starr"] != -1
    df_overlapping = df[overlap_mask].copy()
    print(len(df_overlapping))
    df_not_overlapping = df[~overlap_mask].sample(len(df_overlapping)).copy()

    df_overlapping["label"] = 1
    df_not_overlapping["label"] = 0

    df = pd.concat([df_overlapping, df_not_overlapping],
                   ignore_index=True)

    fpr, tpr, _ = roc_curve(df["label"], df["Score"])
    auc = roc_auc_score(df["label"], df["Score"])

    plt.plot(fpr, tpr, label="{:.1%}".format(auc))
    plt.xlabel("False Positive Rate", fontsize=16)
    plt.ylabel("True Positive Rate", fontsize=16)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.legend(fontsize=16)
    plt.savefig(args.plot)

    
