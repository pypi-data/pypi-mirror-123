#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

"""

This module is used by the data harvesters to handle the decoded data TTrees for each DIF. Basically it just
opens a TTree and enables some of its TBranches. Optionally it can store a list of events for later retrieval.
It is not really meant to read the TTree itself, just open it and do some collateral checks.

The classes are organized in a tree-like structure where basically a "Detectors" object is just a list of "Detector"
objects, which in turn are a list of "Dif" objects. The detectors and DIFs are iterable like standard Python lists,
even if strictly speaking they are not subclasses of 'list'.

"""

from collections import namedtuple
from typing import Optional, List

try:
    import ROOT

    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    ROOT = None

from wagascianpy.plotting.topology import Topology, DetectorType, DifIndex

WallmrdDifList = namedtuple('WallmrdDifList', ['top', 'bottom'])
WagasciDifList = namedtuple('WagasciDifList', ['top', 'side'])


class Dif(object):

    def __init__(self, name, dif_id, enabled):
        self.name = name
        self._dif_id = dif_id
        self._enabled = enabled
        self._tree_name = None
        self._chain = None
        self._friends = {}
        self._spills = None

    @property
    def dif_id(self):
        return self._dif_id

    def is_enabled(self):
        return self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def add_tree(self, root_file, tree_name, tree_friends=None):
        # type: (str, str, Optional[List[str]]) -> None
        if self._tree_name is None:
            self._tree_name = tree_name
        if tree_name != self._tree_name:
            raise ValueError("TTree name must be consistent among all ROOT files")
        if self._chain is None:
            self._chain = ROOT.TChain(tree_name)
        self._chain.Add(root_file)
        if tree_friends:
            tfile = ROOT.TFile(root_file, "READ")
            for friend in tree_friends:
                print("Searching for tree friend {}".format(friend))
                if tfile.GetListOfKeys().Contains(friend):
                    print("Tree friend {} found".format(friend))
                    if friend not in self._friends:
                        self._friends[friend] = ROOT.TChain(friend)
                        self._chain.AddFriend(self._friends[friend])
                    self._friends[friend].Add(root_file)
                else:
                    print("Tree friend {} not found".format(friend))
            tfile.Close()

    def set_active_branches(self, active_branches):
        assert self._chain is not None, "Add a tree before accessing it"
        self._chain.SetBranchStatus("*", 0)
        for variable in active_branches:
            self._chain.SetBranchStatus(variable, 1)

    def get_tree(self):
        # type: (...) -> ROOT.TChain
        assert self._chain is not None, "Add a tree before accessing it"
        return self._chain

    def get_friend(self, name):
        # type: (str) -> ROOT.TChain
        return self._friends[name]

    def has_friend(self, name):
        # type: (str) -> bool
        return name in self._friends

    def set_spills(self, spills):
        assert isinstance(spills, list), "The spill list must be a list"
        self._spills = spills

    def get_spills(self):
        assert self._spills is not None, "Please set the spill list before accessing it"
        return self._spills

    def has_spills(self):
        return bool(self._spills)

    def has_tree(self):
        if self._chain is None:
            return False
        else:
            return True


class Detector(object):

    def __init__(self, name, difs, enabled=True):
        self.name = name
        self._enabled = enabled
        if isinstance(difs, WallmrdDifList):
            self.detector_type = DetectorType.Wallmrd
            self.top = difs.top
            self.bottom = difs.bottom
            self.num_difs = 2
        elif isinstance(difs, WagasciDifList):
            self.detector_type = DetectorType.Wagasci
            self.top = difs.top
            self.side = difs.side
            self.num_difs = 2
        else:
            raise NotImplementedError("DIF list type {} not recognized".format(type(difs).__name__))

    def is_enabled(self):
        if not self._enabled:
            return False
        else:
            for dif in self:
                if not dif.has_tree() or not dif.has_spills():
                    return False
        return True

    def get_snake_case_name(self):
        return self.name.lower().replace(' ', '_')

    def __iter__(self):
        """ Returns the Iterator object """
        return DifsIterator(self)


