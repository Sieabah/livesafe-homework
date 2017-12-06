"""
Author: Christopher Stephen Sidell
2017, LiveSafe HW Assignment
"""
import os
import sys
import csv
import json
import argparse

if __name__ == '__main__':
  # convert.py <json file> <output folder>
  parser = argparse.ArgumentParser(
    description='Convert json to csv'
  )
  parser.add_argument(
    'jsonfile',
    type=str,
    help='File to convert to a csv'
  )
  parser.add_argument(
    'outfolder',
    type=str,
    help='Directory to place csv file'
  )

  args = parser.parse_args()

  # Read the input file
  with open(args.jsonfile) as fp:
    # Figure out what the filename is
    filename, extension = os.path.splitext(args.jsonfile)
    # Build output file name
    outfile = os.path.join(args.outfolder, '.'.join([filename, 'csv']))
    with open(outfile, 'w') as csvfile:

      # The issue with json output is parsing it may result
      # in large amounts of memory usage.
      input_data = json.load(fp)

      columns = []
      # If there is any row available figure out the columns
      # This assumes the data has some uniform output
      if len(input_data) > 0:
        for col in input_data[0]:
          columns.append(col)

      # Write the csv from the json dict
      writer = csv.DictWriter(csvfile, fieldnames=columns)
      writer.writeheader()
      for row in input_data:
        writer.writerow(row)







