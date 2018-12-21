from matplotlib import pyplot as pt
import matplotlib.ticker as mticker

class PlotDrawer:

    def drawStats(self, stats):
        print('drawing stats')
        _, axes = pt.subplots(nrows=1, ncols=len(stats), sharex=False)

        pt.setp(axes[0].get_xticklabels(), visible=True, rotation=90)
        for (i, stat) in enumerate(stats):
            stat._statData.plot(ax=axes[i], kind=stat._statKind)
            axes[i].yaxis.set_label_text(stat._name)
            axes[i].xaxis.set_ticklabels(axes[i].get_xticklabels())
            if stat._yaxisFormatter is 'percent':
                axes[i].yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

        #pt.tight_layout()
        pt.show()
