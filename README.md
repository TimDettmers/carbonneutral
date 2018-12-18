# Carbon Neutral Calculator for Academic Labs

This calculator estimates your carbon footprint by looking at the two largest factors: (1) flights, (2) GPU computing. It adds a multiplicative factor on top of this for other emissions (default 20%). This repository is inspired by the [NYU ML^2 Lab going carbon neutral](https://wp.nyu.edu/ml2/carbon-neutral-lab/).

## How to Use This Carbon Free Calculator

1. First install the requirements: `pip install -r requirements.txt`
2. Create a txt file that lists all the publications in your lab in the format: PAPER COUNT, CONFERENCE NAME. Look at `xlab.txt` for a valid example.
3. Add missing conferences and their location to `conferences.txt`
4. Call the script to calculate your carbon footprint (see below for details).
5. If there were missing conferences that you needed to add, please consider submitting a pull request so that the next person doing this does not have to add the conferences.

## Script parameters

- hq, default='Seattle', type=str, help='The city name where your lab is based. This is for travel to conferences.')
- pubs, default='./xlab.txt', type=str, help='The text file which contains the list of conferences.')
- avg_people_per_conference, default=2.0, type=float, help='How many people do on average travelt to conferences.')
- num_gpus, default=10, type=int, help='The number of GPUs in the lab.')
- avg_gpu_watt, default=250, type=int, help='The average wattage of all GPUs in the lab')
- avg_gpu_util, default=0.75, type=float, help='The average utilization of all GPUs in the lab')
- other_emissions_fraction, type=float, default=0.2, help='This is the fraction of all other emissions of your lab that are not from GPUs or conferences. This can be food, paper for printing, and others. The default value of 0.2 is quite conservative.')

## What to Offset The Calculated Emissions?

1. Register with the [UN Carbon offset platform](https://offset.climateneutralnow.org/howtooffset).
2. Choose a specific project which you want to buy carbon offsets from.
3. Specify the amount produced by this calculator.
4. Congratulations — your lab is now carbon neutral!

