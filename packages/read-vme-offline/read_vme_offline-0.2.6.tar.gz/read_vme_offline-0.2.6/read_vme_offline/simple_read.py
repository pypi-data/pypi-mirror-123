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


import read_vme_offline.general as general

from shutil import copyfile

import sys

import ROOT


#>>> import pandas as pd
#>>> import matplotlib.pyplot as plt
#>>> df=pd.read_hdf("run0001_20200526_102519.h5")
#>>> plt.hist( df['E'][  (df.xx=0) & ( (df.t-df.t.shift())<0.0001) ] , 1024, range=[0,2048] )
# plt.show()
#
#


def shift_channels(df , TSHIFT, TWIN, x,y):

    # df = df.loc[  df["ch"]==1 , "time"] = df["time"] + 100
    # df['time'] = df['ch'].apply(lambda x: df["time"]+100 if  x==1 else df["time"] )

    #works
    #df["time"] = df["time"] + TSHIFT*df["ch"]

    #df.loc[df['chan'] == x, 'time'] = df.loc[ df['chan']==x , 'time'] + TSHIFT
    df.loc[df['ch'] == y, 'time'] = df.loc[ df['ch']==y , 'time'] + TSHIFT
    return df


def only_read( filename, x=0, y=1, batch=0, read_last=0, MAXROWS=1000*1000):
    """
    reads the filename to DF and returns it
    """
    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]
    startd = basename.split("_")[1]
    startt = basename.split("_")[2]
    print("D...  time start MARK=",startd+startt)


    ok = False
    try:
        start = dt.datetime.strptime(startd+startt,"%Y%m%d%H%M%S" )
        ok = True
        print("D... succesfull start with 4 digit year")
    except:
        print("x... year may not by 4 digits")

    if not(ok):
        print("X... trying 2 digits for year")
        start = dt.datetime.strptime(startd+startt,"%y%m%d%H%M%S" )

    with open(filename) as f:
        count = sum(1 for _ in f)

    print("D... total lines=",count)
    print("D... real start",start)

    print("D... basename = ",basename)
    if read_last>0:
        print("D... read_table last",read_last)
        df = pd.read_table( filename, names=['time',"e",'x','ch','y'],
                            sep = "\s+", comment="#",
                            nrows = read_last,
                            skiprows=count-read_last,
                            error_bad_lines=False,

        )
                        #nrows = MAXROWS,
                        #skiprows=MAXROWS*batch)
    else:
        print("D... read_table batch#",batch)
        df = pd.read_table( filename, names=['time',"e",'x','ch','y'],
                        sep = "\s+", comment="#",
                        nrows = MAXROWS,
                        skiprows=MAXROWS*batch)

        print(df)
    return df


#----------------- used during the expseriment-----------------
# plot is true by default to run from cmdline
# overwrite when running from code
def fastread(filename, x=0, y=1, batch = 0, read_last=0, df = None, plot = True):
    """
    COINCIDENCES: use: ./bin_readvme fast run0023_20200220_144753.asc 0 1  --read_last 500
    """
    TSHIFT = 30 # 10 seems ok, 20 is safe (200ns)  40 broke some detetors
    TWIN = 2*TSHIFT
    CHAN0=x
    CHAN1=y
    ENE_0="chan_"+str(CHAN0)
    ENE_1="chan_"+str(CHAN1)
    MAXROWS = 1000*1000*35


    if df is None:
        df = only_read(filename, x,y,batch, read_last, MAXROWS)

    # energy is marked "e"
    df = df.rename(columns={"e":ENE_0})


    if (len(df)<MAXROWS):
        print("X... END OF FILE REACHED ***")
        CONTINUE = False
    else:
        CONTINUE = True
    print("D... len=", len(df)," SHIFTING chan IN TIME BY ",TSHIFT*10,"ns")
    df = shift_channels(df, TSHIFT, TWIN, x, y)
    print("D... len=", len(df) )


    print("D... SORTING BY TIME")
    df1=df.sort_values(by="time")
    df1.reset_index(inplace=True, drop=True)
    print("D... len=", len(df) )

    print(f"D... select channels {x},{y}")
    df1 = df1.loc[  (df1["ch"]==CHAN0)|(df1["ch"]==CHAN1) ]
    print("D... len=", len(df) )


    print("D... introducing shift differences")
    df1['prev'] = df1['time'] - df1.shift(1)['time']
    df1['next'] = - df1['time'] + df1.shift(-1)['time']

    print("D... len=", len(df1) , " dropping lonely events" )
    #df1 = df1[ (df1["prev"]<TWIN) | (df1["next"]<TWIN) ]
    df1 = df1[ (df1["prev"]<TWIN) | (df1["next"]<TWIN) ]


    print("D... len=", len(df1))

    if (1==0): # CHECK THE EVENTS IN WINDOW ========== NEXT IS GOOD
        dfnext = df1[ (df1["ch"]==0) & (df1["next"]<TWIN)]
        print("D... DF next", len(dfnext) )
        dfprev = df1[ (df1["ch"]==0) & (df1["prev"]<TWIN)]
        print("D... DF prev", len(dfprev) )


    df1[ENE_1] = df1.shift(-1)[ENE_0]
    print(df1)

    print("D... dropping all when NEXT < ",TWIN )
    df2 = df1.loc[  df1["next"]<TWIN ]
    print( "D... len =",len(df2) )
    print("D...  window mean / 3sigma ... {:.1f} +- {:.1f}".format(df2["next"].mean(),  3*df2["next"].std() ))


    if CONTINUE:
        print(f"D... only {MAXROWS} read")
        print("X...  INCOMPLETE FILE, TRY TO READ batch=", batch+1)

    if plot:
        df2.plot.scatter(x=ENE_0,  y=ENE_1,
                     ylim=(0, 6000), xlim=(0,6000),
                     s=.01);
        plt.show()
        return

    return df2




