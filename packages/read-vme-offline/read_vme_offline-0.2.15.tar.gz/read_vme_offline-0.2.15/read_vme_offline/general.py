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

import psutil

import datetime as dt

#================ OPERATIONS ON NAMES, INFO ON COLS ROWS
#------------------------------------------------------------------------

def freemem():
    a = psutil.virtual_memory()
    return f"D... AVAIL MEM: {a.available/1024/1024/1024:.2f} GB  ...  used: {a.percent} %"

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

def get_number_of_lines(filename):
    """
    wc to count the lines of ASC
    """
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
      print(f"D... {ncolumns} cols ... 2020+ version with pile-up info (1/0)")
    elif ncolumns==4:
        print(f"D... {ncolumns} cols  ... 2018 version without extras column, pileup (3/0)")
    else:
        print(f"X... BAD NUMBER OF COLUMNS {ncolumns}")
        sys.exit()
    return ncolumns



#-----------------------------------------------------
def generate_hname(filename, channel):
    """
    create histogram name for ROOT TH
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


#=============================== CREATE HISTO, TREE

#------------------------------------------------------
def fill_hist( his, narr):
    """
    FILL histogram from np.histogram data.
    simple way bin by bin
    """
    #print(f"D... filling TH  bin by bin ({narr.shape[0]}) bins")
    if len(narr.shape) == 1: # 1D
        for i in range(narr.shape[0]):
            #if narr.shape[0]<6:
            #    print(i, narr[i], "  ", end=";")
            # we start with 0, bin starts with 1 in ROOT
            his.SetBinContent( i+1, narr[i] )

    elif narr.shape[1] == 2: #  2D not tested
        for i in range(narr.shape[0]):
            for j in range(narr.shape[1]):
                his.SetBinContent( i+1, j+1, narr[i][j] )
    #print("D... filling TH DONE")


#------------------------------------------------------------------------
def column_to_histo( dfcol , binmax = 32*1024, himax=32*1024, savename = "", hname = "h1", writeondisk = False , writetxt = True):
    """
    send df["E"] for example
    - converts to numpy array; creates HIST;
    - saves txt
    - updates allhist.root too
    """
    print("D... ========= creating histo ======= column to_numpy; bins=", binmax)
    narr = dfcol.to_numpy()
    print("D... len=", len(narr), narr.dtype, "...  ndarray to np histo")
    #print(dfcol)
    #print(narr)
    his,bins = np.histogram(narr,bins=binmax,range=(0.0,himax) )
    #    print("D... histo:", his)
    #    print("D... bins :", bins)
    del narr

    #
    basename = os.path.basename(savename) # title without path...

    th1f = ROOT.TH1F(hname, basename, binmax, 0 , himax)
    #for i in range(len(his)):
    #    th1f.SetBinContent( i, his[i] )
    #print("D... narr=",narr)

    #print(narr.shape  ,len(narr.shape) )
    #print(narr.shape[0] )
    fill_hist( th1f,  his )
    #th1f.Print()

    if (savename!="") and  writeondisk:
        if writetxt:
            print(f"D...          text spectrum = {savename}")
            np.savetxt(savename, his, fmt="%d")
        # rootname = os.path.splitext(savename)[0]+".root"
        rootname = os.path.dirname(savename)
        if len(rootname)>3:
            rootname+="/"
        rootname+="all_histograms.root"
        print("D...          root spectum at", rootname, "name=", hname )
        f = ROOT.TFile(rootname,"UPDATE")
        # print(f"D...          {th1f.GetName():13s} @ {rootname}")
        th1f.Write()
        f.Close()
    endblock(nomem=True)
    return his


#------------------------------------------------------------------------

def save_to_tree(df2, filename, modname=""):
    print("i... ===============creating and writing tree, expect 25% of the original size")
    # convert to dict with numpy arrays
    #data = {key: df[key].values for key in ['time', 'E', 'x']}
    data = {key: df2[key].values for key in df2.columns }
    print("D... columns that go to TTree:", df2.columns)
    rdf = ROOT.RDF.MakeNumpyDataFrame( data )
    print(rdf)
    outfile =  os.path.splitext(filename)[0] +f"_tree{modname}.root"
    print("D...  snaphost rdf as TTREE to ", outfile)

    start = dt.datetime.now()
    rdf.Snapshot("df",outfile)
    meastime = (dt.datetime.now() - start).total_seconds()
    print(f"D... speed = {get_number_of_lines(filename)/meastime/1000/1000:.3f} Mrows/sec")

    return

#========================== READ; ANALYSIS AND DETECTION ===================


def endblock(nomem=False):
    if not nomem:
        print( freemem() )
    print("D... ","_"*50)

#------------------------------------------------------------------------
def select_channels(df, channels, delete_original = False):
    """
    select channels bu not as view! COPY and DELETE
    """
    print("D... selecting channels:", channels)
    print( freemem() )
    # CHANNEL (i hope it is sorted)
    if delete_original:
        df1 = df.loc[ df["ch"].isin( channels ) ].copy()
        del df
    else:
        df1 = df.loc[ df["ch"].isin( channels ) ]
    df1.reset_index(inplace=True, drop=True)
    #del df
    if len(df1) ==0 :
        print("X... no data for channels",channels)
        sys.exit(1)
    endblock()
    return df1


def enhance_by_dtus_and_next_E(df):
    print("D... adding dtus and next_E columns")
    print( freemem() )

    print(f"D... broadening table - dt")
    df['dtus'] = (df.time.shift(-1)-df.time)*1000*1000
    df.fillna(0)
    df['dtus'] = df['dtus'].astype('float32') #
    print("D... range of erlang values : ",df['dtus'].min(), df['dtus'].max() )

    print(f"D... broadening table - next_E")
    df['next_E'] = (df.E.shift(-1))
    df.fillna(0, inplace=True)
    df['next_E'] = df['next_E'].astype('int32') #

    print(f"D... broadening table - next_ch")
    df['next_ch'] = (df.ch.shift(-1))
    df.fillna(0, inplace=True)
    df['next_ch'] = df['next_ch'].astype('int32') #

    if 'extras' in df.columns:
        print(f"D... broadening table - prev_dtus SATU")
        df['prev_satu'] = (df.time - df.time.shift(+1))*1000*1000
        df['prev_satu'] = np.where((df['extras']&1)==1, df['prev_satu'] , 0)
        df.fillna(0)
        df['prev_satu'] = df['prev_satu'].astype('float32') #

    print(df)
    endblock()
    return df

#----------------------------------------------------------------------
def pd_detect_zeroes(df, channel,  TIMEWIN_US = 25  ):
    """
   1-get the channel only
   2-dtus
    get number of zeroes, single zeroes, double zeroes, standalone zeroes
    -
      2nd phase - SZ and DZ - make one event from these PILEUPs
      3rd phase - create
    """
    print( "D.. detecting zeroes")
    print( freemem() )

    # this oneliner doesnt occupy memory ---------------
    # print("D... searching for correlations")
    dzeroes = len( df.loc[ ((df.E==0) & (df.next_E==0)) & (df.dtus<TIMEWIN_US) ])
    #df_dz = df.loc[ ((df.E==0) & (df.next_E==0)) & (df.dtus<TIMEWIN_US) ]
    #dzeroes = len(df_dz)
    print(freemem() )

    szeroes = len( df.loc[ ((df.E!=0) & (df.next_E==0)) & (df.dtus<TIMEWIN_US) ] )
    #szeroes = len(df_sz)
    print(freemem() )

    izeroes = len( df.loc[ ((df.E==0) & (df.next_E!=0)) & (df.dtus<TIMEWIN_US) ] )
    #izeroes = len(df_iz)
    print(freemem() )


    print(f"D... ---------------------- START of zero detection ch={channel}")
    zeroes = len( df.loc[ (df.E==0) & (df.ch==channel)] )
    zeroes2 = len( df[ (df.E==0) & (df.ch==channel)] )
    #zeroes = len(df_z)
    print(freemem() )


    print(f"D... total  zeroes (chan={channel}) = {zeroes} which is  {zeroes/len(df)*100:5.2f}%")
    print(f"D... total  zeroes (chan={channel}) = {zeroes2} which is  {zeroes2/len(df)*100:5.2f}%")
    print(f"D... double zeroes (chan={channel}) = {dzeroes} which is  {dzeroes/len(df)*100:5.2f}%")
    #print(df_dz)
    print(f"D... single zeroes (chan={channel}) = {szeroes} which is  {szeroes/len(df)*100:5.2f}%")
    #print(df_sz)
    print(f"D... ilogic zeroes (chan={channel}) = {izeroes} which is  {izeroes/len(df)*100:5.2f}%")
    #print(df_iz)
    print("D... ______________________ end of zero detection")


    # returns length for now
    endblock()
    return zeroes,dzeroes,szeroes,izeroes

#------------------------------------------------------------------------

def pd_read_table(filename, sort = True):
    """
    READ THE ASC TABLE:   two possibilities:  4 columns OR 5 columns
