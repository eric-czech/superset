
import numpy as np


def plotly_scattermatrix(
        df, series, diag='histogram', size=4, height=500, width=500,
        title='Scatter Matrix', barmode='stack', include_index_as_text=True):
    from plotly.graph_objs import graph_objs
    from plotly.tools import make_subplots, DEFAULT_PLOTLY_COLORS

    dim = len(df.columns)
    fig = make_subplots(rows=dim, cols=dim)
    cols = df.select_dtypes(include=[np.float64, np.int64]).columns.tolist()

    colormap = {}
    colorlist = DEFAULT_PLOTLY_COLORS
    for i, v in enumerate(np.unique(series)):
        j = i % len(colorlist)
        colormap[v] = colorlist[j]

    for j, y in enumerate(cols):
        for i, x in enumerate(cols):
            d = df[np.unique([x, y]).tolist()]
            if x == y:
                for s, g in d[[x]].groupby(series):
                    v = g[x].dropna()
                    trace = graph_objs.Histogram(
                        x=v.values,
                        showlegend=False,
                        marker=dict(color=colormap[s]),
                        name=s,
                        nbinsx=30
                    )
                    fig.append_trace(trace, i + 1, j + 1)
                    if j == 0:
                            fig['layout'][trace['yaxis'].replace('y', 'yaxis')].update(title=x)
                    if i == dim - 1:
                        fig['layout'][trace['xaxis'].replace('x', 'xaxis')].update(title=y)
            else:
                for s, g in d[[x, y]].groupby(series):
                    v = g[[x, y]].dropna()
                    trace = graph_objs.Scatter(
                        x=v[x].values,
                        y=v[y].values,
                        mode='markers',
                        marker=dict(color=colormap[s]),
                        showlegend=False,
                        name=s,
                        text=(v.index.values if include_index_as_text else None)
                    )
                    fig.append_trace(trace, i + 1, j + 1)
                    if j == 0:
                        fig['layout'][trace['yaxis'].replace('y', 'yaxis')].update(title=x)
                    if i == dim - 1:
                        fig['layout'][trace['xaxis'].replace('x', 'xaxis')].update(title=y)

    print('Scatter fig data len: ', len(fig['data']))

    # for i in range(dim):
    #     xaxis_key = 'xaxis{}'.format((dim * dim) - dim + 1 + i)
    #     fig['layout'][xaxis_key].update(title=cols[i])
    #     yaxis_key = 'yaxis{}'.format(1 + (dim * i))
    #     fig['layout'][yaxis_key].update(title=cols[i])

    fig['layout'].update(
        height=height, width=width,
        title=title,
        showlegend=False,
        barmode=barmode,
        hovermode='closest'
    )
    return fig