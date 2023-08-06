#!/usr/bin/env python3

from fire import Fire
from read_vme_offline.version import __version__

#print("i... module read_vme_offline/ascdf is being run")

import pandas as pd
import tables # here, to avoid a crash when writing pandas
import h5py
import datetime
import subprocess as sp
import numpy as np

import os
import datetime as dt

import matplotlib.pyplot as plt

import ROOT

import sys
# import root_numpy# 2019 is old with newer numpy



#-----------------------------------------------------
def generate_hname(filename, channel):
    """
    this will return comment with channel OR run with channel
    works with run_yyddmm_hhmmss.asc
    works with run_yyddmm_hhmmss_.asc
    works with run_yyddmm_hhmmss_comment.asc
    """
    bname = os.path.basename(filename)
    bname2 = os.path.splitext(bname)[0]  #basename

    hname = bname2.split("_")[-1]  # last thing should be a comment

    if hname.isdigit(): # NO COMMENT PRESENT NO _ PRESENT
        hname = bname2.split("_")[0]
    if len(hname) <2: #  _ PRESENT only
        hname = bname2.split("_")[0]

    hname = f"{hname}_{channel}"
    return hname


#------------------------------------------------------
def fill_hist( his, narr):

    print(f"D... filling TH  bin by bin ({narr.shape[0]}) bins")
    if len(narr.shape) == 1: # 1D
        for i in range(narr.shape[0]):
            his.SetBinContent( i, narr[i] )

    elif narr.shape[1] == 2: #  2D not tested
        for i in range(narr.shape[0]):
            for j in range(narr.shape[1]):
                his.SetBinContent( i, j, narr[i][j] )
    print("D... filling TH DONE")


#------------------------------------------------------------------------
def column_to_histo( dfcol , binmax = 32*1024, savename = "", hname = "h1"):
    """
    df["E"] for example
    df["E"].to_numpy()    np.histogram
    """
    print("D... column to_numpy")
    narr = dfcol.to_numpy()
    print("D... len=", len(narr), narr.dtype, ".. now to histo")
    his,bins = np.histogram(narr,bins=binmax,range=(0.0,binmax) )
    print("D... histo:", his)

    #
    th1f = ROOT.TH1F(hname, savename, binmax, 0 , binmax)
    #for i in range(len(his)):
    #    th1f.SetBinContent( i, his[i] )
    print("D... narr=",narr)
    print(narr.shape  ,len(narr.shape) )
    print(narr.shape[0] )
    fill_hist( th1f,  his )
    th1f.Print()

    if savename!="":
        print(f"D... creating text spectrum = {savename}")
        np.savetxt(savename, his, fmt="%d")
        # rootname = os.path.splitext(savename)[0]+".root"
        rootname = os.path.dirname(savename)
        if len(rootname)>3:
            rootname+="/"
        rootname+="all_histograms.root"
        print("D... creating root spectum at", rootname )
        f = ROOT.TFile(rootname,"UPDATE")
        print(f"D... saving {th1f.GetName()} into {rootname}")
        th1f.Write()
        f.Close()
    return his


#------------------------------------------------------------------------
def pd_detect_zeroes(df):
    """
    get number of zeroes, single zeroes, double zeroes, standalone zeroes
    2nd phase - SZ and DZ - make one event from these PILEUPs
    3rd phase - create
    """
    dfzero = df[ (df.E==0) ]
    print(f"D... zeroes {len(dfzero)} which is  {len(dfzero)/len(df)}")
    # returns length for now
    return len(dfzero)

#------------------------------------------------------------------------

def pd_read_table(filename):
    """
    two possibilities:  4 columns OR 5 columns
    """
    df = pd.read_table( filename, names=['time','E','x','ch','y'], sep = "\s+", comment="#")

    #    df.to_hdf('run'+str(number)+'.h5',
    #              "matrix",
    #              format='t',
    #              data_columns=True,
    #              mode='w')

    return df

#------------------------------------------------------------------------

def get_number_of_lines(filename):
    ps = sp.Popen( ['cat', filename], stdout=sp.PIPE)
    output = sp.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    nlines=int(output.decode("utf8").split()[0])
    return nlines

#------------------------------------------------------------------------

def get_number_of_columns(filename):
    """
    omit first 4 lines, take one line and tell
    """
    CMDL = ['head','-n','4', filename]
    ps = sp.Popen( CMDL , stdout=sp.PIPE)
    # print(" ".join(CMDL))
    output = sp.check_output(('tail','-n','1'), stdin=ps.stdout)
    ps.wait()
    ncolumns=len(output.decode("utf8").strip().split())
    if ncolumns==5:
      print(f"D... {ncolumns} cols ... 2020+ version with pile-up info")
    elif ncolumns==4:
        print(f"D... {ncolumns} cols  ... 2018 version without pileup column")
    else:
        print(f"X... BAD NUMBER OF COLUMNS {ncolumns}")
        sys.exit()
    return ncolumns

#------------------------------------------------------------------------

def filename_decomp(filename):
    """
    The ONLY procedure to get the start time from filename
    """
    # should work both with 2021mmdd and  21mmddd
    # returns the start time
    #

    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]
    # start-date
    startd = basename.split("_")[1]
    # start-time
    startt = basename.split("_")[2]

    # 4 digits always
    if len(startd)==6:
        print("D...  compensating 2 digit year to 4 digit year")
        startd="20"+startd

    print("D...  time start MARK=",startd+startt)


    #ok = False
    #try:
    start = dt.datetime.strptime(startd+startt,"%Y%m%d%H%M%S" )
    #ok = True
    print("D... succesfull start with 4 digit year")

    #except:
    #    print("x... year may not by 4 digits")
    #if not(ok):
    #    print("X... trying 2 digits for year")
    #    start = dt.datetime.strptime(startd+startt,"%y%m%d%H%M%S" )

    return start
#------------------------------------------------------------------------


def main():
    print("D... entry point of general")

if __name__=="__main__":
    print("D... fastread can be called too, from bin_readvme")
    Fire(main)
