# -*- coding: utf-8 -*-
import numpy as np
from torch.utils.data import Dataset, DataLoader
from os.path import join, dirname, abspath
import sys

import utils.config_loader as config
from utils.config_loader import config_model
from data.dataset_parser import dataset_parser
import data.data_tools as data_tools

import utils.tools as tools
from frame.ir.ir_tools import load_retrieved_passages
from frame.bert_passage.bert_input import build_bert_passage_x

sys.path.insert(0, dirname(dirname(abspath(__file__))))


class ClusterDataset(Dataset):
    def __init__(self, cid, query, retrieve_dp, tdqfs_data=False, transform=None):
        super(ClusterDataset, self).__init__()
        original_passages, _, passage_ids = load_retrieved_passages(retrieved_dp=retrieve_dp,
            cid=cid,
            get_sents=True,
            tdqfs_data=tdqfs_data)
        self.passages = original_passages
        self.passage_ids = passage_ids

        self.query = query
        self.yy = 0.0  # 0.0

        self.transform = transform

    def __len__(self):
        return len(self.passages)

    @staticmethod
    def _vec_label(yy):
        if yy == '-1.0':
            yy = 0.0
        return np.array([yy], dtype=np.float32)

    def __getitem__(self, index):
        """
            get an item from self.doc_ids.

            return a sample: (xx, yy)
        """
        # build xx
        xx = build_bert_passage_x(self.query, passage=self.passages[index])

        # build yy
        yy = self._vec_label(self.yy)

        sample = {
            **xx,
            'yy': yy,
        }

        if self.transform:
            sample = self.transform(sample)

        return sample


class ClusterDataLoader(DataLoader):
    def __init__(self, cid, query, retrieve_dp, tdqfs_data=False, transform=data_tools.ToTensor()):
        dataset = ClusterDataset(cid, query, retrieve_dp=retrieve_dp, tdqfs_data=tdqfs_data)
        self.transform = transform
        self.cid = cid
        self.passage_ids = dataset.passage_ids

        super(ClusterDataLoader, self).__init__(dataset=dataset,
                                                batch_size=8,
                                                shuffle=False,
                                                num_workers=3,  # 3
                                                drop_last=False)

    def _generator(self, super_iter):
        while True:
            batch = next(super_iter)
            batch = self.transform(batch)
            yield batch

    def __iter__(self):
        super_iter = super(ClusterDataLoader, self).__iter__()
        return self._generator(super_iter)


class QSDataLoader:
    """
        iter over all clusters.
        each cluster is handled with a separate data loader.

        tokenize_narr: whether tokenize query into sentences.
    """

    def __init__(self, tokenize_narr, query_type, retrieve_dp):
        if query_type == config.TITLE:
            query_dict = dataset_parser.get_cid2title()
        elif query_type == config.NARR:
            query_dict = dataset_parser.get_cid2narr()
        elif query_type == config.QUERY:
            query_dict = dataset_parser.get_cid2query(tokenize_narr)
        else:
            raise ValueError('Invalid query_type: {}'.format(query_type))

        cids = tools.get_test_cc_ids()

        self.loader_init_params = []
        for cid in cids:
            query = query_dict[cid]
            self.loader_init_params.append({
                'cid': cid,
                'query': query,
                'retrieve_dp': retrieve_dp,
            })

    def _loader_generator(self):
        for params in self.loader_init_params:
            c_loader = ClusterDataLoader(**params)
            yield c_loader

    def __iter__(self):
        return self._loader_generator()


class TdqfsQSDataLoader:
    """
        iter over all clusters.
        each cluster is handled with a separate data loader.
    """

    def __init__(self, test_cid_query_dicts, retrieve_dp):
        self.loader_init_params = []
        for cq_dict in test_cid_query_dicts:
            self.loader_init_params.append({
                'cid': cq_dict['cid'],
                'query': cq_dict['query'],
                'retrieve_dp': retrieve_dp,
                'tdqfs_data': True,
            })

    def _loader_generator(self):
        for params in self.loader_init_params:
            c_loader = ClusterDataLoader(**params)
            yield c_loader

    def __iter__(self):
        return self._loader_generator()
    