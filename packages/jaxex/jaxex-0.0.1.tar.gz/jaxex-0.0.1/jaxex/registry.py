class Registry:
    def __init__(self):
        self.experiments = dict()

    def add(self, experiment):
        self.experiments[experiment.name] = experiment

    def run(self, name):
        return self.experiments[name].run()

    def list(self):
        for k, v in self.experiments.items():
            print(f'{k:40} : {v}')

