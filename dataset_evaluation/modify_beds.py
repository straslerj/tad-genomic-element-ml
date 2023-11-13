from tqdm import tqdm

BP_SIZE = 1001
BP_ADJUSTMENT = int((BP_SIZE / 2) + 1)


def process_bed_file(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        total_lines = sum(1 for line in open(input_file))

        progress_bar = tqdm(
            total=total_lines, desc="Processing BED file", unit=" lines"
        )

        for line in infile:
            columns = line.strip().split("\t")

            chrom = columns[0]
            start = int(columns[1])
            end = int(columns[2])

            new_start = start - BP_ADJUSTMENT
            new_end = start + BP_ADJUSTMENT
            new_start2 = end - BP_ADJUSTMENT
            new_end2 = end + BP_ADJUSTMENT

            outfile.write(
                "\t".join([chrom, str(new_start), str(new_end)] + columns[3:]) + "\n"
            )

            outfile.write(
                "\t".join([chrom, str(new_start2), str(new_end2)] + columns[3:]) + "\n"
            )

            progress_bar.update(1)

        progress_bar.close()


input_bed_file = "input/tad_classification.bed"
output_bed_file = f"input/{BP_SIZE}_tad_classification.bed"
process_bed_file(input_bed_file, output_bed_file)