class Detectors(object):

    def __init__(self, enabled_detectors=None):
        # type: (Optional[Topology]) -> None
        self._enabled_detectors = Topology(iterate_by_dif=True)
        if enabled_detectors is not None:
            self._enabled_detectors.import_topology(enabled_detectors)

        self.wallmrd_north = Detector(
            name="WallMRD north",
            difs=WallmrdDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WallMrdNorthTop),
                                    enabled=self._enabled_detectors.wallmrd_north_top.is_enabled()),
                                Dif(name="bottom",
                                    dif_id=int(DifIndex.WallMrdNorthBottom),
                                    enabled=self._enabled_detectors.wallmrd_north_bottom.is_enabled())),
            enabled=(self._enabled_detectors.wallmrd_north_top.is_enabled() or
                     self._enabled_detectors.wallmrd_north_bottom.is_enabled()))
        self.wallmrd_south = Detector(
            name="WallMRD south",
            difs=WallmrdDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WallMrdSouthTop),
                                    enabled=self._enabled_detectors.wallmrd_south_top.is_enabled()),
                                Dif(name="bottom",
                                    dif_id=int(DifIndex.WallMrdSouthBottom),
                                    enabled=self._enabled_detectors.wallmrd_south_bottom.is_enabled())),
            enabled=(self._enabled_detectors.wallmrd_south_top.is_enabled() or
                     self._enabled_detectors.wallmrd_south_bottom.is_enabled()))
        self.wagasci_upstream = Detector(
            name="WAGASCI upstream",
            difs=WagasciDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WagasciUpstreamTop),
                                    enabled=self._enabled_detectors.wagasci_upstream_top.is_enabled()),
                                Dif(name="side",
                                    dif_id=int(DifIndex.WagasciUpstreamBottom),
                                    enabled=self._enabled_detectors.wagasci_upstream_side.is_enabled())),
            enabled=(self._enabled_detectors.wagasci_upstream_top.is_enabled() or
                     self._enabled_detectors.wagasci_upstream_side.is_enabled()))
        self.wagasci_downstream = Detector(
            name="WAGASCI downstream",
            difs=WagasciDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WagasciDownstreamTop),
                                    enabled=self._enabled_detectors.wagasci_downstream_top.is_enabled()),
                                Dif(name="side",
                                    dif_id=int(DifIndex.WagasciDownstreamBottom),
                                    enabled=self._enabled_detectors.wagasci_downstream_side.is_enabled())),
            enabled=(self._enabled_detectors.wagasci_downstream_top.is_enabled() or
                     self._enabled_detectors.wagasci_downstream_side.is_enabled()))

    def __iter__(self):
        """ Returns the Iterator object """
        return DetectorsIterator(self)

    def get_dif(self, dif_id):
        # type: (int) -> Dif
        dif_id = int(dif_id)
        if dif_id == int(DifIndex.WallMrdNorthTop):
            return self.wallmrd_north.top
        elif dif_id == int(DifIndex.WallMrdNorthBottom):
            return self.wallmrd_north.bottom
        elif dif_id == int(DifIndex.WallMrdSouthTop):
            return self.wallmrd_south.top
        elif dif_id == int(DifIndex.WallMrdSouthBottom):
            return self.wallmrd_south.bottom
        elif dif_id == int(DifIndex.WagasciUpstreamTop):
            return self.wagasci_upstream.top
        elif dif_id == int(DifIndex.WagasciUpstreamBottom):
            return self.wagasci_upstream.side
        elif dif_id == int(DifIndex.WagasciDownstreamTop):
            return self.wagasci_downstream.top
        elif dif_id == int(DifIndex.WagasciDownstreamBottom):
            return self.wagasci_downstream.side
        else:
            raise ValueError("DIF ID not recognized : {}".format(dif_id))

    def disable_all_difs(self):
        # type: (...) -> None
        for detector in self:
            for dif in detector:
                dif.disable()

    def enable_dif(self, dif_id):
        # type: (int) -> None
        dif_id = int(dif_id)
        self.get_dif(dif_id).enable()

    def get_detector(self, detector_name):
        detector_name = detector_name.lower().replace(' ', '').replace(' ', '')
        if detector_name == "wallmrdnorth":
            return self.wallmrd_north
        elif detector_name == "wallmrdsouth":
            return self.wallmrd_south
        elif detector_name == "wagasciupstream":
            return self.wagasci_upstream
        elif detector_name == "wagascidownstream":
            return self.wagasci_downstream
        elif detector_name == "wallmrdnorthtop":
            return self.wallmrd_north.top
        elif detector_name == "wallmrdnorthbottom":
            return self.wallmrd_north.bottom
        elif detector_name == "wallmrdsouthtop":
            return self.wallmrd_south.top
        elif detector_name == "wallmrdsouthbottom":
            return self.wallmrd_south.bottom
        elif detector_name == "wagasciupstreamtop":
            return self.wagasci_upstream.top
        elif detector_name == "wagasciupstreamside":
            return self.wagasci_upstream.side
        elif detector_name == "wagascidownstreamtop":
            return self.wagasci_downstream.top
        elif detector_name == "wagascidownstreamside":
            return self.wagasci_downstream.side
        return None


class DifsIterator(object):
    def __init__(self, detector):
        # Difs object reference
        self._detector = detector
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """ Returns the next value from difs object's lists """
        result = None
        if self._detector.detector_type == DetectorType.Wallmrd:
            if self._index < 2:
                if self._index == 0:
                    result = self._detector.top
                elif self._index == 1:
                    result = self._detector.bottom
                self._index += 1
                return result
        elif self._detector.detector_type == DetectorType.Wagasci:
            if self._index < 2:
                if self._index == 0:
                    result = self._detector.top
                elif self._index == 1:
                    result = self._detector.side
                self._index += 1
                return result
        else:
            raise NotImplementedError("Detector type {} not recognized".format(self._detector.detector_type))
        # End of Iteration
        raise StopIteration

    def next(self):
        return self.__next__()


class DetectorsIterator(object):
    def __init__(self, detectors):
        # Detectors object reference
        self._detectors = detectors
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """ Returns the next value from detectors object's lists """
        result = None
        if self._index < 4:
            if self._index == 0:
                result = self._detectors.wallmrd_north
            elif self._index == 1:
                result = self._detectors.wallmrd_south
            elif self._index == 2:
                result = self._detectors.wagasci_upstream
            elif self._index == 3:
                result = self._detectors.wagasci_downstream
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration

    def next(self):
        return self.__next__()
