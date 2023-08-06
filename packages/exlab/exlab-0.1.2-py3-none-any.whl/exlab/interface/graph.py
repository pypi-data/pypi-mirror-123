# from exlab.remote.server import Server
import math

from exlab.utils.io import parameter

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def display(*graphes):
    return Visual().display(*graphes)


class Visual(object):
    def __init__(self, server=None):
        # self.server = server if server else Server()
        pass

    def display(self, *graphes):
        flat = []
        for graph in graphes:
            if isinstance(graph, list):
                flat += graph
            else:
                flat.append(graph)
        graphes = flat

        self.subconf, self.subfigsize = self.createSubConf(graphes)
        self.fig = plt.figure(figsize=(8, 8))
        for i, graph in enumerate(graphes):
            vax = self.createAxis(graph, i)
            graph.display(vax)
            vax.ax.legend()
    
    def createAxis(self, graph, i):
        kwargs = {}
        if graph.dim() >= 3:
            kwargs['projection'] = '3d'
        ax = self.fig.add_subplot(*self.subconf, i + 1, **kwargs)
        vax = VisualAxis(self, ax)

        if graph.ratio == 'square':
            ax.set_aspect('equal')

        ax.yaxis.set_major_formatter(
            mpl.ticker.StrMethodFormatter('{x:,.2f}'))
        ax.grid(True)

        return vax
    
    def createSubConf(self, graphes):
        number = len(graphes)
        # horizontals = len(list(graph for graph in graphes if graph.ratio == 'horizontal'))
        # verticals = len(list(graph for graph in graphes if graph.ratio == 'vertical'))
        m = 1
        while number > m ** 2:
            m += 1
        n = math.ceil(number / m)

        return ((n, m), (15, 15))


class VisualAxis(object):
    def __init__(self, visual, ax):
        self.visual = visual
        self.ax = ax


class Graph(object):
    def __init__(self, *items, title=None, ratio=None, options=None):
        super().__init__()
        self.items = list(items)
        options = parameter(options, {})

        self.range = options.get('range')
        self.title = title
        self.ratio = ratio  # can be 'square', 'horizontal', 'vertical'

    def __add__(self, other):
        return self.__class__(*(self.items + other.items))

    def display(self, visual):
        plt.title(self.title)

        for item in self.items:
            item.display(visual)

    def plot(self, *args, **kwargs):
        self.items.append(PlotItem(*args, **kwargs))
        return self
    
    def scatter(self, *args, **kwargs):
        self.items.append(ScatterItem(*args, **kwargs))
        return self
    
    def arrow(self, *args, **kwargs):
        self.items.append(ArrowItem(*args, **kwargs))
        return self
    
    def rectangle(self, *args, **kwargs):
        kwargs['shape'] = 'rectangle'
        self.items.append(PatchItem(*args, **kwargs))
        return self
    
    def dim(self):
        return max((item.dim for item in self.items))


class GraphItem(object):
    def __init__(self):
        pass

    def display(self, visual):
        pass

    def convertData(self, data):
        if data is None:
            return data
        if isinstance(data, np.ndarray):
            return data
        elif isinstance(data, list):
            if len(data) > 0 and hasattr(data[0], 'plain'):
                return np.array([item.plain() for item in data])
            else:
                return np.array(data)
        return np.array(data)


class PlotItem(GraphItem):
    def __init__(self, *data, **options):
        super().__init__()
        self.data = data
        self.dim = len(self.data)
        self.options = options
    
    def display(self, plotter):
        plt.xlabel('Iteration')
        if self.dim == 1:
            plotter.ax.plot(self.data[0])
        elif self.dim == 2:
            plotter.ax.plot(self.data[0], self.data[1])


class ScatterItem(GraphItem):
    def __init__(self, points, **options):
        super().__init__()
        self.data = self.convertData(points)
        self.dim = self.data.shape[1]
        self.options = options
        if 'color' in options and not isinstance(self.options['color'], str):
            self.options['color'] = self.convertData(self.options['color'])

    def display(self, plotter):
        label = self.options.get('label')
        color = self.options.get('color')
        alpha = self.options.get('alpha')
        marker = self.options.get('marker')

        options = {'label': label, 'c': color, 'alpha': alpha, 'marker': marker}
        if self.dim == 1:
            plotter.ax.scatter(self.data[:, 0],
                               **options)
        elif self.dim == 2:
            plotter.ax.scatter(self.data[:, 0], self.data[:, 1],
                               **options)
        elif self.dim >= 2:
            plotter.ax.scatter(self.data[:, 0], self.data[:, 1], self.data[:, 2],
                               **options)


class ArrowItem(GraphItem):
    def __init__(self, data, **options):
        super().__init__()
        self.data = self.convertData(data)
        self.dim = self.data.shape[2]
        self.options = options
        if 'color' in options:
            self.options['color'] = self.convertData(self.options['color'])
        if 'colorMap' in options:
            self.options['colorMap'] = self.convertData(self.options['colorMap'])

    def display(self, plotter):
        label = self.options.get('label')
        color = self.options.get('color')
        colorMap = self.options.get('colorMap')
        for i, data in enumerate(self.data):
            if color is None and colorMap is not None:
                color = colorMap[i]
            if self.dim == 2:
                plotter.ax.arrow(data[0, 0], data[0, 1], data[1, 0], data[1, 1],
                                 label=label, color=color, head_width=0.5)
        plotter.ax.set_xlim([200, 600])
        plotter.ax.set_ylim([200, 600])


class PatchItem(GraphItem):
    def __init__(self, position, width, height, shape='rectangle', **options):
        super().__init__()
        self.position = position
        self.width = width
        self.height = height
        self.shape = shape

        self.dim = 2
        self.options = options

    def display(self, plotter):
        if self.shape == 'rectangle':
            borders = (False, True) if self.options.get('border') else (False)
            for border in borders:
                plotter.ax.add_patch(patches.Rectangle(self.position,
                                                    self.width,
                                                    self.height,
                                                    alpha=.5 if border else self.options.get('alpha'),
                                                    zorder=self.options.get('zorder'),
                                                    fill=not border))
