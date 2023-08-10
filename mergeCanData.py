# generates the output file merged, based on inputs from cmd line
import pandas as pd

#file_rcs="rcs_gps_message_raw2.csv"
#file_car58_speed="mvt_11_14_to_11_18_can_speed_car58.csv"
file_dim_vehicle="mvt_dim_vehicle.csv"
#file_controls_allowed="mvt_1114_1118_controls_allowed.csv"

import sys
n = len(sys.argv)

#if( n <= 3 ):
#    print("Must pass argument of desired input filename, and output filename")
#    print(" mergeCanData -i inputFile.csv -c 45 -o outputFile.csv")
#    print(" for car 45")
#    exit()

#inputFile=sys.argv[1]
#outputFile=sys.argv[2]

import argparse
parser = argparse.ArgumentParser(description="Merges CAN and ROS data from existing csv files into the RCS data.")
parser.add_argument('--input', '-i', help="Input CAN file (csv)", type=str)
parser.add_argument('--output', '-o', help="Output file (csv)", type=str)
parser.add_argument('--car', '-c', help="Car number", type=int)
parser.add_argument('--rcsfile', '-r', help="RCS file for this car (csv)", type=str)
parser.add_argument('--controlsAllowedFile', help="Controls allowed datafile for all cars (csv)", type=str)

args=parser.parse_args()


inputFile=args.input
outputFile=args.output
car=args.car
file_controls_allowed=args.controlsAllowedFile
file_rcs=args.rcsfile

if( None in [inputFile, outputFile, car, file_controls_allowed, file_rcs] ):
    print(parser.format_help())
    exit()

print("Generating ",outputFile, " from ", inputFile, " for car ", str(car) )

# read the rcs file
df_rcs_all = pd.read_csv(file_rcs).dropna()
# sort the file by car first, and then by time for each car
df_rcs = df_rcs_all.sort_values(by=['Systime'])

# throw away early values...why do we even have those?...
# the 'bad' ones are too short, so we can throw away any
# that are less than 0.5 of our max
max_time = max(df_rcs.Systime)
df_rcs = df_rcs[df_rcs['Systime'] > 0.5*max_time]

# read the input car's speed file
df_car_speed = pd.read_csv(inputFile)
df_car_speed = df_car_speed.set_index('systime', drop=False)

# read the vehicle to vin lookup
df_dim_vehicle = pd.read_csv(file_dim_vehicle)

# read the controls allowed file
df_controls_allowed = pd.read_csv(file_controls_allowed)
df_controls_allowed.sort_values(by=['Time'])

print("Processing car", car)
# veh_id is an integer, so we convert our string to an int
vin_car_df=df_dim_vehicle[df_dim_vehicle["veh_id"]==int(car)]
# get the row from this df: it should have just one row
# TODO: put an exception if len>1
vin_car=vin_car_df.iloc[0].vin
print("It has vin {}".format(vin_car))

df_controls_allowed_car=df_controls_allowed[df_controls_allowed["vin"]==vin_car]
df_controls_allowed_car.set_index('Time',inplace=True, drop=False)
df_controls_allowed_car.index.rename('TimeIndex')
df_controls_allowed_car = df_controls_allowed_car.sort_index()
# get df_rcs for this car only
df_rcs_car = df_rcs[df_rcs["vin"]==int(car)]
df_rcs_car = df_rcs_car.set_index('Systime',drop=False)

# let's put together the speed plus RCS data first
df_result_speed = pd.merge_asof(df_rcs_car, df_car_speed, left_index=True, right_index=True, suffixes=('','_can'))
# remove the cols we don't want
df_result_speed.drop(columns=['systime','vin_key','file_tag_id'],inplace=True)

# rename the can speed to something we like
df_result_speed.rename({"speed" : "can_speed" }, axis='columns', inplace=True)

# do the same for the controls_allowed
df_result = pd.merge_asof(df_result_speed, df_controls_allowed_car, left_index=True, right_index=True, suffixes=('','_ros'))
# take away some cols we don't want
df_result.drop(columns=['vin_ros','Time'],inplace=True)
# rename the data field to control_active
df_result.rename({"data" : "control_active"}, axis='columns', inplace=True)

# go back to our old index
df_result.index.rename('index_old')
df_result.rename({"Unnamed: 0" : "index_new" }, axis='columns', inplace=True)
df_result.set_index('index_new', inplace=True)
# reset the index to its original name
df_result.index.rename("", inplace=True)

print("Writing file ", outputFile)
# write to file
df_result.to_csv(outputFile)

