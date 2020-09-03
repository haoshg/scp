#!/usr/bin/env python3
import argparse
import collections
import pandas as pd
import pathlib
import itertools
def getargs():
    parser=argparse.ArgumentParser()
    parser.add_argument('input',nargs='+')
    parser.add_argument('sheet_name',help='comma-separated list of sheet names')
    parser.add_argument('output')
    return parser.parse_args()
if __name__=='__main__':
    args=getargs()
    fileList=args.input
    sheetNames=args.sheet_name.split(',')
    output=args.output
    d=collections.defaultdict(list)
    # a=itertools.product(fileList,sheetNames)
    # print([x for x in a])
    # exit()
    for f,sn in itertools.product(fileList,sheetNames):
        fp=pathlib.Path(f)
        df=pd.read_excel(fp,sheet_name=sn)
        df.insert(0,'FileIdentifier',fp.stem)
        d[sn].append(df)

    writer=pd.ExcelWriter(output,engine='xlsxwriter')
    for k,v in d.items():
        pd.concat(v).to_excel(writer,sheet_name=k,index=False)
    writer.save()
