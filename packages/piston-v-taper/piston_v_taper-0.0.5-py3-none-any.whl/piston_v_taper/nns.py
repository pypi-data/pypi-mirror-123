import torch
from torch import nn


class ElastoplasticRegression(nn.Module):
    def __init__(self, input_dim, mid_dim, output_dim, x_translation, x_scale, n_hidden_layers=1):
        super(ElastoplasticRegression, self).__init__()

        self.x_translation = x_translation
        self.x_scale = x_scale

        self.input = nn.Linear(input_dim, mid_dim)
        torch.nn.init.xavier_uniform_(self.input.weight)
        torch.nn.init.zeros_(self.input.bias)

        self.output = nn.Linear(mid_dim, output_dim)
        torch.nn.init.xavier_uniform_(self.output.weight)
        torch.nn.init.zeros_(self.output.bias)

        self.hidden = nn.ModuleList([torch.nn.Linear(mid_dim, mid_dim) for i in range(n_hidden_layers)])
        self.n_hidden_layers = n_hidden_layers
        for i in range(n_hidden_layers):
            torch.nn.init.xavier_uniform_(self.hidden[i].weight)
            torch.nn.init.zeros_(self.hidden[i].bias)

        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(1)

        self.accuracy = 0

    def forward(self, x):
        x = self.input(x)
        x = self.sigmoid(x)

        for i in range(self.n_hidden_layers):
            x = self.hidden[i](x)
            x = self.hidden[i](x)

        x = self.output(x)
        x = self.sigmoid(x)
        x = self.softmax(x)

        return x

    def predict(self, x):
        x = x * self.x_scale + self.x_translation
        return self(x)


class ElasticRegression(nn.Module):
    def __init__(self, input_dim, mid_dim, output_dim, x_translation, x_scale, n_hidden_layers=1):
        super(ElasticRegression, self).__init__()

        self.x_translation = x_translation
        self.x_scale = x_scale

        self.input = nn.Linear(input_dim, mid_dim)
        torch.nn.init.xavier_uniform_(self.input.weight)
        torch.nn.init.zeros_(self.input.bias)

        self.output = nn.Linear(mid_dim, output_dim)
        torch.nn.init.xavier_uniform_(self.output.weight)
        torch.nn.init.zeros_(self.output.bias)

        self.hidden = nn.ModuleList([torch.nn.Linear(mid_dim, mid_dim) for i in range(n_hidden_layers)])
        self.n_hidden_layers = n_hidden_layers
        for i in range(n_hidden_layers):
            torch.nn.init.xavier_uniform_(self.hidden[i].weight)
            torch.nn.init.zeros_(self.hidden[i].bias)

        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(1)

        self.accuracy = 0

    def forward(self, x):
        x = self.input(x)
        x = self.sigmoid(x)

        for i in range(self.n_hidden_layers):
            x = self.hidden[i](x)
            x = self.hidden[i](x)

        x = self.output(x)
        x = self.sigmoid(x)
        x = self.softmax(x)

        return x

    def predict(self, x):
        x = x * self.x_scale + self.x_translation
        return self(x)


class ElasticRegression1(torch.nn.Module):
    def __init__(self, n_in=3, n_mid=3, n_hidden_layers=0, n_out=2):
        super(ElasticRegression1, self).__init__()
        self.input = nn.Linear(n_in, n_mid)
        torch.nn.init.xavier_uniform_(self.input.weight)
        torch.nn.init.zeros_(self.input.bias)

        self.output = nn.Linear(n_mid, n_out)
        torch.nn.init.xavier_uniform_(self.output.weight)
        torch.nn.init.zeros_(self.output.bias)

        self.hidden = nn.ModuleList([torch.nn.Linear(n_mid, n_mid) for i in range(n_hidden_layers)])
        self.n_hidden = n_hidden_layers
        for i in range(n_hidden_layers):
            torch.nn.init.xavier_uniform_(self.hidden[i].weight)
            torch.nn.init.zeros_(self.hidden[i].bias)

        self.relu = nn.ReLU()
        self.activation = nn.ReLU()

    def forward(self, x):
        z = self.input(x)
        # z = self.activation(z)
        z = self.activation(z)

        for i in range(self.n_hidden):
            z = self.hidden[i](z)
            z = self.activation(z)

        z = self.output(z)
        # z[0, :] = z[0, :] ** 2
        # z = z ** 2

        # z = self.activation(z)
        return z


class ContactClassification(nn.Module):
    def __init__(self, input_dim, mid_dim, output_dim, x_translation, x_scale, n_hidden_layers=1):
        super(ContactClassification, self).__init__()

        self.x_translation = x_translation
        self.x_scale = x_scale

        self.input = nn.Linear(input_dim, mid_dim)
        torch.nn.init.xavier_uniform_(self.input.weight)
        torch.nn.init.zeros_(self.input.bias)

        self.output = nn.Linear(mid_dim, output_dim)
        torch.nn.init.xavier_uniform_(self.output.weight)
        torch.nn.init.zeros_(self.output.bias)

        self.hidden = nn.ModuleList([torch.nn.Linear(mid_dim, mid_dim) for i in range(n_hidden_layers)])
        self.n_hidden_layers = n_hidden_layers
        for i in range(n_hidden_layers):
            torch.nn.init.xavier_uniform_(self.hidden[i].weight)
            torch.nn.init.zeros_(self.hidden[i].bias)

        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(1)

        self.accuracy = 0

    def forward(self, x):
        x = self.input(x)
        x = self.sigmoid(x)

        for i in range(self.n_hidden_layers):
            x = self.hidden[i](x)
            x = self.hidden[i](x)

        x = self.output(x)
        x = self.sigmoid(x)
        x = self.softmax(x)

        return x

    def predict(self, x):
        x = x * self.x_scale + self.x_translation
        return self(x)
