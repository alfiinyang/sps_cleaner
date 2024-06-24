#!/usr/bin/env python3

import sps_cleaner as clean
import argparse

def main():
    parser = argparse.ArgumentParser(description='Clean a file or file path.')
    parser.add_argument('file_path', type=str, help='The path to the file to be cleaned')
    args = parser.parse_args()

    file, file_name, file_path = clean.file_loader(args.file_path)

    head, body = clean.data_splitter(file)

    clean_data_body = clean.data_cleaner(body)
    clean_data_body = clean.d_trimmer(clean_data_body, min_row= 70)
    head.extend(clean.deduplicator(clean_data_body))

    spsc.to_file(head, file_name, file_path)

if __name__ == '__main__':
    main()
