from collections import namedtuple
from copy        import deepcopy, copy

import subprocess
import logging as log

Fixed = namedtuple('Fixed', ['val'])
Fixed.__str__ = lambda f : f'{f.val}'
Param = namedtuple('Param', ['val', 'possible'])
Param.__str__ = lambda f : f'{f.val} ∈ {f.possible}'

class ExperimentConfig(object):
    def __init__(self, *args, **params):
        self.params = dict()
        self.params['version'] = subprocess.check_output(['git', 'describe', '--always']).strip()
        for arg in args:
            self.combine(arg)
        self.reconfigure(**params)

    def __getattr__(self, name):
        try:
            return self.params[name].val
        except KeyError:
            return object.__getattr__(self, name)

    def __getstate__(self):
        return self.params

    def __setstate__(self, params):
        self.params = params

    def update(self, k, v):
        self.params[k] = Fixed(v)

    def summary(self):
        return self.params

    def param_matrix(self):
        param_dict = copy(self.params)
        returned = False
        subconfigs = param_dict.get('subconfigs', Fixed([None]))
        for outer_subconfig in subconfigs.val:
            if outer_subconfig is None:
                possibilities = [ExperimentConfig()]
            else:
                possibilities = outer_subconfig.param_matrix()
            for subconfig in possibilities:
                # Oh, the combinatorial possiblities!!
                param_dict = copy(self.params)
                param_dict.update(subconfig.params)
                for name, param in param_dict.items():
                    if name != 'subconfigs':
                        if isinstance(param, Param):
                            for option in param.possible:
                                log.info(f'Config: setting {name} = {option}')
                                param_dict[name] = param._replace(val=option)
                                yield ExperimentConfig(**param_dict)
                                returned = True

                if not returned:
                    yield ExperimentConfig(**param_dict)

    def reconfigure(self, **params):
        parsed = {k : (v if (isinstance(v, Fixed)
                             or isinstance(v, Param))
                         else Fixed(v))
                  for k, v in params.items()}
        self.params.update(parsed)

    def combine(self, config):
        self.params.update(config.params)
