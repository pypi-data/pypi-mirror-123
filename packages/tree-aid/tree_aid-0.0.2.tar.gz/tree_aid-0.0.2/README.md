# Readme

Tree Aid Utilities

Simply call:

'''
python3 -m tree_aid.placettes
'''

In the directory with the tree and plot data (.json), will output a CSV with processed data.

Alternativly, use in a script / jupyter notebook..

'''
from tree_aid.placettes import add_data_to_df, get_clean_tree_df, get_dictionary_from_json
#from tree_aid.placettes import add_data_to_df, get_clean_tree_df, get_dictionary_from_json
%load_ext autoreload
%autoreload 2

config = {
    'name_scientific': 'name_scientific',
    'small_trees': 'small_circle/repeat_small_tree_circle',
    'large_trees': 'group_large_tree/repeat_large_tree',
    'geolocation': '_geolocation',
    'large_tree_stems' : 'group_large_tree/repeat_large_tree/grp_tree_stand_shoots/repeat_circumference_stem',
    'large_tree_circumfrence': 'group_large_tree/repeat_large_tree/grp_tree_stand_shoots/repeat_circumference_stem/grp_circumference_stem/circumference_measure'
}
    
tree_data_loc = './test/Mali_PMP_TREE_Survey_FINAL-2021-10-11-15-15-46.json'
plot_data_loc = './test/Mali_PMP_PLOT_Survey_FINAL-2021-10-11-15-16-08.json'
output_data_loc = './output.csv'

tree_data = get_dictionary_from_json(tree_data_loc)
plot_data = get_dictionary_from_json(plot_data_loc)

tree_plot_df = get_clean_tree_df(tree_data,plot_data, config)
output_df = add_data_to_df(tree_plot_df, config)
#output_df.to_csv(output_data_loc)
'''