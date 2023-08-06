import rasterio
from math import ceil, exp, log, pi
import pkg_resources

class utils:
    @staticmethod
    def compute_E(lat:float,long:float):
        try:
            coords = [(long,lat)]
            # Use this to get the file location 
            path_pkg = pkg_resources.resource_filename(__name__, 'data/E/E.bil')
            #path_lkl = 'data/E/E.bil'
            src = rasterio.open(path_pkg)
            e_vals = src.sample(coords)
            return float([val for val in e_vals][0])
        except:
            return None

    @staticmethod
    def compute_AGB(E, D, WD): 
        try:
            return exp(-2.023977 - (0.89563505 * E) + (0.92023559 * log(WD)) + (2.79495823 * log(D)) - (0.04606298 * (log(D)**2))) 
        except:
            return None

    @staticmethod
    def get_wood_density(scientific_name, wdDF):
        name_lower = scientific_name.lower()
        try:
            name_space = name_lower.replace('_',' ')
        except:
            return None
        try:
            filtered_row = wdDF[wdDF['Binomial']==name_space]
            return float(filtered_row['WoodDensity'])
        except:
            # likely return value is empty, return None
            return None
    
    @staticmethod
    def surface_area(plot_shape, deq):
        if plot_shape == 'rectangle' or plot_shape == 'square':
            return deq**2
        else:
            return pi * (deq/2)**2