import json
import pandas as pd
from .placettes_utils import utils
import os
import sys
from math import sqrt, nan, pi
import pkg_resources

def get_dictionary_from_json(f_loc):
    with open(f_loc) as fin:
        return json.load(fin)
        
def get_clean_tree_df(tree_data, plot_data, config):
    
    def flatten_large_tree(tree, config):
        """
        Reduces the number of shoots in tree to a single diameter
        """
        tree2 = tree
        try:
            iter_shoots = config['large_tree_stems']
            
            # Get circumfrences
            circumfrences = []
            for s in tree2[iter_shoots]:
                c = config['large_tree_circumfrence']
                circumfrences.append(s[c])
            
            # Calculate diameters and deq
            diameters = [i/(pi) for i in circumfrences]
            tree2['deq (cm)'] = sqrt(sum([i**2 for i in diameters]))

            # Delete steams
            del tree2[iter_shoots]
            return tree2
        
        except Exception as e:
            # If all else fails, return the original tree (with an attempy to remove nested shoots)
            try:
                del tree[iter_shoots]
            except Exception as e2:
                pass
            
            tree['deq (cm)'] = nan
            return tree

    def clean_columns(df:pd.DataFrame)->pd.DataFrame:
        columns = list(df.columns)
        cleaned = []
        for col in columns:
            # If theres a name, i.e small_tree_scientific other etc, strip
            if 'name' in col:
                cleaned.append(col.split('tree_')[-1])
            else:
                cleaned.append(col.split('/')[-1])
        df.columns = cleaned
        return df
    
    large_trees = []
    small_trees = []

    for plot_idx, plot in enumerate(tree_data):
        for tree in plot[config['large_trees']]:
            tree['plot_idx'] = plot_idx
            tree['tree_type'] = 'large'
            flattened = flatten_large_tree(tree, config)
            large_trees.append(flattened)
            # deal with large trees
        
        for tree in plot[config['large_trees']]:
            tree['plot_idx'] = plot_idx
            tree['tree_type'] = 'small'
            small_trees.append(tree)
    
    small_trees_df = pd.DataFrame.from_dict(small_trees)
    large_trees_df = pd.DataFrame.from_dict(large_trees)
    plot_data_df = pd.DataFrame.from_dict(plot_data)

    # Clean columns
    small_trees_df = clean_columns(small_trees_df)
    large_trees_df = clean_columns(large_trees_df)
    plot_data_df = clean_columns(plot_data_df)

    # Combine large and small, merge with plots and drop temp plot_idx col
    trees_df = pd.concat([large_trees_df, small_trees_df], axis=0, ignore_index=True)
    tree_plot_df = pd.merge(left=trees_df,right=plot_data_df,how='left', left_on='plot_idx', right_index=True).drop(columns='plot_idx')
    
    return tree_plot_df

def add_data_to_df(df, config):
    wd_csv_path = pkg_resources.resource_filename(__name__, 'data/wd_means.csv')
    wdDF = pd.read_csv(wd_csv_path)
    df['WD'] = df[config['name_scientific']].apply(lambda x: utils.get_wood_density(x, wdDF))
    df['E'] = df[config['geolocation']].apply(lambda x: utils.compute_E(x[0],x[1]))
    df['deq (m)'] = df['deq (cm)']/100
    df['AGB (kg)'] = df[['E','deq (cm)','WD']].apply(lambda x: utils.compute_AGB(x["E"], x['deq (cm)'], x["WD"]), axis=1)
    return df
    
if __name__ == "__main__":
    
    config = {
        'name_scientific': 'name_scientific',
        'small_trees': 'small_circle/repeat_small_tree_circle',
        'large_trees': 'group_large_tree/repeat_large_tree',
        'geolocation': '_geolocation',
        'large_tree_stems' : 'group_large_tree/repeat_large_tree/grp_tree_stand_shoots/repeat_circumference_stem',
        'large_tree_circumfrence': 'group_large_tree/repeat_large_tree/grp_tree_stand_shoots/repeat_circumference_stem/grp_circumference_stem/circumference_measure'
    }
    
    current_dir = os.listdir('./')
    
    tree_data_loc = None
    plot_data_loc = None

    for f in current_dir:
        f = f.lower()
        if 'tree' in f and f[-5:]=='.json':
            tree_data_loc = f
            print(f'Tree Data Found: {f}')
        elif 'plot' in f and f[-5:]=='.json':
            plot_data_loc = f
            print(f'Plot Data Found: {f}')

    if (tree_data_loc is None) or (plot_data_loc is None):
        print('Faiure loading tree or plot data \nEXITING')
        sys.exit()

    tree_data = get_dictionary_from_json(tree_data_loc)
    plot_data = get_dictionary_from_json(plot_data_loc)

    try:
        tree_plot_df = get_clean_tree_df(tree_data, plot_data, config)
        output_df = add_data_to_df(tree_plot_df, config)
        output_df.to_csv('./output.csv', index=False)
        print('Outputted to: ./output.csv')
    except Exception as e:
        print(f'FAILED: {e}')