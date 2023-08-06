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

    tag_df.columns = ['tag_id', 'x', 'y', 'z']
    tag_df['tag_id'] = tag_df['tag_id'].astype('int')
    for key in ['x', 'y', 'z']:
        tag_df[key] = tag_df[key].astype('float')
    return tag_df


def load_distince_data(path):
    d1 = open(path).read()
    d2 = d1.split('\n')
    d3 = pd.DataFrame([line.split(':') for line in d2[1:] if ':' in line])
    d3.columns = ['c1', 'unixtime', 'c3', 'tag_id', 'anchor_id', 'distance', 'distance_check', 'c8', 'data_index']
    d3['distance'] = d3['distance'].astype('float')
    d3['distance_check'] = d3['distance_check'].astype('float')

    d41 = d3[['data_index', 'anchor_id', 'distance']].pivot(index='data_index', columns='anchor_id', values='distance')
    d41.reset_index(inplace=True)
    d41.columns = ['data_index', 'dis_0', 'dis_1', 'dis_2', 'dis_3']

    d42 = d3[['data_index', 'anchor_id', 'distance_check']].pivot(
        index='data_index', columns='anchor_id', values='distance_check')
    d42.reset_index(inplace=True)
    d42.columns = ['data_index', 'dis_c_0', 'dis_c_1', 'dis_c_2', 'dis_c_3']

    d5 = d3[['c1', 'data_index', 'c3', 'tag_id', 'c8', 'unixtime']].groupby(['data_index']).max().reset_index()

    d6 = pd.merge(d5, d41, on=['data_index'])
    d6 = pd.merge(d6, d42, on=['data_index'])

    d6.reset_index(drop=True, inplace=True)

    assert len(d41) == len(d41) == len(d5) == len(d6)

    return d6
