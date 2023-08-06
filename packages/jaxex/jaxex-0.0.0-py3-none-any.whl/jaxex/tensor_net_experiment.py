from .experiment import Experiment
import numpy as np
import jax.numpy as jnp
from time import time

import torch
import jax.random as jr
from pprint import pprint

from torch.utils.data import DataLoader

class TensorNetExperiment(Experiment):
    ''' A custom class for organizing experiments & results '''
    def reseed(self, seed):
        torch.manual_seed(seed)
        self.settings.update(key=jr.PRNGKey(seed))

    def loop(self, repeats=1, epochs=1, loader=None, kind='train'):
        for seed in range(repeats):
            self.reseed(seed)
            for epoch in range(epochs):
                for batch, (xt, yt) in enumerate(loader):
                    total_seen = batch * self.settings.batch_size
                    for model in self.settings.wrapped_models:
                        if model.is_jax:
                            x = xt.cpu().detach().numpy().astype(np.float32)
                            y = jnp.array(yt.cpu().detach().numpy()).astype(np.float32)
                        else:
                            x = xt.float(); y = yt.float()
                        start = time()
                        if kind == 'train':
                            metrics = model.step(x, y)
                        else:
                            metrics = model.eval(x, y)
                        end = time()
                        metrics.update(duration=end-start, seed=seed, epoch=epoch, batch=batch)
                        self.log(metrics, total_seen, kind=kind)
                    if kind == 'train' and total_seen % self.settings.checkpoint_interval == 0:
                        self.checkpoint(total_seen)

    def run(self):
        pprint(self.settings.params)
        loader = lambda d : DataLoader(d, batch_size=self.settings.batch_size,
                                          drop_last=self.settings.drop_last)
        train_loader = loader(self.settings.train_data)
        test_loader  = loader(self.settings.test_data)

        x0, y0 = next(iter(train_loader))
        x0_jax = x0.cpu().detach().numpy().astype(np.float32)

        for model in self.settings.wrapped_models:
            if model.is_jax:
                model.init(x0_jax, self.settings)
            else:
                model.init()
        try:
            self.loop(self.settings.repeats, self.settings.epochs, train_loader, kind='train')
            self.loop(self.settings.repeats, self.settings.epochs, test_loader, kind='test')
        except KeyboardInterrupt:
            print('Received Keyboard Interrupt, successfully broke out of experiment loop')

    def checkpoint(self, total_seen):
        for model in self.settings.wrapped_models:
            model_dir = self.checkpoints.joinpath(f'{model.name}_{total_seen}')
            model.save(model_dir)
            print(f'Saving checkpoint of {model.name} after {total_seen} training examples')


