from pathlib import Path
import haiku as hk
import numpy as np
import optax
import jax
import jax.numpy as jnp
from jax.scipy.special import logsumexp
from jax import grad, jit, vmap, value_and_grad, lax, random

def save(params, path):
    for name, layer in params.items():
        sub = path.joinpath(name)
        sub.mkdir(parents=True, exist_ok=True)
        for key, values in layer.items():
            subsub = sub.joinpath(key)
            if isinstance(values, jnp.DeviceArray):
                np.savez(subsub, values)
            else:
                for subkey, subvalues in values.items():
                    subsubsub = subsub.joinpath(subkey)
                    np.savez(subsubsub, subvalues)

def load(path):
    params = dict()
    for sub in path.rglob('*'):
        if sub.is_file():
            if sub.suffix == 'npz':
                value = jnp.array(np.load(sub), dtype=jnp.float32)
            else:
                continue
            keys = list(k for k in sub.parts[1:]) # if k != '~')
            current = params
            for k in keys[:-1]:
                if k not in current:
                    current[k] = dict()
                current = current[k]
            current[keys[-1]] = value
    return hk.data_structures.to_immutable_dict(params)

class JaxWrapper:
    def __init__(self, model, settings, name):
        print('Creating wrapper for', name)
        def forward(x):
            net = model()
            si = net.initial_state(settings.batch_size)
            if settings.apply_vmap:
                net = vmap(net)
            return hk.dynamic_unroll(net, x, si, time_major=False)

        self.opt       = optax.rmsprop(settings.learning_rate)
        self.net       = hk.without_apply_rng(hk.transform(forward))
        self.name = name
        self.is_jax = True

        self.params    = None
        self.opt_state = None
        self.loss_func = None
        self.param_count = None

    def init(self, x0, settings):
        ''' Initialization with RNG, needs to be called with different keys to work correctly '''
        print(f'Building {self.name} {x0.shape}')
        self.params    = self.net.init(settings.key, x0)
        self.opt_state = self.opt.init(self.params)

        @jit
        def loss_func(params, x, y):
            # TODO: Potentially introduce a MASK over irrelevant bits/channels
            yh, final_state = self.net.apply(params, x)
            return (jnp.sum(optax.sigmoid_binary_cross_entropy(yh, y))
                    / jnp.prod(jnp.array(yh.shape)))

        self.loss_func = loss_func
        self.param_count = sum(x.size for x in jax.tree_leaves(self.params))

    def eval(self, x, y):
        loss = self.loss_func(self.params, x, y)
        return dict(loss=loss, name=self.name)

    def step(self, x, y):
        loss, grad = jax.value_and_grad(self.loss_func)(self.params, x, y)
        updates, self.opt_state = self.opt.update(grad, self.opt_state)
        self.params = optax.apply_updates(self.params, updates)
        return dict(loss=loss, name=self.name)

    def save(self, path):
        save(self.params, path)

    def load(self, path):
        self.params = load(path)
