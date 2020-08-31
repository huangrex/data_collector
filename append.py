import csv
import pandas as pd 
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='fill arguement')

parser.add_argument('--num_data', type=int, required=False, default=1,
                    help='input the number to sum the data')

args = parser.parse_args()

sum = open("sum.csv", 'w')
writer = csv.writer(sum)
jump = 0
for i in range(args.num_data):
    print(str(i+1)+".csv")

    old_data = open(str(i+1)+".csv", 'r')
    rows = csv.reader(old_data)

    for j in rows:
        if(jump == 0):
            jump+=1
            continue
        jump+=1
        print(j)
        writer.writerow(j)
    
    jump = 0