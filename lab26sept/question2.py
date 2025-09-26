import os
import csv
import pyclamd


def is_unusual_extension(filename, unusual_exts):
    return any(filename.lower().endswith(ext) for ext in unusual_exts)


def scan_and_detect_suspicious(folder_path, csv_output):
    cd = pyclamd.ClamdAgnostic()
    unusual_exts = [".exe", ".js"]
    size_threshold = 50 * 1024 * 1024  # 50MB
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            suspicious_reasons = []
            # 1. ClamAV scan
            scan_res = cd.scan_file(file_path)
            if scan_res:
                result = "Infected"
                suspicious_reasons.append(
                    f"Malware signature: {scan_res[file_path][1]}"
                )
            else:
                result = "Clean"
            # 2. Unusual extension
            if is_unusual_extension(file, unusual_exts):
                result = "Suspicious"
                suspicious_reasons.append(
                    f"Unusual extension: {os.path.splitext(file)[1]}"
                )
            # 3. Large unexpected file
            if os.path.getsize(file_path) > size_threshold:
                result = "Suspicious"
                suspicious_reasons.append("Large file (>50MB)")
            results.append(
                [
                    file,
                    result,
                    "; ".join(suspicious_reasons) if suspicious_reasons else "",
                ]
            )
    with open(csv_output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Scan Result", "Reason for Suspicion"])
        writer.writerows(results)


# Example usage:
# scan_and_detect_suspicious('/path/to/folder', 'report2.csv')
