

def merge_files(files_to_merge: list, output_filename: str) -> None:
    
    output = []
    for filename in files_to_merge:
        with open(filename, 'r') as f:
            output += f.readlines()
    with open(output_filename, 'w') as f:
        for i, line in enumerate(output):
            if line[-1] != '\n':
                output[i] += '\n'
        f.writelines(output)
            