#=============================== MAIN1 EVA ==================
def eva_cut_time(filename,  od=0, do=9999999 , chan=1,  tree = False):
    """
    EVA: use: read_vme_offline cut1 filename_with_asc  60 120
    """
    # od = 0
    # do = 999999


    print( general.freemem() )

    #*************
    start = general.filename_decomp(filename)   #  - get start


    print(f"D... real start",start)
    od_dt = dt.timedelta(seconds=od)
    do_dt = dt.timedelta(seconds=do)
    print(f"D... skip       {od} sec ... {od_dt}")


    startcut = start + od_dt
    stopcut = start + do_dt
    print(f"D... CUT  start {startcut}")
    print(f"D... CUT  stop  {stopcut}  (demanded or max)")


    #*************
    nlines   = general.get_number_of_lines(filename)
    ncolumns = general.get_number_of_columns(filename)
    print(f"i... reading the table of {nlines} lines ... ({nlines/1e+6:.1f} milion lines)")
    print(f"i... reading the table of {ncolumns} columns ... ")
    #print(f"i... reading the table of {ncolumns} columns ... ", end="")


    #*************
    df = general.pd_read_table(filename, sort = True)
    print(df.dtypes)
    print("D... channels present:",df['ch'].unique() )
    print(df)


    if (od!=0) and (do<9999999):
        print()
        print(f"D...  selecting events for  channel {chan} from {od}s to {do}s")
        print(f"D...  selecting events for  channel {chan} from {od}s to {do}s")
        print(f"D...  selecting events for  channel {chan} from {od}s to {do}s")
        print()
        df1 = df[ (df.ch==chan)&(df.time>od)&(df.time<do)  ].copy() # copy ELSE warning....
        df1.reset_index(inplace=True, drop=True)
        df1.fillna(0,inplace=True)

        print(df1)
        if len(df1)==0:
            print("D... no data for channel {chan}")
            sys.exit(0)
    else:
        df1 = df


    #*************   one channel; time span
    len_dfzero,_ = general.pd_detect_zeroes(df1, chan) # df1[ (df1.E==0) ]




    print()
    print(f"D...  selecting nonzero events for  channel {chan} ")
    print(f"D...  selecting nonzero events for  channel {chan} ")
    print(f"D...  selecting nonzero events for  channel {chan} ")
    print()

    df2 = df1[ df1.E!=0 ]
    df2.reset_index(inplace=True, drop=True)


    print()
#    print("i... ZEROES == ", len(dfzero))
#    print("i... EVENTS == ", len(df2))
    deadtpr = len_dfzero/len(df2) * 100
    fev = df1.time.iloc[0]
    lev = df1.time.iloc[-1]
#    print(f"i... DT %   == {deadtpr:.2f}")
    # print(f"i... events == {fev} ... {lev}")
    # print(f"i... times  == {fev:.2f} ... {lev:.2f}")
    dift = lev - fev
    deadt = dift*deadtpr/100
    livet = dift - deadt

    stopcut = start + dt.timedelta(seconds=lev)

    output = f"""
     file   == {filename}
     times  == {fev:.2f} ... {lev:.2f}
     real T == {dift:.2f} s
     live T == {livet:.2f} s
     dead T == {deadt:.2f} s
     start  == {start}
     CUTsta == {startcut}
     CUTsto == {stopcut}

     zeroes     = {len_dfzero:8d}
     nz events  = {len(df2):8d}
     tot events = {len(df1):8d}

     DT %       = {deadtpr:.2f}
"""
    print(output)

    outinfo = os.path.splitext(filename)[0]+".info"
    print(f"D... creating info FILE {outinfo}")
    with open(outinfo,"w") as f:
        f.write(output)



    bname = os.path.splitext(filename)[0]  #basename
    # hname = bname.split("_")[-1]  # last thing should be a comment
    #*************
    hname = general.generate_hname(filename, chan)

    outfile = bname+".txt"
    #*************
    his = general.column_to_histo(df2['E'], savename = outfile, hname = hname, writeondisk = True)
    outfile2 = bname+".asc1"
    print(f"D... {outfile2} is save as a duplicate")
    copyfile(outfile, outfile2)

    print( general.freemem() )


    if tree:
        #*************
        general.save_to_tree(df2, filename) #

    print( general.freemem() )

    return


if __name__=="__main__":
    print("D... fastread can be called too, from bin_readvme")
    Fire(eva_cut_time)
