import numpy as np

# usefull class for grid work
# it is able to build our grid from the edges, and the grid-step
# calculates and stores the all lat and lon grid-step values and the borders of geographical cells represented by the grid points
# it calculates a subgrid as well, which is higher resolution than the original - if divider = 3, then our steps will be 3 times shorter, so on
# our original 1X1 cell we get a 3X3 resolution

class SubGridBuilder:
    def __init__(self, grid_WESN, grid_gaps=(1,1), divider=1):
        self.divider = int(divider)
        self.west = grid_WESN[0]
        self.east = grid_WESN[1]
        self.south = grid_WESN[2]
        self.north = grid_WESN[3]
        self.gap_lon = grid_gaps[0]
        self.gap_lat = grid_gaps[1]
        self.default_lon_grid = [x for x in np.arange(self.west, self.east + self.gap_lon, self.gap_lon)]
        self.default_lat_grid = [x for x in np.arange(self.south, self.north + self.gap_lat, self.gap_lat)]
        self.default_lon_border = [x for x in np.arange(self.west - (self.gap_lon/2), self.east + (self.gap_lon/2) + self.gap_lon, self.gap_lon)]
        self.default_lat_border = [x for x in np.arange(self.south - (self.gap_lat/2), self.north + (self.gap_lat/2) + self.gap_lat, self.gap_lat)]        
        self.sub_lon_grid, self.sub_lon_border, self.sub_lat_grid, self.sub_lat_border = self.build_grid()

    def build_grid(self):
        if self.divider < 1:
            raise ValueError('divider should be integer and larger than 0')
        if self.divider == 1:
            return (self.default_lon_grid, self.default_lon_border, self.default_lat_grid, self.default_lat_border)
        else:
            lon_border = np.linspace(self.default_lon_border[0], self.default_lon_border[-1], (len(self.default_lon_grid)*self.divider)+1)
            lat_border = np.linspace(self.default_lat_border[0], self.default_lat_border[-1], (len(self.default_lat_grid)*self.divider)+1)
            lon_grid = [(lon_border[i]+lon_border[i+1])/2 for i, x in enumerate(lon_border) if i < len(lon_border)-1]
            lat_grid = [(lat_border[i]+lat_border[i+1])/2 for i, x in enumerate(lat_border) if i < len(lat_border)-1]
            return (lon_grid, lon_border.tolist(), lat_grid, lat_border.tolist())