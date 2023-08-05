from nns import ContactClassification, ElasticRegression1
from data_sets import CapElastoplasticDataset, CapElasticDataset, CapContactDataset
import torch


class PistonVTaper:
    def __init__(self, ):
        self.disp = 0

        self.contact_dset = CapContactDataset('./data/processed_test_data.csv')

        self.contact_model = ContactClassification(3,
                                                   8,
                                                   3,
                                                   self.contact_dset.translate,
                                                   self.contact_dset.scale,
                                                   n_hidden_layers=0)

        state_dict = torch.load("./data/contact_mid_dim_8_n_hidden_0.pth", map_location=torch.device('cpu'))
        self.contact_model.load_state_dict(state_dict)

        self.elastic_dest = CapElasticDataset('./data/processed_test_data.csv')

        self.elastic_force_model = ElasticRegression1(n_mid=3, n_hidden_layers=0)
        state_dict = torch.load("./data/elastic_mid_dim_3_n_hidden_0.pth")
        self.elastic_force_model.load_state_dict(state_dict)

        self.elastoplastic_dest = CapElastoplasticDataset('./data/processed_test_data.csv')

        self.elastoplastic_force_model = ElasticRegression1(n_mid=3, n_hidden_layers=0)
        state_dict = torch.load("./data/elastoplastic_mid_dim_3_n_hidden_0.pth")
        self.elastoplastic_force_model.load_state_dict(state_dict)

    def inc(self, x, v, dt, detail=False):

        features = torch.Tensor([[x, self.disp, v]])

        contact_features = self.contact_dset.to_x_tilde(features)
        contact = self.contact_model(contact_features)

        _, predicted = torch.max(contact.data, 1)
        predicted = int(predicted)

        if predicted == 0:
            if detail:
                return 0, 0, self.disp, predicted
            else:
                return 0
        elif predicted == 1:
            elastic_features = self.elastic_dest.to_x_tilde(features)
            [force, ddisp_dt] = \
            self.elastic_dest.from_y_tilde(self.elastic_force_model(elastic_features).detach().numpy())[0]
        elif predicted == 2:
            elastoplastic_features = self.elastoplastic_dest.to_x_tilde(features)
            [force, ddisp_dt] = self.elastoplastic_dest.from_y_tilde(
                self.elastoplastic_force_model(elastoplastic_features).detach().numpy())[0]
        else:
            raise Exception(f'Invalid contact result: {predicted}')

        self.disp += ddisp_dt * dt

        if detail:
            return force, ddisp_dt, self.disp, predicted
        else:
            return force

