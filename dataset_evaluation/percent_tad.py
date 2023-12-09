def calculate_genome_length(genome_file):
    total_length = 0
    with open(genome_file, "r") as file:
        for line in file:
            _, start, end, _, _ = line.split("\t")
            total_length += int(end) - int(start)
    return total_length


def calculate_tad_length(tad_file):
    total_length = 0
    with open(tad_file, "r") as file:
        for line in file:
            _, start, end, _, _, _, _, _, _ = line.split("\t")
            total_length += int(end) - int(start)
    return total_length


def calculate_percentage(genome_length, tad_length):
    percentage = (tad_length / genome_length) * 100
    return percentage


genome_file_path = "input/dm3.fa.fai"
tad_file_path = "input/tad_classification.bed"

genome_length = calculate_genome_length(genome_file_path)
tad_length = calculate_tad_length(tad_file_path)

percentage_in_tad = calculate_percentage(genome_length, tad_length)

print(f"Percent TAD: {percentage_in_tad:.2f}%")
