# Makefile for producing each output file

# does not include cars for which we have no data, since they did not drive
# these are: 7, 49, 81, 101, 102, 104
CARS=1 2 3 4 5 6 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 103
# # we need all these source files to gen the desired output files
# SOURCES=$(wildcard ../mvt-speed/mvt_11_14_to_11_18_can_speed_car*.csv)
# now change these into the desired output filenames
# OBJECTS=$(patsubst %.csv,%_)

BUILDDIR=build

# output files, maybe?
INPUTS=$(addprefix ../mvt-speed/mvt_11_14_to_11_18_can_speed_car, $(CARS)) 
OUTPUTS=$(addsuffix .csv, $(addprefix $(BUILDDIR)/circles_v2_1_car, $(CARS)))
CARRCS=$(addsuffix .csv, $(addprefix $(BUILDDIR)/rcs/rcs_gps_message_raw2_car, $(CARS)))
SINGLEFILE=circles_v2_1_car_all.csv

all: build $(CARRCS) $(SINGLEFILE)

$(SINGLEFILE) : $(OUTPUTS)
	touch $(SINGLEFILE)
	
$(OUTPUTS): $(BUILDDIR)/circles_v2_1_car%.csv : ../mvt-speed/mvt_11_14_to_11_18_can_speed_car%.csv $(BUILDDIR)/rcs/rcs_gps_message_raw2_car%.csv
#echo look at $@ which came from $^
# get the car name
	#CAR=$(patsubst build/rcs/rcs_gps_message_raw2_car%,%, $(patsubst %.csv, %, $(word 2,$^)))
# $^ gives all prereqs, the second one that matches is the raw RCS data
	#rcsfile=$(word 2,$^)
# $^ gives all prereqs, the first one that matches is the CAN data
	#canspeedfile=$(word 1,$^)
	python3 mergeCanData.py -i $(word 1,$^) -o $@ -c $(patsubst build/rcs/rcs_gps_message_raw2_car%,%, $(patsubst %.csv, %, $(word 2,$^))) -r $(word 2,$^) --controlsAllowedFile ../mvt-controls_allowed/mvt_1114_1118_controls_allowed.csv

$(CARRCS): rcs_gps_message_raw2.csv
	python3 extractCarRcsFile.py rcs_gps_message_raw2.csv build/rcs

build: 
	mkdir -p build/rcs



