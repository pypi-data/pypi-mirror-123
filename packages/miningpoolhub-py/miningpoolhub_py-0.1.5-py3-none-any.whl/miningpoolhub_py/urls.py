class Urls:
    def __init__(self):
        self.protocol = 'https://'
        self.base_url = 'miningpoolhub.com/index.php?page=api&action={action}'
        self.coin_pool = '{coin_pool}.'
        self.pool_base_url = self.protocol + "{coin_pool}." + self.base_url
        self.no_pool_base_url = self.protocol + self.base_url

        # Urls specific to each coins' mining pool
        self.get_dashboard_data = self.protocol + self.coin_pool + self.base_url.format(action='getdashboarddata')
        self.get_hourly_hash_rates = self.protocol + self.coin_pool + self.base_url.format(action='gethourlyhashrates')

        # Info for all mining pools
        self.get_mining_profit_and_statistics = self.no_pool_base_url.format(action='getminingandprofitsstatistics')
        self.get_auto_switching_and_profits_statistics =\
            self.no_pool_base_url.format(action='getautoswitchingandprofitsstatistics')
        self.public = self.no_pool_base_url.format(action='public')

    def base_url(self):
        return self.base_url

    def get_dashboard_data_url(self, pool):
        return self.get_dashboard_data.format(coin_pool=pool)

    def get_hourly_hash_rates_url(self, pool):
        return self.get_hourly_hash_rates.format(coin_pool=pool)

    def get_mining_profit_and_statistics_url(self):
        return self.get_mining_profit_and_statistics

    def get_auto_switching_and_profits_statistics_url(self):
        return self.get_auto_switching_and_profits_statistics

    def public_url(self):
        return self.public
