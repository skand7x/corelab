import os
import csv
import pyclamd


def scan_folder_with_clamav(folder_path, csv_output):
    cd = pyclamd.ClamdAgnostic()
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            scan_res = cd.scan_file(filepath)
            if scan_res:
                status = "infected"
                virus_name = scan_res[filepath][1]
            else:
                status = "clean"
                virus_name = ""
            results.append([file, status, virus_name])
    with open(csv_output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Scan Status", "Virus Name"])
        writer.writerows(results)


# Example usage:
scan_folder_with_clamav("/Aero/Uni/Sem-1/ethicalhacking/keylogger/", "report1.csv")
