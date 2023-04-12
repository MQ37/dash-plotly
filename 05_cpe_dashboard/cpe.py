import random

class CPE:
    def __init__(self):
        self.rssi = random.randint(-70, -30)
        self.sinr = random.uniform(5, 25)
        self.n_clients = random.randint(1, 8)

    def get_rssi(self):
        self.rssi = random.randint(self.rssi-2, self.rssi+2)
        return self.rssi

    def get_sinr(self):
        self.sinr = random.uniform(self.sinr-0.5, self.sinr+0.5)
        return self.sinr

    def get_wifi_score(self):
        min_rssi = -90
        max_rssi = -30
        rssi_percent = (self.rssi - min_rssi) / (max_rssi - min_rssi) * 100 + 5

        min_sinr = 25
        max_sinr = -5
        sinr_percent = (self.sinr - min_sinr) / (max_sinr - min_sinr) * 100 + 5

        score = (rssi_percent + sinr_percent) / 2
        if score <= 100:
            return score
        else:
            return 100

    def get_n_clients(self):
        self.n_clients += random.randint(-1, 1)
        if self.n_clients < 0:
            self.n_clients = 0
        return self.n_clients
