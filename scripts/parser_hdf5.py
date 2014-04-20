import hdf5_functions
h5 = hdf5_functions.open_h5_file_read(\..\TRAXLZU12903D05F94.h5)
artist_name = hdf5_functions.get_artist_name(h5)
title = hdf5_functions.get_title(h5)
track_id = hdf5_functions.get_track_id(h5)
duration = hdf5_functions.get_duration(h5)
year = hdf5_functions.get_year(h5)
print artist_name
print title
print track_id
print duration
print year

h5.close()