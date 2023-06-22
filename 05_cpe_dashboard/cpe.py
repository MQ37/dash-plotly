import random

class CPE:
    """
    Třída pro simulaci CPE zařízení.
    Hodnoty:
    - rssi: síla signálu
    - sinr: signal to noise ratio
    - n_clients: počet klientů připojených k CPE
    - channels: počet klientů na jednotlivých kanálech
    - channel: aktuální kanál
    """

    def __init__(self):
        self.rssi : float = random.uniform(-70, -30)
        self.sinr : float = random.uniform(5, 25)
        self.n_clients : int= random.randint(1, 8)
        self.channels : list[int] = [random.randint(0, 4) for _ in range(13)]
        self.channel : int = random.randint(1, 13)

    def get_rssi(self) -> float:
        self.rssi = random.uniform(self.rssi-2, self.rssi+2)
        if self.rssi > -30:
            self.rssi = -30
        if self.rssi < -70:
            self.rssi = -70
        return self.rssi

    def get_sinr(self) -> float:
        self.sinr = random.uniform(self.sinr-0.5, self.sinr+0.5)
        if self.sinr > 25:
            self.sinr = 25
        if self.sinr < -5:
            self.sinr = -5
        return self.sinr

    def get_wifi_score(self) -> float:
        min_rssi = -90
        max_rssi = -30
        rssi_percent = (self.rssi - min_rssi) / (max_rssi - min_rssi) * 100 + 5

        min_sinr = -5 
        max_sinr = 25
        sinr_percent = (self.sinr - min_sinr) / (max_sinr - min_sinr) * 100 + 5

        score = (rssi_percent + sinr_percent) / 2
        if score > 100:
            return 100
        return score

    def get_n_clients(self) -> int:
        self.n_clients += random.randint(-1, 1)
        if self.n_clients < 0:
            self.n_clients = 0
        return self.n_clients

    def get_channels(self) -> list[int]:
        for ch in range(13):
            if random.random() < 0.8:
                continue

            rn = random.randint(-1, 1)
            if self.channels[ch] + rn < 0:
                continue

            self.channels[ch] += rn

        return self.channels

    def get_current_channel(self) -> int:
        return self.channel
