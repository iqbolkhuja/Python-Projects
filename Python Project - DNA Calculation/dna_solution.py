"""
IQBOLKHOJA TEMIRKHOJAEV - CSC170
Project "DNA Identification"
"""

# Defined a function to read the DNA database from a file
def read_dna_database(file_name):
    """
    Read a DNA database from a CSV file (dna_db.csv) and return a list of records.

    Arguments:
    file_name (String): The name of the CSV file containing the DNA database.

    Returns:
    List: A list of records, where each record is a list containing the name and DNA counts.
    """
    
    dna_database = []

    file =  open(file_name, 'r')
    header = file.readline().strip().split(',')

    for line in file:
        data = line.strip().split(',')
        name = data[0]
        counts = [int(x) for x in data[1:]]
        dna_database.append([name, counts])
                 
    file.close()
                 
    return dna_database


# Defined a function to match DNA sequence with the database
def match_dna_sequence(dna_sequence, dna_database):
    """
    Match a DNA sequence with the database and return the name.

    Arguments:
    dna_sequence (String): The DNA sequence to be matched.
    dna_database (List): A list of records from the DNA database.

    Returns:
    String: The name of the matched DNA sequence or "Match not found" if no match is found.
    """
    agat_max_count = 0
    aatg_max_count = 0
    tatc_max_count = 0

    for i in range(len(dna_sequence) - 3):
        current_subsequence = dna_sequence[i:i + 4]

        if current_subsequence == 'AGAT':
            count = 1
            j = i + 4

            while j < len(dna_sequence) - 3 and dna_sequence[j:j + 4] == 'AGAT':
                count += 1
                j += 4

            agat_max_count = max(agat_max_count, count)

        elif current_subsequence == 'AATG':
            count = 1
            j = i + 4

            while j < len(dna_sequence) - 3 and dna_sequence[j:j + 4] == 'AATG':
                count += 1
                j += 4

            aatg_max_count = max(aatg_max_count, count)

        elif current_subsequence == 'TATC':
            count = 1
            j = i + 4

            while j < len(dna_sequence) - 3 and dna_sequence[j:j + 4] == 'TATC':
                count += 1
                j += 4

            tatc_max_count = max(tatc_max_count, count)

    counts = [agat_max_count, aatg_max_count, tatc_max_count]

    for record in dna_database:
        if record[1] == counts:
            return record[0]

    return "Match not found"


# the Main starting function of our second project - DNA Identification
def main():

    # Read the DNA database from a file
    dna_db = read_dna_database('dna_db.csv')

    # Ask the user for a DNA sequence file
    sequence_file_name = input("Sequence file: ")

    # Read the DNA sequence from a file
    sequence_file = open(sequence_file_name, "r") 
    dna_sequence = sequence_file.readline()
    sequence_file.close()
    
    # Match the DNA sequence with the database
    matching_result = match_dna_sequence(dna_sequence, dna_db)

    # Print the result
    if matching_result == "Match not found":
        print("No matching DNA sequence found in the database.")
    else:
        print(f"Found match: {matching_result}")

if __name__ == "__main__":
    main()
