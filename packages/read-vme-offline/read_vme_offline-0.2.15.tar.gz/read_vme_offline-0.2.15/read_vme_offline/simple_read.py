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
from tabulate import tabulate

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


#=====================================================================

def coincidences(filename, ch0, ch1,  tree = False):
    """
    """
    print( general.freemem() )

    #*************
    nlines   = general.get_number_of_lines(filename)
    ncolumns = general.get_number_of_columns(filename)
    print(f"i... reading the table of {nlines} lines ... ({nlines/1e+6:.1f} milion lines)")
    print(f"i... reading the table of {ncolumns} columns ... ")


    #*************
    df = general.pd_read_table(filename, sort = True)
    #print(df.dtypes)
    #print(df)
    chan_available = df['ch'].unique()
    print("D... channels available:", chan_available )
    print("D... x        present:",df['pu'].unique() )
    if 'extras' in df:
        print("D... y        present:",df['extras'].unique() )
    print("D... Emin            :",df['E'].min() )
    print("D... Emax            :",df['E'].max() )

    if not((ch0 in chan_available) and (ch1 in chan_available)):
        print(f"X... channels {ch0} OR {ch1} not in the file !!")
        sys.exit(1)

    #-------------------------here shold be something to check double events in a detector

    #-------------------------here shold be something to check double events in a detector

    #**************** select
    df1 = general.select_channels(df, [ch0,ch1] , delete_original = True)

    n_ch0 = len(df1.loc[ df1['ch']==ch0  ])
    n_ch1 = len(df1.loc[ df1['ch']==ch1  ])
    print(f"D... # events {n_ch0} and {n_ch1}")


    #df1['time'] = np.where( df1['ch']==ch1,  df1['time'] ,  df1['time']+5.0)


    TIMESHIFT = 2

    df1.loc[ df1['ch'] ==ch1, 'time'] += TIMESHIFT*1e-6 # ADD  x us to ch1 time
    df1 = df1.sort_values(by="time")
    df1.reset_index(inplace=True, drop=True)


    # df1.drop( df[df. < 50].index, inplace=True)
    #*************  dt us    and next_E
    df1 = general.enhance_by_dtus_and_next_E(df1)


    df1.drop(df1.tail(1).index,inplace=True) # drop last n rows


    #drop all longer than
    df1 = df1.loc[ df1['dtus']<TIMESHIFT*2 ]

    print(df1)

    print(f"D... RANDOM EVENTS starting with ch=={ch1}: ",len(df1.loc[ df1['ch']==ch1] ) )
    print(f"D... ZERO E EVENTS                       : ",len(df1.loc[ df1['E']==0] ) )
    print(f"D... ZERO E EVENTS                       : ",len(df1.loc[ df1['next_E']==0] ) )
    print()
    print(f"D... N{ch0}={n_ch0} , N{ch1}={n_ch1},  COIN# {ch0}x{ch1} = {len(df1)} ... {100*len(df1)/min(n_ch0,n_ch1):.2f} %" )

    print(f"D... dtus statistics:           MEAN = {df1['dtus'].mean():.2f}  STD={df1['dtus'].std():.2f} us" )
    print()

    bname = os.path.splitext(filename)[0]  #basename
    #--------------- histogram coincidence time
    hname = general.generate_hname(filename, ch0)+f"_coin{ch1}"
    outfile = bname+f"_{ch0}_coin{ch1}"+".txt"
    #*************
    his = general.column_to_histo(  df1['dtus']  , binmax=int(2*TIMESHIFT*100), himax=2*TIMESHIFT, savename= outfile, hname = hname, writeondisk = True, writetxt = False) # 500 for 2us is exactly channel by channel


    if tree:
        df1.rename(columns = {'E':f'E{ch0}','next_E':f'E{ch1}'}, inplace = True)
        general.save_to_tree( df1, filename, modname=f"coin_{ch0}_{ch1}" )

    return

