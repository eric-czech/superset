
import os
from superset.viz import LocalFileViz, config
import seaborn as sns
import matplotlib.pyplot as plt
from flask_babel import lazy_gettext as _


class MatplotlibImageViz(LocalFileViz):

    """Matplotlib Viz"""

    credits = ''
    is_timeseries = False

    def get_figure_data(self, fig):
        fig_path = config.get('MATPLOTLIB_CACHE_PATH')
        fig_dir = config.get('MATPLOTLIB_CACHE_DIR')
        filename = self.get_filename('png')
        filepath = os.path.join(fig_dir, filename)
        fig.savefig(filepath)
        url = os.path.join(os.path.sep + fig_path, filename)
        return {'url': url}


class SeabornScatterMatrixViz(MatplotlibImageViz):

    viz_type = "seaborn_scattermatrix"
    verbose_name = _("Seaborn Scatter Matrix")
    is_timeseries = False
    credits = ('')
    fieldsets = ({
        'label': None,
        'fields': (
            'groupby',
            'columns',
            #'color_field',
            'metric'
        )
    }, {
        'label': _('Scatter Matrix Options'),
        'fields': (
            'row_limit',
            'color_log_scale',
            'normalize_across'
        )
    },)

    def query_obj(self):
        d = super(SeabornScatterMatrixViz, self).query_obj()
        fd = self.form_data
        d['metrics'] = [fd.get('metric')]
        d['groupby'] = fd.get('groupby') + fd.get('columns')
        return d

    def get_scatter_matrix_fig(self, d, hue):

        def plot_scatter(x, y, **kwargs):
            is_na = x.isnull() | y.isnull()
            return plt.scatter(x[~is_na], y[~is_na], alpha=.8, c=kwargs['color'], label=kwargs['label'])

        def plot_diag(x, **kwargs):
            return plt.hist(x.dropna(), bins=30, label=kwargs['label'], alpha=.5)

        g = sns.PairGrid(d, diag_sharey=False, hue=hue, dropna=False)
        g.map_offdiag(plot_scatter)
        g.map_diag(plot_diag)
        g.add_legend()
        return g.fig

    def get_data(self):
        df = self.get_df()
        fd = self.form_data
        x = fd.get('groupby')
        y = fd.get('columns')
        v = fd.get('metric')
        #s = fd.get('color_field')
        s = 'DRUG_NAME_MGDS'
        df = df[x + y + [v]]

        df = df.pivot_table(index=x, columns=y, values=v)

        def collapse(c):
            return c if isinstance(c, str) else '_'.join(c)
        df.columns = [collapse(c) for c in df.columns]
        series_col = '__SERIES__'
        df[series_col] = df.index.get_level_values(s)

        series_limit = 5
        series_values = df[series_col].unique()[:series_limit]
        df = df[df[series_col].isin(series_values)]

        df = df.reset_index(drop=True)
        fig = self.get_scatter_matrix_fig(df, series_col)
        return self.get_figure_data(fig)