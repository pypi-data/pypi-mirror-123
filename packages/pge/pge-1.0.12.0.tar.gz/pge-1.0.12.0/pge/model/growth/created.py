from pge.model.growth.bsc.ca import CAGrowth
from pge.model.growth.bsc.delete import FixUnGrowth, FixDegGrowth, FixClustGrowth
from pge.model.growth.bsc.pa import PAGrowth
from pge.model.growth.bsc.simple import SimpleGrowth


class PASchemaFreeEvolve(PAGrowth):
    def __init__(self, graph, deg, params, schema):
        PAGrowth.__init__(self, graph, deg, params, schema)


class CAFixUniEvolve(SimpleGrowth, FixUnGrowth, CAGrowth):
    def __init__(self, graph, deg, params):
        SimpleGrowth.__init__(self, graph, deg, params)


class CAFixDegEvolve(SimpleGrowth, FixDegGrowth, CAGrowth):
    def __init__(self, graph, deg, params):
        SimpleGrowth.__init__(self, graph, deg, params)


class CAFixClustEvolve(SimpleGrowth, FixClustGrowth, CAGrowth):
    def __init__(self, graph, deg, params):
        SimpleGrowth.__init__(self, graph, deg, params)
