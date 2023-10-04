# these two have to be in the same order
peaks = ["ATAC", "DNase", "FAIRE", "H3K4me1", "H3K4me3", "H3K27ac", "STARR", "UMI-STARR"]

# determines used in the ROC curve plot
experiment_names = ["ATAC", "DNase", "FAIRE", "H3K4me1", "H3K4me3", "H3K27ac", "STARR", "UMI-STARR"]

N_ESTIMATORS = 48
REG_WEIGHT = 0.1

# The heterochromatin and other scaffolds are pretty small
# so we won't use them
CHROMOSOMES = ["2L", "2R", "3L", "3R", "X"]

rule extract_sequences:
    input:
        peaks="input/{exp}_peaks.bed",
        genome="input/genome.fa"
    params:
        selected_chrom=" ".join(CHROMOSOMES)
    output:
        tmnt_bed="data/sequences/{exp}/tmnt.bed",
        tmnt_fa="data/sequences/{exp}/tmnt.fa",
        ctrl_bed="data/sequences/{exp}/ctrl.bed",
        ctrl_fa="data/sequences/{exp}/ctrl.fa"
    threads:
        1
    shell:
        "scripts/sample_controls --peaks-fl {input.peaks} --genome-fl {input.genome} --output-tmnt-bed {output.tmnt_bed} --output-tmnt-fasta {output.tmnt_fa} --output-ctrl-bed {output.ctrl_bed} --output-ctrl-fasta {output.ctrl_fa} --selected-chromosomes {params.selected_chrom} --window-size 501"

rule evaluate_models:
    input:
        tmnt_fa="data/sequences/{exp}/tmnt.fa",
        ctrl_fa="data/sequences/{exp}/ctrl.fa"
    params:
        reg_weight=REG_WEIGHT,
        n_estimators=N_ESTIMATORS,
        selected_chrom=" ".join(CHROMOSOMES)
    output:
        npz="data/model_predictions/{exp}.npz",
        pos_bed="data/model_predictions/{exp}_pos.bed",
        neg_bed="data/model_predictions/{exp}_neg.bed"
    threads:
        24
    shell:
        "scripts/train_and_evaluate_models --tmnt-fasta {input.tmnt_fa} --ctrl-fasta {input.ctrl_fa} --reg-weight {params.reg_weight} --predictions-fl {output.npz} --select-chrom {params.selected_chrom} --n-jobs {threads} --positive-bed-fl {output.pos_bed} --negative-bed-fl {output.neg_bed} &> {output.npz}.log"

rule plot_roc_curve:
    input:
        expand("data/model_predictions/{peak_exp}.npz", peak_exp=peaks)
    params:
        names=" ".join(experiment_names)
    output:
        "data/figures/roc_curve.png"
    threads:
        1
    shell:
        "scripts/plot_roc_curve --result-npzs {input} --experiment-names {params.names} --plot-fl {output}"
        
rule run_experiments:
    input:
        treatment_bed_fls=expand("data/sequences/{peak_exp}/tmnt.bed",
                                 peak_exp=peaks),
        pred_fls=expand("data/model_predictions/{peak_exp}.npz",
                        peak_exp=peaks),
        roc="data/figures/roc_curve.png"



