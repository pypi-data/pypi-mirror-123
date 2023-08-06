import pandas as pd

from .report import Report


def plot_holdings(report: Report, *, freq: str = '1h') -> None:
    holding_sample = report.holdings.resample(freq).asfreq()
    holding_sample.where(holding_sample > 0., 0.).plot.area()


def plot_cost_proceeds(report: Report) -> None:
    df = pd.DataFrame({'Cost': report.costs, 'Proceeds': report.proceeds})
    df.plot.scatter(x='Cost', y='Proceeds')
