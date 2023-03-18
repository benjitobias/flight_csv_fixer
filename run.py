import os
import csv
import argparse

BAD_COLUMNS =  ['E2 CHT1', 'E2 CHT2', 'E2 CHT3', 'E2 CHT4', 'E2 CHT5', 'E2 CHT6']

def parse_csv(f_path, csv_writer):
    bad_indexes = []
    try:
        with open(f_path) as csvfile:
            reader = csv.reader(csvfile)
            line_number = 0
            for row in reader: # row
                line_number += 1            
                if len(bad_indexes) < 1:
                    #print("[*] Finding bad columns")
                    for index, column in enumerate(row): # column
                        for bad_c in BAD_COLUMNS:
                            if bad_c in column:
                                bad_indexes.append(index)
                    #print("[*] Bad columns: ", bad_indexes)
                else:
                    #print(f"========= LINE {line_number} BEFORE ==========")
                    #print(row)
                    for index in bad_indexes:
                        try:
                            row[index] = ''
                        except IndexError as e:
                     #       print(f"[!] Couldn't replace line: {line_number}. Finished maybe?")
                            pass
                    #print(f"========= LINE {line_number} AFTER ============")
                    #print(row)
                csv_writer.writerow(row)
            #print("[*] Done")
            return True
    except UnicodeDecodeError:
        print(f"[!] Error with file: {f_path}")
        return False


def parse_all_files_in_path(input_dir, output_dir):
    problem_files = []
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass
    for d, _, files in os.walk(input_dir):
        for f in files:
            f_path = os.path.join(d, f)
            o_path = os.path.join(output_dir, f)
            with open(o_path, 'w') as csvfile:
                writer = csv.writer(csvfile)
                if not parse_csv(f_path, writer):
                    problem_files.append(f_path)
        print("[*] Done")
        with open("error.log", "w") as e:            
            for b in problem_files:
                print(f"[!] Encountered error in file: {b}")
            e.writelines(problem_files)

def main(input_dir, output_dir):
    parse_all_files_in_path(input_dir, output_dir)
    #with open("tt/log_200417_091301_EGBJ.csv", "w") as f:
    #    writer = csv.writer(f)
    #    parse_csv("files/log_200417_091301_EGBJ.csv", writer)


if __name__ == '__main__':
    output_dir = None
    input_dir = None
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-dir", dest=input_dir)
    parser.add_argument("-o", "--output-dir", dest=output_dir)
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
