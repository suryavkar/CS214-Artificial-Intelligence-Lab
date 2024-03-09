import pandas as pd
import numpy as np
import sys

def calc_entropy(data,class_name):
    total_count = data.shape[0];
    entropy = 0;
    for c in data[class_name].unique():
#         print('\n',data[data[class_label]==c],'\n')
        class_count = data[data[class_name]==c].shape[0]
        if class_count != 0:
            entropy -= (class_count/total_count)*np.log2(class_count/total_count)
    return entropy

def calc_gain(data,feature_name,class_name):
    gain = calc_entropy(data,class_name)
    total_count = data.shape[0]
    for feature_value in data[feature_name].unique():
        feature_count = data[data[feature_name]==feature_value].shape[0]
        gain -= (feature_count/total_count)*calc_entropy(data[data[feature_name]==feature_value],class_name)
    return gain

def get_best_feature(data,class_name):
    best_gain = -np.inf
    best_feature_name = None
    
    feature_names = data.columns.drop(class_name)
    for feature_name in feature_names:
        gain = calc_gain(data,feature_name,class_name)
        if gain > best_gain:
            best_gain = gain
            best_feature_name = feature_name
    return best_feature_name

def id3(data,class_name):
    tree = {}
    skip_feature = 0
    if not data.empty:
        best_feature_name = get_best_feature(data,class_name)
        for feature_value in data[best_feature_name].unique():
            new_data = data[data[best_feature_name]==feature_value]
            total_count = new_data.shape[0]
            for label in new_data[class_name].unique():
                if new_data[new_data[class_name]==label].shape[0] == 1 or total_count == new_data[new_data[class_name]==label].shape[0]:
                    tree[f'{best_feature_name} = {feature_value}'] = label
                    skip_feature = 1
            if skip_feature == 0:
                tree[f'{best_feature_name} = {feature_value}'] = id3(new_data.drop(best_feature_name,inplace=False,axis=1),class_name)
            else:
                skip_feature = 0
    return tree
        
def display_tree(d, indent=0):
    for key, value in d.items():
        print('\n'+'\t' * indent + str(key),end='')
        if isinstance(value, dict):
            display_tree(value, indent+1)
        else:
            print(': ' + str(value))

if __name__ == "__main__":
    data = pd.read_table(str(sys.argv[1]),delimiter='\t')

    data = data.drop_duplicates()

display_tree(id3(data,'playtennis' if str(sys.argv[1])=='tennis.txt' else 'survived'))