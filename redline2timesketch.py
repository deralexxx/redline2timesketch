#!/usr/bin/python

# Copyright Alexander Jaeger
# https://github.com/deralexxx/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
import sys
import os
import csv
import datetime
import time
import traceback

# The mapping will happen:
# Alert --> Alert (extra field)
# Tag --> Tag (extra field)
# Timestamp --> timestamp
# Timestamp --> datetime
# Field --> timestamp_desc

def import_redline_file(a_input,a_output):
    try:
        redlinefile = open(a_input, 'r')
        with redlinefile,open('temp.csv', 'w') as temp_file:
            for line in redlinefile.readlines():
                # remove ugly new lines etc
                line = line.replace('\n', '')
                line = line.replace('\t', '')
                temp_file.write(line + "\n")

        #output = open("/Users/jaegeral/Documents/scripts/timesketch/vagrant/output.csv", 'w')
        output = open(a_output, 'w')

        # write the headers of the output file
        output.write("message,timestamp,datetime,timestamp_desc,tag" + "\n")
    except Exception as e:
        print traceback.format_exc()


    with open('temp.csv') as f:
        csv.register_dialect('myDialect',
                             delimiter=',',
                             quoting=csv.QUOTE_ALL,
                             skipinitialspace=True)
        reader = csv.DictReader(f, delimiter=',',dialect='myDialect')
        for row in reader:
            alert = ""
            tag = ""
            entry_unix_timestamp = ""
            entry_timestamp = ""
            field = ""
            summary = ""

            if 'Alert' in row:
                alert = row['Alert']
            else:
                print "error no alert"
            tag = row['Tag']
            entry_unix_timestamp = convert_date_to_timestamp(row['Timestamp'])
            entry_timestamp = convert_date_to_datetime(row['Timestamp'])
            field = row['Field']

            summary = clean_summary(row['Summary'])

            # for reference, this is the expected format
            #message,timestamp,datetime,timestamp_desc,extra_field_1,extra_field_2

            # this looks hacky but it works, create the line to be written in the file
            l = []
            l.append(str(summary))
            l.append(',')
            l.append(str(entry_unix_timestamp))
            l.append(',')
            l.append(str(entry_timestamp))
            l.append(',')
            l.append(str(field))
            l.append('\n')
            newline = ''.join(l)
            print newline
            output.write(newline)

    # after finished, delete the temp file
    os.remove("temp.csv")


# to avoid hickups in timesketch, some newlines, commas etc will be removed
def clean_summary(argument):
    argument = argument.replace('\n', '')
    argument = argument.replace(',', '.') # otherwise timesketch will be confused
    argument = argument.replace('\t', '')
    return argument


# method to create the datetime
def convert_date_to_datetime(argument):
    argument  = argument.replace('Z', '')
    d = datetime.datetime.strptime(argument, '%Y-%m-%d %H:%M:%S')
    iso_date = d.isoformat()
    iso_date_new = iso_date + "+00:00"
    return  iso_date_new
# helper to create the timestamp
def convert_date_to_timestamp(argument):
    argument = argument.replace('Z', '')
    d = datetime.datetime.strptime(argument, '%Y-%m-%d %H:%M:%S')
    unixtime = time.mktime(d.timetuple())
    unix_print = int(unixtime)
    unix_print = unix_print*1000
    return unix_print

def main():
    args = sys.argv[1:]

    # get the params
    input = args[0]
    output= args[1]
    try:
        import_redline_file(input,output)
    except Exception as e:
        print traceback.format_exc()
    # TODO: make argparse

    if not args:
        print('usage: [--flags options] [inputs] ')
        sys.exit(1)

# Main body
if __name__ == '__main__':
    main()