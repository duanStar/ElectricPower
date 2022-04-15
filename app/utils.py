"""
    Here we defined the details of each model in this system.

    For reports, these info can be used in that situation and it could be
    fine with the global view of this analysis system.
"""


class ModelDetails:
    def __init__(self):
        self.expert_collections = ['prediction', 'visualize']
        self.IO_type = ('number', 'series', 'dataframe', 'excel', 'csv', 'tsv')


class ARIMA(ModelDetails):
    """ Class of ARIMA Details. For Reports. """
    def __init__(self):
        super().__init__()
        self.name = 'ARIMA'
        self.params = {
            'input': self.IO_type[1],
            'output': self.IO_type[1]
        }
        self.expert = self.expert_collections[0]
        self.introduction = """ARIMA(Auto Regressive Integrate Moving AverageModel) 差分自回归移动平均模型是在 ARMA 模型的基础上进行改造的，ARMA 模型是针对 t 期值进行建模的，而 ARIMA 是针对 t 期与 t d 期之间差值进行建模，这种不同期之间做差 即 为差分。 ARIMA 模型也是基于平稳的时间序列的或者差分化后是稳定的。"""

    def __call__(self):
        return {
            "name": self.name,
            "input": self.params['input'],
            "output": self.params['output'],
            "solve_field": self.expert,
            "intro": self.introduction
        }


if __name__ == '__main__':

    # Example for usage.

    ALL_MODELS = {'ARIMA': ARIMA(), }
    print(ALL_MODELS['ARIMA']())