EARLIER:
         Events[ch][ev].TimeTag, ENERGY,(Events[ch][ev].Energy)>>MAXNBITS, ch
         MAXNBITS 15
Feb 2020+:
       Events[ch][ev].TimeTag, ENERGY,  (Events[ch][ev].Energy)>>MAXNBITS, ch, Events[ch][ev].Extras
       MAXNBITS 15
    >>t,e,PU (1/0) (or 3/0 old)  ,  channel,   Extras(2020+ only)


https://www.npl.washington.edu/TRIMS/sites/sand.npl.washington.edu.TRIMS/files/manuals-documentation/CAENDigitizer_SW_User_Manual_rel.5.pdf

EXTRAS: bit[0] = DEAD_TIME. This is set to 1 when a dead time occurred before this event. The dead time can be due to
either a signal saturation or a full memory status. Check Fig. B.4 and Fig. B.5 for more details
bit[1] = ROLL_OVER. Identify a trigger time stamp roll-over that occurred before this event
bit[2] = TT_RESET. Identify a trigger time stamp reset forced from external signals in S-IN (GPI for Desktop)
bit[3] = FAKE_EVENT. This is a fake event (which does not correspond to any physical event) that identifies a
time stamp roll-over. The roll-over can be due to an external or internal reset. The user can set bit[25]
= 1 of register 0x1n80 to enable the fake-event saving in case of reset from S-IN, and bit[26] = 1 of
register 0x1n80 to enable the fake-event saving in case of internal roll-over. In the first case the event
will have both bit[3] and bit[2] set to 1, while in the second case the event will have both bit[3] and
bit[1] set to 1.
    """
    start = dt.datetime.now()
    df = pd.read_table( filename,
                        names=['time','E','pu','ch','extras'],
                        sep = "\s+",
                        comment="#")

    meastime = (dt.datetime.now() - start).total_seconds()
    print(f"D... speed = {get_number_of_lines(filename)/meastime/1000/1000:.3f} Mrows/sec")


    print("D... lasttime ",df.iloc[-1]["time"])
    print(freemem() )
    # drop if 4 column
    df = df.dropna(axis='columns', how='all')


    df['time'] = df['time']/1e+8 # this is correct for 10ns step ADC
    print("D... lasttime ",df.iloc[-1]["time"])

    #print(df.dtypes)
    df['time'] = df['time'].astype('float64')
    df['E']    = df['E'].astype('int32')
    df['pu']    = df['pu'].astype('int32')
    df['ch']   = df['ch'].astype('int32')
    if 'extras' in df:
        df['extras'] = df['extras'].astype('int32')
    print("D...    finale types ************************************")
    print(df.dtypes)
    # print(freemem())

    #    df.to_hdf('run'+str(number)+'.h5',
    #              "matrix",
    #              format='t',
    #              data_columns=True,
    #              mode='w')

    # print(freemem() )
    if sort:
        print("D... sorting (after read_table):")
        #print(df)
        df = df.sort_values(by="time")
        #print(df)
        df.reset_index(inplace=True, drop=True)
        #print(df)
        #print( freemem() )

    print("D... lasttime ",df.iloc[-1]["time"])
    endblock()
    return df





#====================================== MAIN ==================================
#------------------------------------------------------------------------

def main():
    print("D... entry point of general")


#-------------------------------------------------------------------------

if __name__=="__main__":
    print("D... fastread can be called too, from bin_readvme")
    Fire(main)
