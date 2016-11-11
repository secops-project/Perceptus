#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""log2csv.py - Converts a log file into CSV."""

import sys, argparse
import string, textwrap
import re

__author__ = "Marcelo de Souza"
__email__ = "marcelo@marcelosouza.com"
__license__ = "GPL"

#
# globals
# 
logger = ''

#
# main()
#
def main(argv):
    # parse the args
    parser = argparse.ArgumentParser(description="Parses Linux logfiles into CSVs.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent("""\
       This script expects the input log file to be a linux well-known log.

       Example: 
        $ log2csv.py -t ssh auth.log output.csv
        - Converts auth.log SSH entries into ouput.csv. 

       """))
    parser.add_argument("-t", "--type", help="Log type (options are ssh or iptables", required=True)
#    parser.add_argument("-d", "--delimiter", help="Delimiter (comma, semi-comma, pipe...).")
    parser.add_argument("infile", help="Input log file.", metavar='INFILE')
    parser.add_argument("outfile", help="Output CSV file.", metavar='OUTFILE')
    args = parser.parse_args()
    # call the converter
    #log2csv(args.infile, args.outfile, args.type, args.delimiter)
    log2csv(args.infile, args.outfile, args.type, ",")

#
# log2csv() - the dirty work goes here!
#
def log2csv(infile, outfile, log_type, delimiter_par):
    regex = ''
    if log_type == "ssh" :
        print "> Going to parse SSH entries..."
        #
        # log samples that match the regex:
        # Nov 11 09:34:08 host sshd[20239]: Invalid user support from 1.2.3.4
        # Nov 11 12:27:08 host sshd[20327]: Accepted publickey for username from 5.6.7.8 port 63553 ssh2: RSA SHA256:whatever
        #
        regex = "^(.*)\s(.*)\ssshd.*(?:(Invalid user )|(Accepted publickey) for )(\w+)\sfrom\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*"
    #elif log_type == "iptables" :
    else :
        print "> Log type not implemented yet!"
        sys.exit(2)

    try:
        print "> Reading log file '{0}'".format(infile)
        log = open(infile, 'r')
    except:
        print "> Ooops... Could not open log file"
        sys.exit(2)


#    log = open(infile, r)
    
    pattern = re.compile(regex)
    id = 1
    with open(outfile, 'w') as csv:
        # write the header
        csv.write("id,timestamp,target,action,user,source\n")
        for line in log:
            match = pattern.match(line) 
            if match :
                if match.group(3): # we have a ?   
                    csv_line = str(id) + ',' + match.group(1) + ',' + match.group(2) + ',' + 'ssh-login-denied' + ',' + match.group(5) + ',' + match.group(6)
                else :
                    csv_line = str(id) + ',' + match.group(1) + ',' + match.group(2) + ',' + 'ssh-login-accepted' + ',' + match.group(5) + ',' + match.group(6)
                csv.write(csv_line + '\n')
                id += 1

    # CODE FROM ANOTHER SCRIPT
    # # set up the CSV header array
    # header = []
    # header_str = ''
    # for n in n_cols_list:
    #     header.append(sh.cell_value(rowx=0, colx=n-1))
    # header_str = ','.join(header)

    # print "> CSV header: {0}".format(header_str)
    # #
    # # iterate and create the CSV file
    # print "> Writing CSV file '{0}'".format(outfile)
    # with open(outfile, "w") as csv_file:
    #     csv_row = {}
    #     if delimiter_par == None:
    #         delimiter_par = ','
    #     csv_writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=delimiter_par, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     csv_writer.writeheader()
    #     for row in range(1, n_total_rows):
    #         for column in n_cols_list:
    #             column_name = sh.cell_value(rowx=0, colx=column-1)
    #             # TODO - handle other cell types. See XLRD docs
    #             if sh.cell_type(rowx=row, colx=column-1) == xlrd.XL_CELL_NUMBER:
    #                 value = str(int(sh.cell_value(rowx=row, colx=column-1)))
    #                 csv_row[column_name] = value  
    #             else:
    #                 value = sh.cell_value(rowx=row, colx=column-1)
    #                 csv_row[column_name] = unidecode.unidecode(value)
    #         csv_writer.writerow(csv_row)
    #         csv_row.clear()


if __name__ == "__main__":
    main(sys.argv[1:])