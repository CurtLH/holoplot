import pandas as pd
from holoplot import HoloPlot, patch
from holoviews import Store, Scatter
from holoviews.element.comparison import ComparisonTestCase


class TestDefaults(ComparisonTestCase):

    def setUp(self):
        patch('pandas')
        self.df = pd.DataFrame([[1, 2], [3, 4], [5, 6]], columns=['x', 'y'])

    def test_define_default_options(self):
        holoplot = HoloPlot(self.df, width=42, height=42)
        curve = holoplot(y='y')
        opts = Store.lookup_options('bokeh', curve, 'plot')
        self.assertEqual(opts.options.get('width'), 42)
        self.assertEqual(opts.options.get('height'), 42)

    def test_define_custom_method(self):
        holoplot = HoloPlot(self.df, {'custom_scatter': {'width': 42, 'height': 42}})
        custom_scatter = holoplot.custom_scatter(y='y')
        scatter = holoplot.scatter(y='y')
        custom_opts = Store.lookup_options('bokeh', custom_scatter, 'plot')
        opts = Store.lookup_options('bokeh', scatter, 'plot')
        self.assertEqual(custom_opts.options.get('width'), 42)
        self.assertEqual(custom_opts.options.get('height'), 42)
        self.assertNotEqual(opts.options.get('width'), 42)
        self.assertNotEqual(opts.options.get('height'), 42)

    def test_define_customize_method(self):
        holoplot = HoloPlot(self.df, {'scatter': {'width': 42, 'height': 42}})
        custom_scatter = holoplot.scatter(y='y')
        curve = holoplot.line(y='y')
        custom_opts = Store.lookup_options('bokeh', custom_scatter, 'plot')
        opts = Store.lookup_options('bokeh', curve, 'plot')
        self.assertEqual(custom_opts.options.get('width'), 42)
        self.assertEqual(custom_opts.options.get('height'), 42)
        self.assertNotEqual(opts.options.get('width'), 42)
        self.assertNotEqual(opts.options.get('height'), 42)

    def test_attempt_to_override_kind_on_method(self):
        holoplot = HoloPlot(self.df, {'scatter': {'kind': 'line'}})
        self.assertIsInstance(holoplot.scatter(y='y'), Scatter)
