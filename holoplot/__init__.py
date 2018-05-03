import holoviews as _hv
from holoviews.ipython import display # noqa

from bokeh.io import export_png as _export_png, show as _show, save as _save
from bokeh.resources import CDN as _CDN

from .converter import HoloViewsConverter

renderer = _hv.renderer('bokeh')

# Register plotting interfaces
def _patch_plot(self):
    return HoloPlot(self)


def patch(library, extension=None):
    """
    Patch library to support HoloViews based plotting API.
    """
    if not isinstance(library, list): library = [library]
    if 'streamz' in library:
        try:
            import streamz.dataframe as sdf
        except ImportError:
            raise ImportError('Could not patch plotting API onto streamz. '
                              'Streamz could not be imported.')
        sdf.DataFrame.plot = property(_patch_plot)
        sdf.DataFrames.plot = property(_patch_plot)
        sdf.Series.plot = property(_patch_plot)
        sdf.Seriess.plot = property(_patch_plot)
    if 'pandas' in library:
        try:
            import pandas as pd
        except:
            raise ImportError('Could not patch plotting API onto pandas. '
                              'Pandas could not be imported.')
        pd.DataFrame.plot = property(_patch_plot)
        pd.Series.plot = property(_patch_plot)
    if 'dask' in library:
        try:
            import dask.dataframe as dd
        except:
            raise ImportError('Could not patch plotting API onto dask. '
                              'Dask could not be imported.')
        dd.DataFrame.plot = property(_patch_plot)
        dd.Series.plot = property(_patch_plot)
    if 'intake' in library:
        try:
            from intake.source.base import DataSource
        except ImportError:
            raise ImportError('Could not patch plotting API onto intake. '
                              'Intake could not be imported.')
        DataSource.plot = property(_patch_plot)
    if 'xarray' in library:
        try:
            from xarray import DataArray
        except ImportError:
            raise ImportError('Could not patch plotting API onto xarray. '
                              'Xarray could not be imported.')
        DataArray.plot = property(_patch_plot)
    if extension and not _hv.extension._loaded:
        _hv.extension(extension, logo=logo)


class HoloPlot(object):

    def __init__(self, data, **metadata):
        self._data = data
        self._metadata = metadata

    def __call__(self, x=None, y=None, kind=None, **kwds):
        params = dict(self._metadata, **kwds)
        converter = HoloViewsConverter(
            self._data, x, y, kind=kind, **params
        )
        return converter(kind, x, y)

    def line(self, x=None, y=None, **kwds):
        """
        Line plot

        Parameters
        ----------
        x, y : string, optional
            Field name to draw x- and y-positions from
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='line', **kwds)

    def scatter(self, x=None, y=None, **kwds):
        """
        Scatter plot

        Parameters
        ----------
        x, y : string, optional
            Field name to draw x- and y-positions from
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='scatter', **kwds)

    def area(self, x=None, y=None, stacked=False, **kwds):
        """
        Area plot

        Parameters
        ----------
        x, y : string, optional
            Field name to draw x- and y-positions from
        stacked : boolean
            Whether to stack multiple areas
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='area', stacked=stacked, **kwds)

    def heatmap(self, x=None, y=None, C=None, **kwds):
        """
        HeatMap plot

        Parameters
        ----------
        x, y : string, optional
            Field name to draw x- and y-positions from
        C : string
            Field to draw heatmap color from
        reduce_function : function
            Function to compute statistics for heatmap
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='heatmap', C=C, **kwds)

    def hexbin(self, x=None, y=None, C=None, **kwds):
        """
        HexBin plot

        Parameters
        ----------
        x, y : string, optional
            Field name to draw x- and y-positions from
        C : string
            Field to draw heatmap color from
        reduce_function : function
            Function to compute statistics for hexbins
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='hexbin', C=C, **kwds)

    def bar(self, x=None, y=None, **kwds):
        """
        Bars plot

        Parameters
        ----------
        x, y : string, optional
            Field name to draw x- and y-positions from
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='bar', **kwds)

    def barh(self, x=None, y=None, **kwds):
        """
        Horizontal bar plot

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='barh', **kwds)

    def box(self, y=None, **kwds):
        """
        Boxplot

        Parameters
        ----------
        by : string or sequence
            Column in the DataFrame to group by.
        kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(kind='box', x=None, y=y, **dict(kwds, hover=False))

    def violin(self, y=None, **kwds):
        """
        Boxplot

        Parameters
        ----------
        by : string or sequence
            Column in the DataFrame to group by.
        kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(kind='violin', x=None, y=y, **dict(kwds, hover=False))

    def hist(self, y=None, **kwds):
        """
        Histogram

        Parameters
        ----------
        by : string or sequence
            Column in the DataFrame to group by.
        kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(kind='hist', x=None, y=y, **kwds)

    def kde(self, y=None, **kwds):
        """
        KDE

        Parameters
        ----------
        by : string or sequence
            Column in the DataFrame to group by.
        kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(kind='kde', x=None, y=y, **kwds)

    def table(self, columns=None, **kwds):
        """
        Table

        Parameters
        ----------
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(kind='table', **dict(kwds, columns=columns))

    def image(self, x=None, y=None, **kwds):
        """
        Image plot

        Parameters
        ----------
        x, y : label or position, optional
            Field name to draw x- and y-positions from
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='image', **kwds)

    def quadmesh(self, x=None, y=None, **kwds):
        """
        QuadMesh plot

        Parameters
        ----------
        x, y : label or position, optional
            Field name to draw x- and y-positions from
        **kwds : optional
            Keyword arguments to pass on to
            :py:meth:`holoplot.converter.HoloViewsConverter`.
        Returns
        -------
        HoloViews object: Object representing the requested visualization
        """
        return self(x, y, kind='quadmesh', **kwds)



def save(obj, filename, title=None, resources=None):
    """
    Saves HoloViews objects and bokeh plots to file.

    Parameters
    ----------
    obj : HoloViews object
       HoloViews object to export
    filename : string
       Filename to save the plot to
    title : string
       Optional title for the plot
    resources: bokeh resources
       One of the valid bokeh.resources (e.g. CDN or INLINE)
    """
    if isinstance(obj, _hv.Dimensioned):
        plot = renderer.get_plot(obj).state
    else:
        raise ValueError('%s type object not recognized and cannot be saved.' %
                         type(obj).__name__)

    if filename.endswith('png'):
        _export_png(plot, filename=filename)
        return
    if not filename.endswith('.html'):
        filename = filename + '.html'

    if title is None:
        title = 'HoloPlot Plot'
    if resources is None:
        resources = _CDN

    if obj.traverse(lambda x: x, [_hv.HoloMap]):
        renderer.save(plot, filename)
    else:
        _save(plot, filename, title=title, resources=resources)


def show(obj):
    """
    Displays HoloViews objects in and outside the notebook

    Parameters
    ----------
    obj : HoloViews object
       HoloViews object to export
    """
    if not isinstance(obj, _Dimensioned):
        raise ValueError('%s type object not recognized and cannot be shown.' %
                         type(obj).__name__)

    if obj.traverse(lambda x: x, [_HoloMap]):
        renderer.app(obj, show=True, new_window=True)
    else:
        _show(renderer.get_plot(obj).state)
