import numpy as np
from sklearn.metrics import auc, roc_curve

__all__ = [
    'plot_anomaly_score',
    'plot_roc_curve',
    'plot_graphical_model',
    'plot_partial_corrcoef'
]

# TODO: Implement plot_featurewise_anomaly_score function
# TODO: Update plot_anomaly_score function so that a gaussian kernel density
# estimate can be plotted


def plot_anomaly_score(
    anomaly_score, ax=None, bins='fd', figsize=None,
    filepath=None, grid=True, hist=True, threshold=None,
    title=None, xlabel='Samples', xlim=None, ylabel='Anomaly score',
    ylim=None, **kwargs
):
    """Plot the anomaly score for each sample.

    Parameters
    ----------
    anomaly_score : array-like of shape (n_samples,)
        Anomaly score for each sample.

    ax : matplotlib Axes, default None
        Target axes instance.

    bins : int, str or array-like, default 'fd'
        Number of hist bins.

    figsize : tuple, default None
        Tuple denoting figure size of the plot.

    filepath : str, default None
        If provided, save the current figure.

    grid : bool, default True
        If True, turn the axes grids on.

    hist : bool, default True
        If True, plot a histogram of anomaly scores.

    threshold : float, default None
        Threshold.

    title : string, default None
        Axes title. To disable, pass None.

    xlabel : string, default 'Samples'
        X axis title label. To disable, pass None.

    xlim : tuple, default None
        Tuple passed to `ax.xlim`.

    ylabel : string, default 'Anomaly score'
        Y axis title label. To disable, pass None.

    ylim : tuple, default None
        Tuple passed to `ax.ylim`.

    **kwargs : dict
        Other keywords passed to `ax.plot`.

    Returns
    -------
    ax : matplotlib Axes
        Axes on which the plot was drawn.

    Examples
    --------
    .. image:: images/plot_anomaly_score.png
    """

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    n_samples,    = anomaly_score.shape
    xlocs         = np.arange(n_samples)

    if ax is None:
        _, ax     = plt.subplots(figsize=figsize)

    if xlim is None:
        xlim      = (0., n_samples - 1.)

    if ylim is None:
        ylim      = (0., 1.1 * np.max(anomaly_score))

    if title is not None:
        ax.set_title(title)

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if threshold is not None:
        ax.hlines(threshold, xlim[0], xlim[1])

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(grid, linestyle=':')
    ax.plot(xlocs, anomaly_score, **kwargs)

    if hist:
        # Create an axes on the right side of ax
        divider   = make_axes_locatable(ax)
        ax_hist_y = divider.append_axes(
            'right', size='20%', pad=0.1, sharey=ax
        )

        ax_hist_y.set_ylim(ylim)
        ax_hist_y.yaxis.set_tick_params(labelleft=False)
        ax_hist_y.grid(grid, linestyle=':')
        ax_hist_y.hist(
            anomaly_score, bins=bins, density=True, orientation='horizontal'
        )

    if filepath is not None:
        ax.figure.savefig(filepath)

    return ax


def plot_roc_curve(
    y_true, y_score, ax=None, figsize=None,
    filepath=None, grid=True, label=None, title=None,
    xlabel='FPR', ylabel='TPR', **kwargs
):
    """Plot the Receiver Operating Characteristic (ROC) curve.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        True Labels.

    y_score : array-like of shape (n_samples,)
        Target scores.

    ax : matplotlib Axes, default None
        Target axes instance.

    figsize : tuple, default None
        Tuple denoting figure size of the plot.

    filepath : str, default None
        If provided, save the current figure.

    grid : bool, default True
        If True, turn the axes grids on.

    label : str, default None
        Legend label.

    title : string, default None
        Axes title. To disable, pass None.

    xlabel : string, default 'FPR'
        X axis title label. To disable, pass None.

    ylabel : string, default 'TPR'
        Y axis title label. To disable, pass None.

    **kwargs : dict
        Other keywords passed to `ax.plot`.

    Returns
    -------
    ax : matplotlib Axes
        Axes on which the plot was drawn.

    Examples
    --------
    .. image:: images/plot_roc_curve.png
    """

    import matplotlib.pyplot as plt

    fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=-1)
    roc_auc     = auc(fpr, tpr)

    if ax is None:
        _, ax   = plt.subplots(figsize=figsize)

    if label is None:
        label   = f'area={roc_auc:1.3f}'

    if title is not None:
        ax.set_title(title)

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    ax.set_xlim(0., 1.)
    ax.set_ylim(0., 1.05)
    ax.grid(grid, linestyle=':')
    ax.plot(fpr, tpr, label=label, **kwargs)
    ax.legend(loc='lower right')

    if filepath is not None:
        ax.figure.savefig(filepath)

    return ax