#=============================== MAIN1 EVA ==================
def eva_cut_time(filename,  chan, od=0, do=9999999 ,   tree = False):
    """
    EVA: use: read_vme_offline cut1 filename_with_asc  60 120
    """
    # od = 0
    # do = 999999




    print("D... expect 30Mevents processed per minute at best")
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
    #print(df.dtypes)
    print(df)

    print("+"*50,"TOTALS")
    chan_available = df['ch'].unique()
    print("D... channels available:", chan_available, "   chan selected:", chan)
    print(f"D... pu        present: {df['pu'].unique()} ... 1 or 0 (3v0 before 2020)" )
    if 'extras' in df:
        print(f"D... extras    present: {df['extras'].unique()}... 1..satur,3..roll,4..reset,8..fake" )
        print(f"D... total saturations: ",len( df.loc[ (df['extras']&1)==1]  ) )
    print("D... Emin            :",df['E'].min() )
    print("D... Emax            :",df['E'].max() )

    if not(chan in chan_available):
        print(f"X... no events in channel {chan}")
        return



    if (od!=0) and (do<9999999):
        print()
        print(f"D...  selecting events    from {od}s to {do}s")
        print(f"D...  selecting events    from {od}s to {do}s")
        print(f"D...  selecting events    from {od}s to {do}s")
        print()
        df1 = df[ (df.time>od)&(df.time<do)  ].copy() # copy ELSE warning....
        df1.reset_index(inplace=True, drop=True)
        df1.fillna(0,inplace=True)

        print(df1)
        if len(df1)==0:
            print("D... no data for channel {chan}")
            sys.exit(0)

    else:
        df1 = df



    #---------------------------------------------------DF1 ---------------------------
    #************* reduce the DF
    df1 = general.select_channels(df1, [chan] , delete_original = True)



    print("+"*50,"CHANNEL",chan)
    chan_available = df1['ch'].unique()
    print("D... channels available:", chan_available, "   chan selected:", chan)
    print(f"D... pu        present: {df1['pu'].unique()}... 1 or 0 (3v0 before 2020)" )
    if ncolumns == 5:
        pileups_ch = len(df1.loc[ df1['pu']==1])
    else:
        pileups_ch = len(df1.loc[ df1['pu']==3])

    print(f"D... pu        present: {df1['pu'].unique()}... 1 or 0 (3v0 before 2020)" )
    if 'extras' in df:
        print(f"D... extras    present: {df1['extras'].unique()}... 1..satur,3..roll,4..reset,8..fake" )
        print(f"D... number of saturations: ",len( df1.loc[ (df1['extras']&1)==1]  ) )
    print("D... Emin            :",df1['E'].min() )
    print("D... Emax            :",df1['E'].max() )



    #*************  dt us    and next_E
    df1 = general.enhance_by_dtus_and_next_E(df1)
    satu_n_ch = len(df1.loc[ (df1['extras']&1)!=0] )
    print("D... SATURATIONS\n",df1.loc[ (df1['extras']&1)!=0] )
    satu_DT_ch = df1.loc[ (df1['extras']&1)!=0]["prev_satu"].sum()
    print(f"D... SATURATIONS {satu_n_ch} total: {satu_DT_ch/1e+6} sec.")


    # not final
    stat_columns = ['ch','rate','realT','liveT','deadT','satT','min_dtus','Nzero','Npu','Ndz','Ntot','Nsat','DT%','DT+S%']
    df_stat = pd.DataFrame( np.nan, index=[0], columns = stat_columns )
    df_stat['ch'] = chan
    df_stat['Nsat'] = satu_n_ch
    df_stat['satT'] = satu_DT_ch/1e+6
    df_stat['min_dtus'] = df1.loc[df1['dtus']!=0]['dtus'].min()
    #print( df1.loc[df1['dtus']!=0]['dtus'].min())
    #print( df1['dtus'].min())
    if df_stat.iloc[-1]['min_dtus'] != df1['dtus'].min():
        if len(df1.loc[ df1['dtus']==0] )!=1:
            print("X... some error in creation of dtus - i need to debug it")
            sys.exit(1)
    df_stat['Npu'] = pileups_ch


    #------------- histogram with time erlang---------------------------------
    bname = os.path.splitext(filename)[0]  #basename
    # hname = bname.split("_")[-1]  # last thing should be a comment
    #*************
    hname = general.generate_hname(filename, chan)+"_erlang"
    outfile = bname+"erlang_ch"+str(chan)+".txt"
    #*************
    his = general.column_to_histo(df1['dtus'], binmax=1000, himax=1+int(df1["dtus"].max()),savename = outfile, hname = hname, writeondisk = True, writetxt = False)
    hname = general.generate_hname(filename, chan)+"_erlang2"
    outfile = bname+"erlang2_ch"+str(chan)+".txt"
    #*************
    his = general.column_to_histo(df1['dtus'], binmax=1000, himax=100,savename = outfile, hname = hname, writeondisk = True, writetxt = False)



    #--------------- histogram zeros in time
    hname = general.generate_hname(filename, chan)+"_zerotime"
    outfile = bname+"zerotime_ch"+str(chan)+".txt"
    #*************
    his = general.column_to_histo(  df1.loc[ (df1.E==0)  ]["time"]  , binmax=1+int(df1.iloc[-1]["time"]), himax=1+int(df1.iloc[-1]["time"]), savename = outfile, hname = hname, writeondisk = True, writetxt = False)


    #--------------- histogram nonzeroes in time
    hname = general.generate_hname(filename, chan)+"_nzerotime"
    outfile = bname+"nzerotime_ch"+str(chan)+".txt"
    #*************
    his = general.column_to_histo(  df1["time"].loc[ (df1.E!=0)  ]  , binmax=1+int(df1.iloc[-1]["time"]), himax=1+int(df1.iloc[-1]["time"]), savename = outfile, hname = hname, writeondisk = True, writetxt = False)


    #--------------- histogram saturations distribution in time
    hname = general.generate_hname(filename, chan)+"_saturations"
    outfile = bname+"saturations_ch"+str(chan)+".txt"
    #*************
    his = general.column_to_histo(  df1["time"].loc[ (df1.prev_satu!=0)  ]  , binmax=1+int(df1.iloc[-1]["time"]), himax=1+int(df1.iloc[-1]["time"]), savename = outfile, hname = hname, writeondisk = True, writetxt = False)


    #--------------- histogram saturations length
    hname = general.generate_hname(filename, chan)+"_satlength"
    outfile = bname+"satlength_ch"+str(chan)+".txt"
    #*************
    his = general.column_to_histo(  df1["prev_satu"].loc[ (df1.prev_satu!=0)  ]  , binmax=100, himax=1+int(df1["prev_satu"].max()), savename = outfile, hname = hname, writeondisk = True, writetxt = False)





    #*************   one channel; time span
    len_dfzero,len_dzeroes,len_szeroes,len_izeroes = general.pd_detect_zeroes(df1, chan) # df1[ (df1.E==0) ]




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
    dift = lev - fev  # difference of times
    deadt = dift*deadtpr/100
    livet = dift - deadt

    livetprsat = (dift - deadt - satu_DT_ch/1e+6)
    deadtprsat = (dift - livetprsat)/dift*100


    stopcut = start + dt.timedelta(seconds=lev)
    rate = len(df1)/dift

    output = f"""
     file   == {filename}
    channel == {chan}
     rate   == {rate:.1f} cps
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
     saturations= {satu_DT_ch/1e+6:.2f} s

     DT %       = {deadtpr:.2f} %
     DT(inc sat)= {deadtprsat:.2f} %
"""
    print(output)

    df_stat['rate'] =  rate
    df_stat['DT%'] = deadtpr
    df_stat['DT+S%'] = deadtprsat

    df_stat['realT'] =dift
    df_stat['liveT'] = livet
    df_stat['deadT'] = deadt
    df_stat['Nzero'] =len_dfzero
    df_stat['Ntot'] = len(df1)
    df_stat['iDTavg'] = 100*( (1/rate) * satu_n_ch )/dift   #  average dt * nsatur
    df_stat['iDTmin'] = 100*( df_stat['min_dtus']*1e-6 * satu_n_ch )/dift  #  mintime * nsatur
    #    df_stat['tSAT'] =


    df_stat['Ndz'] = len_dzeroes+len_szeroes+len_izeroes

#    df_stat = df_stat.round( decimals = 2 )
    df_stat = df_stat.round( decimals = 2 )

    print( tabulate(df_stat, headers='keys',showindex="never"))#, tablefmt='psql'
    print()

    outinfo = os.path.splitext(filename)[0]+f"_ch{chan}.info"
    print(f"D... creating info FILE {outinfo}")
    with open(outinfo,"w") as f:
        f.write(output)



    bname = os.path.splitext(filename)[0]  #basename
    # hname = bname.split("_")[-1]  # last thing should be a comment
    #*************
    hname = general.generate_hname(filename, chan)


    outfile = bname+f"_ch{chan}.txt"
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
