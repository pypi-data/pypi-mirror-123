from uuid import uuid4
from pathlib import Path
# import logging
from datetime import datetime
from pprint import pprint

import json

class Experiment:
    ''' A custom class for organizing experiments & results '''
    def __init__(self, name, settings):
        self.id = uuid4()
        self.timestamp = datetime.now()
        self.name = name
        self.settings = settings

        self.experiment_dir = Path(f'data/experiments/{name}')
        self.instance_dir   = self.experiment_dir.joinpath(self.timestamp.strftime('%b_%d_%Y_%H%M%S'))
        self.instance_dir.mkdir(parents=True, exist_ok=True)

        self.train_metrics = self.instance_dir.joinpath(f'{name}_train.csv')
        self.test_metrics  = self.instance_dir.joinpath(f'{name}_test.csv')
        self.val_metrics   = self.instance_dir.joinpath(f'{name}_val.csv')
        self.metainfo      = self.instance_dir.joinpath('meta.json')
        self.figures       = self.instance_dir.joinpath('figures')
        self.checkpoints   = self.instance_dir.joinpath('checkpoints')

        self.figures.mkdir(parents=True, exist_ok=True)
        self.checkpoints.mkdir(parents=True, exist_ok=True)
        self.metainfo.write_text(json.dumps(self.settings.params, default=lambda o : '__unserialized__'))

    def update(self, **kwargs):
        self.settings.update(**kwargs)

    def derive(self, name, **kwargs):
        derived_exp = type(self)(f'{self.name} {name}', self.settings.derive(**kwargs))
        return derived_exp

    def run(self):
        raise NotImplementedError('The default Experiment class does not implement run(), use a derived class :)')

    def log(self, metrics, total_seen, kind='train'):
        if kind == 'train':
            metrics_file = self.train_metrics
        elif kind == 'test':
            metrics_file = self.test_metrics
        elif kind == 'val':
            metrics_file = self.val_metrics
        else:
            raise NotImplementedError(f'Cannot handle file of label {kind} in Experiment {self.name}')

        order = list(sorted(metrics.keys()))
        if not metrics_file.is_file():
            metrics_file.write_text(','.join(order) + '\n')
        with open(metrics_file, 'a') as outfile:
            outfile.write(','.join(str(metrics[k]) for k in order) + '\n')
        if total_seen % self.settings.log_interval == 0:
            print('{name:30}: L={loss:2.4f} t={duration:4.6f}'.format(**metrics))

    def reseed(self, seed):
        raise NotImplementedError('Must define reseeding in terms of scientific application')

    def checkpoint(self, model):
        raise NotImplementedError('No default checkpoint() function is defined')

    def __str__(self):
        return f'{self.name}'
