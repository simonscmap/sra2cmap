# sra2cmap

Convert SRA metadata to CMAP import format. Accepts a list of SRA metadata files and an `--outdir` to write Excel files. The `-d` option is in case the SRA file is not tab-delimited.

````
$ ./sra2cmap.py -h
usage: sra2cmap.py [-h] [-d str] [-o str] FILE [FILE ...]

Convert SRA metadata to CMAP import

positional arguments:
  FILE                  SRA metadata

optional arguments:
  -h, --help            show this help message and exit
  -d str, --delimiter str
                        Field delimiter (default: )
  -o str, --outdir str  Output directory (default: export)
````


E.g., PRJNA385854 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA385854/) looks like this:

````
// ****** Record 1 ****** //
BioSample          : SAMN07136695
DATASTORE_filetype : cloud.realign sra
DATASTORE_provider : gs ncbi
DATASTORE_region   : gs.US-EAST1
Experiment         : SRX2974743
Library_Name       : S0226
LoadDate           : 2017-06-30
MBases             : 6550
MBytes             : 2817
Run                : SRR5787989
SRA_Sample         : SRS2329750
Sample_Name        : S0226
bottle_id          : 637139
collection_date    : 2011-03-12T01:56:00
cruise_id          : JC057
cruise_station     : 7
depth              : 9m
geo_loc_name       : Atlantic Ocean
geotraces_section  : GA02
lat_lon            : 37.8305 S 41.1248 W
Assay_Type         : WGS
AvgSpotLen         : 300
BioProject         : PRJNA385854
BioSampleModel     : MIMS.me
Center_Name        : MIT
Consent            : public
InsertSize         : 0
Instrument         : NextSeq 550
LibraryLayout      : PAIRED
LibrarySelection   : RANDOM
LibrarySource      : METAGENOMIC
Organism           : marine metagenome
Platform           : ILLUMINA
ReleaseDate        : 2018-05-01
SRA_Study          : SRP110813
env_biome          : ocean_biome
env_feature        : ocean
env_material       : water
````

We need four standard fields: time, lat, lon, depth.

This program will look for those four fields, format them correctly, and place them first in the resulting Excel file.

# Author

Ken Youens-Clark <kyclark@email.arizona.edu>`
