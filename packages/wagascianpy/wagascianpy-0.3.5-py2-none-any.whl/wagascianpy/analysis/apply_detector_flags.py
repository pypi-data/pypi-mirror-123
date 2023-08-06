#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import re

import numpy as np

# ROOT
try:
    # noinspection PyPackageRequirements
    import ROOT

    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    ROOT = None

from wagascianpy.analysis.spill import IS_GOOD_SPILL, WAGASCI_SPILL_BEAM_MODE
import wagascianpy.database.wagascidb
import wagascianpy.plotting.detector
from wagascianpy.utils.utils import extract_dif_id, extract_raw_tree_name

DETECTOR_FLAGS_ERROR_CODE = 1001
_DETECTOR_FLAGS_TREE_NAME = "detector_flags"
_DETECTOR_FLAGS_BRANCH_NAME = "good_detector_flag"
_DETECTORS = ["wagasci_upstream", "wagasci_downstream", "wallmrd_north", "wallmrd_south"]


def _parse_run_number(file_name, run_number=None):
    # type: (str, Optional[int]) -> int
    if run_number is not None and run_number > 0:
        this_run_number = run_number
    else:
        match = re.search(r'([\d]+)_ecal_dif_[\d]+_tree.root$', file_name)
        if match is not None:
            this_run_number = int(match.group(1))
        else:
            raise ValueError("Cannot detect run number in file name '{}'".format(file_name))
    return this_run_number


def _parse_input_files(input_path, run_number):
    # type: (str, int) -> Tuple[int, Detectors]

    detectors = wagascianpy.plotting.detector.Detectors()
    detectors.disable_all_difs()

    if os.path.isfile(input_path):
        run_number = _parse_run_number(file_name=input_path, run_number=run_number)
        dif_id = extract_dif_id(path=input_path)
        detectors.enable_dif(dif_id)
        detectors.get_dif(dif_id).add_tree(root_file=input_path, tree_name="raw", tree_friends=["fixed_spill_number"])
    elif os.path.isdir(input_path):
        for file_name in os.listdir(input_path):
            if re.search(r'_ecal_dif_[\d]+_tree.root', file_name) is not None:
                run_number = _parse_run_number(file_name=file_name, run_number=run_number)
                dif_id = extract_dif_id(path=file_name)
                detectors.enable_dif(dif_id)
                detectors.get_dif(dif_id).add_tree(root_file=os.path.join(input_path, file_name), tree_name="raw",
                                                   tree_friends=["fixed_spill_number"])
    return run_number, detectors


def _reset_flags(tfile):
    # type: (ROOT.TFile) -> None
    if tfile.GetListOfKeys().Contains(_DETECTOR_FLAGS_TREE_NAME):
        for key in tfile.GetListOfKeys():
            if key.GetName() == _DETECTOR_FLAGS_TREE_NAME:
                tfile.Delete("{};{}".format(_DETECTOR_FLAGS_TREE_NAME, key.GetCycle()))


def apply_detector_flags(input_path, run_number, wagasci_database):
    if ROOT is None:
        raise ImportError("No ROOT module was found!")

    if not os.path.exists(input_path):
        raise IOError("Input file %s not found" % input_path)

    run_number, detectors = _parse_input_files(input_path=input_path, run_number=run_number)

    with wagascianpy.database.wagascidb.WagasciDataBase(db_location=wagasci_database) as db:

        run_records = db.get_run_interval(run_number_start=run_number, only_good=False)
        if len(run_records) != 1:
            raise RuntimeError("Run {} not found in database".format(run_number))
        run_record = run_records[0]
        good_run_flag = run_record.good_run_flag

        for detector in detectors:
            enabled_difs = (dif for dif in detector if dif.is_enabled())
            for dif in enabled_difs:

                detector_name = detector.get_snake_case_name()
                detector_flag = getattr(run_record, detector_name + "_good_data_flag")

                dif.get_tree().LoadTree(0)
                dif.set_active_branches(["spill_mode", "good_spill_flag"])
                tfile = ROOT.TFile(dif.get_tree().GetCurrentFile().GetPath().split(':')[0], "UPDATE")
                _reset_flags(tfile)

                friend_tree = ROOT.TTree(_DETECTOR_FLAGS_TREE_NAME, "Detector good-bad flags")
                friend_tree.SetDirectory(tfile)
                raw_tree = getattr(tfile, extract_raw_tree_name(tfile))
                raw_tree.AddFriend(friend_tree)
                array = np.array([False], dtype=np.bool)
                friend_tree.Branch(_DETECTOR_FLAGS_BRANCH_NAME, array, "{}/O".format(_DETECTOR_FLAGS_BRANCH_NAME))

                for event in dif.get_tree():
                    if not good_run_flag or \
                            event.good_spill_flag != IS_GOOD_SPILL or \
                            event.spill_mode != WAGASCI_SPILL_BEAM_MODE:
                        array[0] = False
                    else:
                        array[0] = bool(detector_flag)
                    friend_tree.Fill()

                friend_tree.Write("", ROOT.TObject.kWriteDelete)
                tfile.Write("", ROOT.TObject.kWriteDelete)
