#!/usr/bin/env python3
import pandas
import argparse
import os
def get_args():
    parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('inputTextFiles',nargs='+',help='one or more text files')
    parser.add_argument('outputXlsx',help='output filename (without extension)')
    parser.add_argument('--sep',default='\t',help='text file seperator')
    parser.add_argument('--concat',action='store_true',default=False,help='concatenate text files along index')
    return parser.parse_args()
def toDf(inputTextFiles,sep='\t',concat=False):
    dfDict={os.path.basename(inputTextFile):pandas.read_csv(inputTextFile,sep=sep)
            for inputTextFile in inputTextFiles}
    if concat:
        return {'Sheet1':pandas.concat(dfDict.values())}
    return dfDict

def toOne(dfDict,outputXlsx):
    writer=pandas.ExcelWriter(f'{outputXlsx}.xlsx',engine='xlsxwriter')  # noqa: E225,E501,E231
    for dfname,df in dfDict.items():
        df.to_excel(writer,sheet_name=dfname,index=False)
    writer.save()
if __name__ == '__main__':
    args=get_args()
    inputTextFiles=args.inputTextFiles
    outputXlsx=args.outputXlsx
    sep=args.sep
    concat=args.concat
    dfDict=toDf(inputTextFiles,sep,concat)
    toOne(dfDict,outputXlsx)
