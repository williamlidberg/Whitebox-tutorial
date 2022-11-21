import os
import whitebox
wbt = whitebox.WhiteboxTools()
wbt.verbose=True

# inputs
dem = '/tutorial/data/dem.tif'
streams = '/tutorial/data/culverts.shp'
roads = '/tutorial/data/Extendedroads.shp'
# output 
roadburned = '/tempdir/roadburneddem.tif'
road_width = 10

# Burn streams across roads
wbt.burn_streams_at_roads(
    dem = dem, 
    streams = streams, 
    roads = roads, 
    output = roadburned, 
    width=road_width,
)

# Inputs

# Outputs
breacheddem = '/tempdir/breacheddem.tif'

# Resolve all remaining depressions
wbt.breach_depressions(
    dem = roadburned, 
    output = breacheddem, 
    max_depth=None, # if a max depth is set it will prevent sinks deeper than that to be breached.
    max_length=None, # if a max length is set it will prevent sinks that require a path longer than that to be breached.
    flat_increment=0.001, # if flat surfaces suck as lakes have the slope 0 it will act like a sink. This parameter will set a small slope to flat areas.
    fill_pits=True # Pits are sinks that are just one pixel big.
)

breacheddem = '/tempdir/breacheddem.tif'
d8_flow_pointer = '/tempdir/D8FlowPointer.tif'
d8_flow_accumulation = '/tempdir/D8FlowAcc.tif'

# Flow pointer
wbt.d8_pointer(
    dem = breacheddem, 
    output = d8_flow_pointer, 
    esri_pntr=False
)

# Flow accumulation
wbt.d8_flow_accumulation(
    i = d8_flow_pointer, 
    output = d8_flow_accumulation, 
    out_type = 'catchment area', 
    log=False, 
    clip=False, 
    pntr=True, 
    esri_pntr=False
)

rasterstreams = '/tempdir/RasterStreams.tif'
vectorstreams = '/tutorial/VectorStreams6ha.shp'
threshold = 60000

wbt.extract_streams(
    flow_accum = d8_flow_accumulation, 
    output = rasterstreams, 
    threshold = threshold, 
    zero_background=False
)

# convert raster streams to vector
wbt.raster_streams_to_vector(
    streams = rasterstreams, 
    d8_pntr = d8_flow_pointer, 
    output = vectorstreams, 
    esri_pntr=False
)

tempdir = '/tempdir/'
for i in os.listdir(tempdir):
  os.remove(tempdir + i)
print('Temp files removed')
