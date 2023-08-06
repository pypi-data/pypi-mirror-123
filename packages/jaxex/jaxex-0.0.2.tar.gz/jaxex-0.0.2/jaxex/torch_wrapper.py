import torch

def clip_grads(net):
    """Gradient clipping to the range [10, 10]."""
    parameters = list(filter(lambda p: p.grad is not None, net.parameters()))
    for p in parameters:
        p.grad.data.clamp_(-10, 10)

class TorchWrapper:
    def __init__(self, net, settings, name):
        self.net = net
        self.criterion = torch.nn.BCELoss()
        self.optimizer = torch.optim.RMSprop(self.net.parameters(), lr=settings.learning_rate)
        self.is_jax = False
        self.param_count = sum(p.numel() for p in self.net.parameters() if p.requires_grad)
        self.name = name

    def init(self):
        pass
        # torch.nn.init.xavier_uniform(self.net)

    def forward(self, x, y):
        inp_seq_len = x.size(1)
        batch_size, outp_seq_len, _ = y.size()

        # New sequence
        self.net.init_sequence(batch_size)

        # Feed the sequence + delimiter
        for i in range(inp_seq_len):
            self.net(x[:, i])

        # Read the output (no input given)
        y_out = torch.zeros(y.size())
        for i in range(outp_seq_len):
            y_out[:, i], _ = self.net()
        return y_out

    def eval(self, x, y):
        self.optimizer.zero_grad()
        y_out = self.forward(x, y)
        loss = self.criterion(y_out, y)
        self.optimizer.zero_grad()
        return dict(loss=loss.item(), name=self.name)

    def step(self, x, y):
        self.optimizer.zero_grad()
        y_out = self.forward(x, y)
        loss = self.criterion(y_out, y)
        loss.backward()
        clip_grads(self.net)
        self.optimizer.step()
        return dict(loss=loss.item(), name=self.name)

    def save(self, location):
        torch.save(self.net.state_dict, location)

    def load(self, location):
        self.net.load_state_dict(torch.load(location))
        self.net.eval()
