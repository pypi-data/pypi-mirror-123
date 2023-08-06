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

    tag_df.columns = ['id', 'x', 'y', 'z']
    tag_df['id'] = tag_df['id'].astype('int')
    return tag_df
