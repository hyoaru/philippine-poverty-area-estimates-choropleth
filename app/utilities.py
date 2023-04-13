import os
import pickle
import pandas as pd

def save_fig_binary(figure, file_name: str, folder_name: str, ) -> None:
    """Saves figure to binary format"""

    data_root_path = f'data/bin/{folder_name}'
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/bin'):
        os.mkdir('data/bin')
    if not os.path.exists(data_root_path):
        os.mkdir(data_root_path)

    with open(f'{data_root_path}/{file_name}.bin', 'wb') as file:
        pickle.dump(figure, file)


def load_fig_binary(file_name: str, folder_name: str):
    """Loads and returns binary figure"""

    data_root_path = f'data/bin/{folder_name}'
    if os.path.exists(f'{data_root_path}/{file_name}.bin'):
        file = open(f'{data_root_path}/{file_name}.bin', 'rb')
        figure = pickle.load(file)
        file.close()
        return figure
    else:
        return None