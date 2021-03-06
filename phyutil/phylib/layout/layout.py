# encoding: UTF-8

"""
Accelerator Layout
==================

The Accelerator Layout is a data model developed to capture
the accelerator element positions independent of file format and/or simulation
tool. It is used as intermediate data structure when converting between formats
or generating lattice files for use with various simulation tools.

The file format used by the accelerator layout data is a simple CSV format with
mandatory columns 'name', 'tyle', 'L', 's', 'apx', 'apy' and then followed by
the names of optional columns:

name,type,L,s,apx,apy [, OPTIONAL COLUMN NAMES ]
ElementName,ElementType,Length,Position,ApertureX,ApertureY[, OPTIONAL COLUMN VALUES ]
[...]

For example:

name,type,L,s,apx,apy,subsystem,dtype,system,inst,device,desc
LS1_CA01:GV_D1124,VALVE,0.072,112.40799996,0.04,0.04,CA01,NONE,LS1,NONE,GV,gate valve
DRIFT,DRIFT,0.1350635,112.49540846,0.04,0.04,NONE,NONE,NONE,NONE,NONE,bellows
LS1_CA01:CAV1_D1127,CAV,0.24,112.69906346,0.034,0.034,CA01,CAV_B04,LS1,D1127,CAV1,b04 cavity
LS1_CA01:BLM_D1128,BLM,0.0,112.78681696,0.034,0.034,CA01,NONE,LS1,NONE,BLM,outside loss monitor
DRIFT,DRIFT,0.06426334,112.86731838,0.04,0.04,NONE,NONE,NONE,NONE,NONE,bellow
LS1_CA01:BPM_D1129,BPM,0.0,112.8833268,0.04,0.04,CA01,BPM6,LS1,D1129,BPM,"position monitor, BPMc"
[...]


:author: Dylan Maxwell
:date: 2015-06-09

:copyright: Copyright (c) 2015, Facility for Rare Isotope Beams

"""

import os.path, logging, csv

from accel import SeqElement
from accel import DriftElement, ValveElement, PortElement, CavityElement
from accel import HCorElement, VCorElement, CorElement, SolCorElement
from accel import BLMElement, BPMElement, BLElement, PMElement,  BCMElement
from accel import StripElement, BendElement, QuadElement, SextElement


_LOGGER = logging.getLogger(__name__)



def build_layout(layoutPath=None, **kwargs):
    """Build the accelerator layout from a layout data file.
 
       :param layoutPath: path to layout data file
    """

    if layoutPath is None:
        raise RuntimeError("build_layout: layout data file not specified")

    if not os.path.isfile(layoutPath):
        raise RuntimeError("build_layout: layout data file not found: {}".format(layoutPath))

    with open(layoutPath, "r") as layoutFile:

        csvstream = csv.reader(layoutFile, delimiter=',', skipinitialspace=True)

        fixedkeys = [ "name", "type", "L", "s", "apx", "apy" ]

        elements = []

        header = csvstream.next()

        def buildEtype(row):
            return row[header.index("type")]

        def buildElement(row, ElemType):
            name = row[header.index("name")]
            length = float(row[header.index("L")])
            z = float(row[header.index("s")])
            apx = float(row[header.index("apx")])
            apy = float(row[header.index("apx")])
            meta = {}
            for idx in range(len(header)):
                if header[idx] not in fixedkeys:
                    if row[idx] != "NONE":
                        meta[header[idx]] = row[idx]
            return ElemType(z, length, (apx,apy), name, **meta)

        while True:
            try:
                row = csvstream.next()
            except StopIteration:
                break;

            etype = buildEtype(row)

            if etype == DriftElement.ETYPE:
                elements.append(buildElement(row, DriftElement))

            elif etype == PortElement.ETYPE:
                elements.append(buildElement(row, PortElement))

            elif etype == ValveElement.ETYPE:
                elements.append(buildElement(row, ValveElement))

            elif etype == CavityElement.ETYPE:
                elements.append(buildElement(row, CavityElement))

            elif etype == PMElement.ETYPE:
                elements.append(buildElement(row, PMElement))

            elif etype == BLElement.ETYPE:
                elements.append(buildElement(row, BLElement))

            elif etype == BLMElement.ETYPE:
                elements.append(buildElement(row, BLMElement))

            elif etype == BPMElement.ETYPE:
                elements.append(buildElement(row, BPMElement))

            elif etype == BCMElement.ETYPE:
                elements.append(buildElement(row, BCMElement))

            elif etype == SolCorElement.ETYPE or etype == CorElement.ETYPE:
                if etype == SolCorElement.ETYPE:
                    elem = buildElement(row, SolCorElement)
                else:
                    elem = buildElement(row, CorElement)

                for _ in xrange(2):
                    row = csvstream.next()
                    etype = buildEtype(row)
                    if etype == HCorElement.ETYPE:
                        if elem.h is None:
                            elem.h = buildElement(row, HCorElement)
                        else:
                            raise RuntimeError("build_layout: HCorElement already found")
                    elif etype == VCorElement.ETYPE:
                        if elem.v is None:
                            elem.v = buildElement(row, VCorElement)
                        else:
                            raise RuntimeError("build_layout: VCorElement already found")

                elements.append(elem)

            elif etype == BendElement.ETYPE:
                elements.append(buildElement(row, BendElement))

            elif etype == QuadElement.ETYPE:
                elements.append(buildElement(row, QuadElement))

            elif etype == SextElement.ETYPE:
                elements.append(buildElement(row, SextElement))

            elif etype == StripElement.ETYPE:
                elements.append(buildElement(row, StripElement))

            else:
                raise RuntimeError("read_layout: Element type '{}' not supported".format(etype))

    return Layout(os.path.basename(layoutPath), elements)



class Layout(SeqElement):
    """Layout represents a sequence of elements

       :param name: name of this element
       :param elements: list of elements
    """
    def __init__(self, name, elements=None, **meta):
        super(Layout, self).__init__(name, elements=elements, **meta)


    def write(self, stream, start=None, end=None):
        """Write the layout elements to the specified output stream.

           :param stream: file-like output stream
           :param start: name of start element
           :param end: name of end element
        """

        def buildElemDict(element):
            metakeys.update(element.meta.keys())
            elemdict = dict(element.meta)
            elemdict["name"] = element.name
            elemdict["type"] = element.ETYPE
            elemdict["L"] = element.length
            elemdict["s"] = element.z
            elemdict["apx"] = element.apertureX
            elemdict["apy"] = element.apertureY
            _LOGGER.debug("Layout: write element: %s", elemdict)
            return elemdict

        metakeys = set()
        elemdicts = []

        for element in self.iter(start,end):
            elemdicts.append(buildElemDict(element))
            if isinstance(element, (CorElement, SolCorElement)):
                elemdicts.append(buildElemDict(element.h))
                elemdicts.append(buildElemDict(element.v))

        fixedkeys = [ "name", "type", "L", "s", "apx", "apy" ]

        metakeys = list(metakeys)

        csvstream = csv.writer(stream, delimiter=',')

        csvstream.writerow(fixedkeys+metakeys)

        for element in elemdicts:
            row = []
            for key in fixedkeys:
                row.append(str(element[key]))
            for key in metakeys:
                if key in element:
                    row.append(str(element[key]))
                else:
                    row.append("NONE")
            csvstream.writerow(row)

