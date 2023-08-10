# generates the output file merged, based on inputs from cmd line
import pandas as pd

file_rcs="rcs_gps_message_raw2.csv"
file_dim_vehicle="mvt_dim_vehicle.csv"

import sys
n = len(sys.argv)

if( n <= 2 ):
    print("Must pass argument of desired input filename")
    print(" extractCarRcsFile.py inputFile.csv builddir")
    exit()

inputFile=sys.argv[1]
builddir=sys.argv[2]

print("Generating rcs_gps files for each car.")

try:
    df_rcs_all = pd.read_csv(file_rcs).dropna()
    # read the rcs file
    df_rcs_all = pd.read_csv(file_rcs).dropna()
    # sort the file by car first, and then by time for each car
    df_rcs = df_rcs_all.sort_values(by=['Systime'])

    # throw away early values...why do we even have those?...
    # the 'bad' ones are too short, so we can throw away any
    # that are less than 0.5 of our max
    max_time = max(df_rcs.Systime)
    df_rcs = df_rcs[df_rcs['Systime'] > 0.5*max_time]

    # read the vehicle to vin lookup
    df_dim_vehicle = pd.read_csv(file_dim_vehicle)
    
    cars=df_dim_vehicle['veh_id']

    for car in cars:
        print("Generating file for car", car)
        # get df_rcs for this car only
        df_rcs_car = df_rcs[df_rcs["vin"]==int(car)]
        df_rcs_car.to_csv("{}/rcs_gps_message_raw2_car{}.csv".format(builddir, car))
except:
    import traceback
    print("Unable to process input file ", inputFile, ". Aborting.")
    traceback.print_exc()



