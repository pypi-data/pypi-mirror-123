import pandas as pd


def load_tag_info(path):
    tag_info = open(path).read()
    tag_info = tag_info.replace('  ', ' ')
    tag_info = tag_info.replace('  ', ' ')
    tag_info = tag_info.replace('  ', ' ')
    tag_info = tag_info.replace(':', '')
    tag_info = tag_info.replace(' \n', '\n')
    tag_info_list = tag_info.split('\n')

    tmp = [[i for i in line.split(' ')] for line in tag_info_list[2:] if ' ' in line]

    tag_df = pd.DataFrame(tmp)

    tag_df.columns = ['anchor_id', 'x', 'y', 'z']
    tag_df['anchor_id'] = tag_df['anchor_id'].astype('int')
    return tag_df


def load_distance_data(path):
    d1 = open(path).read()
    d2 = d1.split('\n')
    d3 = pd.DataFrame([line.split(':') for line in d2[1:]])
    d3.columns = ['c1', 'time', 'c3', 'tag_id', 'anchor_id', 'distance', 'distance_check', 'c8', 'c9']
    return d3
