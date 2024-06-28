#!/usr/bin/env python3

import ukooa_cleaner as ukc
import argparse

def main():
    parser = argparse.ArgumentParser(description='Clean a 3D marine UKOOA file.')
    parser.add_argument('file_path', type=str, help='The path to the file to be cleaned')
    args = parser.parse_args()

    file, file_name, file_path = ukc.file_loader(args.file_path)

    head, body = ukc.data_splitter(file)

    clean_data_body = ukc.data_cleaner(body)
    clean_data_body = ukc.d_trimmer(clean_data_body, min_row= 70)
    head.extend(ukc.deduplicator(clean_data_body))

    ukc.to_file(head, file_name, file_path)

if __name__ == '__main__':
    main()
