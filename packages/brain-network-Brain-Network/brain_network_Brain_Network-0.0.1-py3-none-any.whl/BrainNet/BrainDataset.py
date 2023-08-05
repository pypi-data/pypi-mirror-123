import torch
import numpy as np
import os.path as osp

from scipy.io import loadmat
from torch_geometric.data import InMemoryDataset, download_url, Data, DataLoader
from torch_geometric.utils import dense_to_sparse


class MVData(Data):
    def __init__(self, num_views=None, num_nodes=None, y=None, *args, **kwargs):
        super(MVData, self).__init__()
        self.num_views = num_views
        self.num_nodes = num_nodes
        self.y = y
        for k, v in kwargs.items():
            if k.startswith('x') or k.startswith('edge_index') or k.startswith('edge_attr'):
                self.__dict__[k] = v

    def __inc__(self, key, value):
        if key.startswith('edge_index'):
            return self.num_nodes
        else:
            return super().__inc__(key, value)


class BrainDataset(InMemoryDataset):
    def __init__(self, root, name, transform=None, pre_transform=None):
        self.name = name.upper()
        self.filename_postfix = str(pre_transform) if pre_transform is not None else None
        assert self.name in ['PPMI', 'HIV', 'BP']
        super(BrainDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_dir(self):
        return osp.join(self.root, self.name, 'raw')

    @property
    def processed_dir(self):
        return osp.join(self.root, self.name, 'processed')

    @property
    def raw_file_names(self):
        return f'{self.name}.mat'

    @property
    def processed_file_names(self):
        return f'data_{self.filename_postfix}.pt' if self.filename_postfix is not None else 'data.pt'

    def download(self):
        raise NotImplementedError
        # url = 'https://sxkdz.github.io/files/datasets/'
        # print(self.raw_paths)
        # download_url(url + self.raw_file_names, self.raw_dir)

    def process(self):
        m = loadmat(osp.join(self.raw_dir, self.raw_file_names))
        if self.name == 'PPMI':
            raw_data = m['X']
            num_graphs = raw_data.shape[0]
            num_nodes = raw_data[0][0].shape[0]
            a0 = np.zeros((num_graphs, num_nodes, num_nodes))
            a1 = np.zeros((num_graphs, num_nodes, num_nodes))
            a2 = np.zeros((num_graphs, num_nodes, num_nodes))
            for i, sample in enumerate(raw_data):
                a0[i, :, :] = sample[0][:, :, 0]
                a1[i, :, :] = sample[0][:, :, 1]
                a2[i, :, :] = sample[0][:, :, 2]
            adjs = [
                torch.Tensor(a0),
                torch.Tensor(a1),
                torch.Tensor(a2)
            ]
            num_views = 3
        else:
            adjs = [
                torch.Tensor(m['fmri']).transpose(0, 2),
                torch.Tensor(m['dti']).transpose(0, 2)
            ]
            num_graphs = adjs[0].shape[0]
            num_nodes = adjs[0].shape[1]
            num_views = 2

        y = torch.Tensor(m['label']).long().flatten()
        y[y == -1] = 0

        data_list = []
        for i in range(num_graphs):
            edge_indices = []
            edge_attrs = []
            for adj in adjs:
                edge_index, edge_attr = dense_to_sparse(adj[i])
                edge_indices.append(edge_index)
                edge_attrs.append(edge_attr)
            mvdata = {}
            for j in range(num_views):
                mvdata[f'edge_index{j}'] = edge_indices[j]
                mvdata[f'edge_attr{j}'] = edge_attrs[j]
            data = MVData(num_views=num_views, num_nodes=num_nodes, y=y[i], **mvdata)
            data_list.append(data)

        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{self.name}()'