def plot_graphical_model(
    partial_corrcoef, ax=None, cmap='Spectral', figsize=None,
    filepath=None, random_state=None, title='GGM', **kwargs
):
    """Plot the Gaussian Graphical Model (GGM).

    Parameters
    ----------
    partial_corrcoef : array-like of shape (n_features, n_features)
        Partial correlation coefficient matrix.

    ax : matplotlib Axes, default None
        Target axes instance.

    cmap : str or matplotlib Colormap, default 'Spectral'
        Colormap or Registered colormap name.

    figsize : tuple, default None
        Tuple denoting figure size of the plot.

    filepath : str, default None
        If provided, save the current figure.

    random_state : int, RandomState instance, default None
        Seed of the pseudo random number generator.

    title : string, default 'GGM'
        Axes title. To disable, pass None.

    **kwargs : dict
        Other keywords passed to `nx.draw_networkx`.

    Returns
    -------
    ax : matplotlib Axes
        Axes on which the plot was drawn.

    Examples
    --------
    .. image:: images/plot_graphical_model.png
    """

    import matplotlib.pyplot as plt
    import networkx as nx

    if ax is None:
        _, ax           = plt.subplots(figsize=figsize)

    if title is not None:
        ax.set_title(title)

    tril                = np.tril(partial_corrcoef)
    G                   = nx.from_numpy_matrix(tril)

    try:
        pos             = nx.nx_agraph.graphviz_layout(G)
    except ImportError:
        pos             = nx.spling_layout(G, random_state=random_state)

    # Add the draw_networkx kwargs here
    kwargs['node_size'] = np.array([10. * (d + 1.) for _, d in G.degree])
    kwargs['width']     = np.abs(tril.flat[tril.flat[:] != 0.])

    # Draw the Gaussian grapchical model
    nx.draw_networkx(G, pos=pos, ax=ax, cmap=cmap, **kwargs)

    # Turn off tick visibility
    ax.xaxis.set_tick_params(labelbottom=False, bottom=False)
    ax.yaxis.set_tick_params(labelleft=False, left=False)

    if filepath is not None:
        ax.figure.savefig(filepath)

    return ax


def plot_partial_corrcoef(
    partial_corrcoef, ax=None, cbar=True, cmap='RdBu',
    figsize=None, filepath=None, linecolors='white', linewidths=0.5,
    title='Partial correlation', **kwargs
):
    """Plot the partial correlation coefficient matrix.

    Parameters
    ----------
    partial_corrcoef : array-like of shape (n_features, n_features)
        Partial correlation coefficient matrix.

    ax : matplotlib Axes, default None
        Target axes instance.

    cbar : bool, default True.
        Whether to draw a colorbar.

    cmap : str or matplotlib Colormap, default 'RdBu'
        Colormap or Registered colormap name.

    figsize : tuple, default None
        Tuple denoting figure size of the plot.

    filepath : str, default None
        If provided, save the current figure.

    linecolor : str, default 'white'
        Color of the lines that will divide each cell.

    linewidths : float, default 0.5
        Width of the lines that will divide each cell.

    title : string, default 'Partial correlation'
        Axes title. To disable, pass None.

    **kwargs : dict
        Other keywords passed to `ax.pcolormesh`.

    Returns
    -------
    ax : matplotlib Axes
        Axes on which the plot was drawn.

    Examples
    --------
    .. image:: images/plot_partial_corrcoef.png
    """

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    if ax is None:
        _, ax      = plt.subplots(figsize=figsize)

    if title is not None:
        ax.set_title(title)

    # Add the pcolormesh kwargs here
    kwargs['vmin'] = -1.
    kwargs['vmax'] = 1.

    # Draw the heatmap
    mesh           = ax.pcolormesh(
        np.ma.masked_equal(partial_corrcoef, 0.),
        cmap       = cmap,
        edgecolors = linecolors,
        linewidths = linewidths,
        **kwargs
    )

    ax.set_aspect('equal')
    ax.set_facecolor('grey')

    # Invert the y axis to show the plot in matrix form
    ax.invert_yaxis()

    if cbar:
        # Create an axes on the right side of ax
        divider    = make_axes_locatable(ax)
        cax        = divider.append_axes('right', size='5%', pad=0.1)

        ax.figure.colorbar(mesh, cax=cax)

    if filepath is not None:
        ax.figure.savefig(filepath)

    return ax
