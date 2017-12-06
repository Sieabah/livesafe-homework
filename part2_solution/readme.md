## How to Execute (Runs on Python 3):

    python convert.py (json file) (output folder)

Example:

    python convert.py employeelist.json .

## Notes
The main issues not handled are super large json files and if the titles are not consistent.

#### **Large files**
Large json files are hard to parse due to the nature of having to pull in the entire object to make sure it's parsed correctly. This can be remedied if the output of json can be predictable or at least somewhat parsable by line *or* with consistent output.

If the output is random or a generic tool is needed this would suffice.

#### **Inconsistent Titles**
The way this tool is made is it checks the first entry for the titles it expects to be in the csv. If each entry has different values or some entries have an extra column it won't show up in the header row.

# Prompt
## Premise:

Different software works with data is different formats. Here you are given an employee file in a json format, but unfortunately the integration you have been tasked with only works with CSV format. Given the input “employeelist.json” create a script to parse and reformat the file into CSV format.

## Goal

The goal of this assignment is to be able to run a script that reads from employeelist.json and outputs to a csv file

