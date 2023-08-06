"""
Author: Martin Craig <martin.craig@eng.ox.ac.uk>
Copyright (c) 2016-2017 University of Oxford, Martin Craig
"""

from __future__ import division, unicode_literals, absolute_import, print_function

import sys
import os
import time
import traceback
import re
import tempfile

from PySide2 import QtGui, QtCore, QtWidgets

from quantiphyse.gui.options import OptionBox, DataOption, NumericOption, BoolOption, NumberListOption, TextOption, ChoiceOption
from quantiphyse.gui.widgets import QpWidget, HelpButton, BatchButton, Citation, TitleWidget, RunBox, WarningBox
from quantiphyse.gui.dialogs import TextViewerDialog, error_dialog, GridEditDialog
from quantiphyse.processes import Process
from quantiphyse.utils import get_plugins, QpException, sf

CEST_CITE_TITLE = "Quantitative Bayesian model-based analysis of amide proton transfer MRI"
CEST_CITE_AUTHOR = "Chappell, M. A., Donahue, M. J., Tee, Y. K., Khrapitchev, A. A., Sibson, N. R., Jezzard, P., & Payne, S. J."
CEST_CITE_JOURNAL = "Magnetic Resonance in Medicine. doi:10.1002/mrm.24474"

ALEXMT_CITE_TITLE = "Does the MT Effect Bias CEST Effects? Quantifying CEST in the Presence of MT"
ALEXMT_CITE_AUTHOR = "Alex K. Smith, Kevin J. Ray, Martin Craig, Seth A. Smith, Michael A Chappell"
ALEXMT_CITE_JOURNAL = "Magnetic Resonance in Medicine 2020 (pending, accepted)"

B0_DEFAULTS = ["3.0T", "9.4T", "Custom"]

# Gyromagnetic ratio / 2PI
GYROM_RATIO_BAR = 42.5774806e6

from ._version import __version__

class Pool:
    def __init__(self, name, enabled, vals, userdef=False):
        self.name = name
        self.enabled = enabled
        for b0 in B0_DEFAULTS:
            if b0 not in vals:
                vals[b0] = vals[list(vals.keys())[0]]
        self.original_vals = vals
        self.userdef = userdef
        self.reset()

    def reset(self):
        self.vals = {}
        for b0 in B0_DEFAULTS:
            self.vals[b0] = list(self.original_vals[b0])[:]

class NewPoolDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(NewPoolDialog, self).__init__(parent)
        self.setWindowTitle("New Pool")
        vbox = QtWidgets.QVBoxLayout()

        self.optbox = OptionBox()
        vbox.addWidget(self.optbox)

        self.optbox.add("Name", TextOption(), key="name")
        self.optbox.add("PPM", NumericOption(minval=0, maxval=20, default=0, decimals=3, slider=False), key="ppm")
        self.optbox.add("Exchange rate", NumericOption(minval=0, maxval=1000, default=0, decimals=1, slider=False), key="exch")
        self.optbox.add("T1 (s)", NumericOption(minval=0, maxval=10, default=1.0, decimals=2, slider=False), key="t1")
        self.optbox.add("T2 (s)", NumericOption(minval=0, maxval=1.0, default=0.07, decimals=6, slider=False), key="t2")
        self.optbox.option("name").sig_changed.connect(self._validate)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        vbox.addWidget(self.button_box)

        self.setLayout(vbox)
        self._validate()
    
    def pool(self, b0):
        return Pool(self.optbox.option("name").value, True, 
                    vals={b0 : [self.optbox.option(w).value for w in ["ppm", "exch", "t1", "t2"]]},
                    userdef=True)

    def _validate(self):
        valid = all([self.optbox.option(w).valid for w in ["ppm", "exch", "t1", "t2"]])
        
        if self.optbox.option("name").value != "":
            self.optbox.option("name").setStyleSheet("")
        else:
            self.optbox.option("name").setStyleSheet("QLineEdit {background-color: red}")
            valid = False
        
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(valid)

class SequenceOptions(QtWidgets.QWidget):
    """
    Widget containing options for the CEST sequence
    """

    sig_b0_changed = QtCore.Signal(float)

    def __init__(self, ivm=None):
        QtWidgets.QWidget.__init__(self)
        self._ivm = ivm

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.optbox = OptionBox()
        vbox.addWidget(self.optbox)

        self.optbox.add("CEST data", DataOption(self._ivm), key="data")
        self.optbox.add("ROI", DataOption(self._ivm, rois=True, data=False), key="mask")
        self.optbox.add("Frequency offsets", NumberListOption(), key="freqs")
        self.optbox.add("B0", ChoiceOption(B0_DEFAULTS), key="b0")
        self.optbox.add("Custom B0 (T)", NumericOption(minval=0.0, maxval=15, default=3.0, decimals=3), key="b0_custom")
        # FIXME multiple B1 values
        self.optbox.add("B1 (\u03bcT)", NumericOption(minval=0.0, maxval=2, default=0.55, decimals=6), key="b1")
        self.optbox.add("Saturation", ChoiceOption(["Continuous Saturation", "Pulsed Saturation"], ["continuous", "pulsed"]), key="sat")
        self.optbox.add("Saturation time (s)", NumericOption(minval=0.0, maxval=5, default=2, decimals=2), key="sat_time")
        self.optbox.add("Pulse Magnitudes", NumberListOption(), key="pulse_mag")
        self.optbox.add("Pulse Durations (s)", NumberListOption(), key="pulse_dur")
        self.optbox.add("Pulse Repeats", NumberListOption(), key="pulse_repeats")
        
        self.optbox.option("b0").sig_changed.connect(self._b0_changed)
        self.optbox.option("b0_custom").sig_changed.connect(self._b0_changed)
        self.optbox.option("sat").sig_changed.connect(self._sat_changed)
        
        self.warn_box = WarningBox()
        vbox.addWidget(self.warn_box)

        # B1 field
        #hbox = QtWidgets.QHBoxLayout()
        #self.unsat_cb = QtWidgets.QCheckBox("Unsaturated")
        #self.unsat_cb.stateChanged.connect(self.update_ui)
        #hbox.addWidget(self.unsat_cb)
        #self.unsat_combo = QtWidgets.QComboBox()
        #self.unsat_combo.addItem("first")
        #self.unsat_combo.addItem("last")
        #self.unsat_combo.addItem("first and last  ")
        #hbox.addWidget(self.unsat_combo)
        #hbox.addStretch(1)
        #grid.addLayout(hbox, 2, 2)

        vbox.addStretch(1)
        self._sat_changed()
        self._b0_changed()
    
    def _sat_changed(self):
        pulsed = self.optbox.option("sat").value == "pulsed"
        self.optbox.set_visible("pulse_mag", pulsed)
        self.optbox.set_visible("pulse_dur", pulsed)
        self.optbox.set_visible("pulse_repeats", pulsed)

    def _b0_changed(self):
        b0_sel = self.optbox.option("b0").value
        if b0_sel == "Custom":
            self.optbox.set_visible("b0_custom", True)
            b0 = self.optbox.option("b0_custom").value
        else:
            self.optbox.set_visible("b0_custom", False)
            b0 = float(b0_sel[:-1])
        self.sig_b0_changed.emit(b0)

    def _get_dataspec(self, options):
        dataspec = []
        freqs = options.pop("freqs")
        b1 = options.pop("b1")/1e6
        if options["sat"] == "pulsed":
            repeats = options.pop("pulse_repeats")
        else:
            repeats = 1
        for idx, freq in enumerate(freqs):
            #if self.unsat_cb.isChecked():
            #    self.debug("Unsat", idx, self.unsat_combo.currentIndex())
            #    if idx == 0 and self.unsat_combo.currentIndex() in (0, 2):
            #        b1 = 0
            #    elif idx == len(freqs)-1 and self.unsat_combo.currentIndex() in (1, 2):
            #        b1 = 0
            dataspec.append([freq, b1, repeats])
        #self.debug(dataspec)
        return dataspec

    def _get_ptrain(self, options):
        ptrain = []
        if options.pop("sat") == "pulsed":
            pms = options.pop("pulse_mag")
            pds = options.pop("pulse_dur")
            if len(pms) != len(pds):
                raise QpException("Pulse magnitude and duration must contain the same number of values")
            for pm, pd in zip(pms, pds):
                ptrain.append([pm, pd])
        else:
            ptrain.append([1, options.pop("sat_time")])
        #self.debug(ptrain)
        return ptrain

    def options(self):
        options = self.optbox.values()
        options["spec"] = self._get_dataspec(options)
        options["ptrain"] = self._get_ptrain(options)
        options.pop("b0")
        options.pop("b0_custom", None)
        return options

class PoolOptions(QtWidgets.QWidget):
    """
    Widget which allows the set of pools included in the analysis to be changed
    """
   
    sig_pools_changed = QtCore.Signal(object)

    def __init__(self, ivm=None):
        QtWidgets.QWidget.__init__(self)
        self._ivm = ivm
        self._poolvals_edited = False
        self._updating = False
        self._pools = [
            Pool("Water", True, {"3.0T" : [0, 0, 1.3, 0.07], "9.4T" : [0, 0, 1.9, 0.07]}),
            Pool("Amide", True, {"3.0T" : [3.5, 20, 0.77, 0.01], "9.4T" : [3.5, 20, 1.1, 0.01]}),
            Pool("Amine", False, {"3.0T" : [2.8, 500, 1.23, 0.00025], "9.4T" : [2.8, 500, 1.8, 0.00025]}),
            Pool("NOE/MT", True, {"3.0T" : [-2.41, 30, 1.0, 0.0002], "9.4T" : [-2.41, 30, 1.5, 0.0002]}),
            Pool("NOE", False, {"3.0T" : [-3.5, 20, 0.77, 0.0003], "9.4T" : [-3.5, 20, 1.1, 0.0003]}),
            Pool("MT", False, {"3.0T" : [0, 60, 1.0, 0.0001], "9.4T" : [0, 60, 1.5, 0.0001]}),
        ]

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.pools_table = QtGui.QStandardItemModel()
        self.pools_table.itemChanged.connect(self._pools_table_changed)
        self.pools_table_view = QtWidgets.QTableView()
        self.pools_table_view.setModel(self.pools_table)
        vbox.addWidget(self.pools_table_view)

        hbox = QtWidgets.QHBoxLayout()
        new_btn = QtWidgets.QPushButton("New")
        new_btn.clicked.connect(self._new_pool)
        hbox.addWidget(new_btn)
        reset_btn = QtWidgets.QPushButton("Reset")
        reset_btn.clicked.connect(self._reset_pools)
        hbox.addWidget(reset_btn)
        self.custom_label = QtWidgets.QLabel("")
        self.custom_label.setStyleSheet("QLabel { color : red; }")
        hbox.addWidget(self.custom_label, stretch=1)
        vbox.addLayout(hbox)

        self.set_b0(3.0)
        
    @property
    def pools(self):
        # We must put the MT pool last in case we are using Alex's new 
        # steady state solution (which assumes the last pool is MT)
        pools = [p for p in self._pools if p.name != "MT"]
        for p in self._pools:
            if p.name == "MT":
                pools.append(p)
        return pools

    def _update_pool_list(self):
        self._updating = True
        try:
            self.pools_table.clear()
            self.pools_table.setHorizontalHeaderItem(0, QtGui.QStandardItem("Name"))
            self.pools_table.setHorizontalHeaderItem(1, QtGui.QStandardItem("PPM offset"))
            self.pools_table.setHorizontalHeaderItem(2, QtGui.QStandardItem("Exchange rate"))
            self.pools_table.setHorizontalHeaderItem(3, QtGui.QStandardItem("T1"))
            self.pools_table.setHorizontalHeaderItem(4, QtGui.QStandardItem("T2"))
            self.pools_table_view.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

            for idx, pool in enumerate(self._pools):
                name_item = QtGui.QStandardItem(pool.name)
                name_item.setCheckable(True)
                name_item.setEditable(False)
                name_item.setCheckState(QtCore.Qt.Checked if pool.enabled else QtCore.Qt.Unchecked)
                name_item.setData(pool)
                self.pools_table.setItem(idx, 0, name_item)

                vals = pool.vals[self._b0_str]            
                for col, val in enumerate(vals):
                    item = QtGui.QStandardItem(sf(val))
                    item.setEditable(True)
                    item.setData(pool)
                    self.pools_table.setItem(idx, col+1, item)

            self.pools_table_view.resizeColumnsToContents()
        finally:
            self._updating = False
        self.sig_pools_changed.emit(self.pools)

    def _pools_table_changed(self, item):
        if not self._updating:
            pool = item.data()
            if item.column() == 0:
                pool.enabled = item.checkState()
            else:
                try:
                    val = float(item.text())
                    pool.vals[self._b0_str][item.column() - 1] = val
                    item.setBackground(QtCore.Qt.yellow)
                except ValueError:
                    item.setBackground(QtCore.Qt.red)
            self.sig_pools_changed.emit(self.pools)

    def _new_pool(self):
        dlg = NewPoolDialog(self)
        if dlg.exec_():
            self._pools.append(dlg.pool(self._b0_str))
            self._update_pool_list()

    def _reset_pools(self):
        self.custom_label.setText("")
        self._poolvals_edited = False
        for pool in self.pools:
            pool.reset()
        self._update_pool_list()

    def _get_poolmat(self):
        poolmat = []
        for pool in self.pools:
            vals = pool.vals[self._b0_str]
            if pool.name == "Water":
                # Embed the B0 value in the top left
                vals = [self._b0 * GYROM_RATIO_BAR,] + vals[1:]
            if pool.enabled:
                poolmat.append(vals)
        
        return poolmat

    def set_b0(self, b0):
        self._b0 = b0
        self._b0_str = "%.1fT" % b0
        if self._b0_str not in ("3.0T", "9.4T"):
            self._b0_str = "Custom"
            self.custom_label.setText("Custom B0 specified (%.1fT). Pool values may need editing" % b0)
        self._update_pool_list()

    def options(self):
        options = {
            "pools" : self._get_poolmat()
        }
        
        # Rename outputs using pool names rather than letters a, b, c etc
        renames = {"mean_M0a" : "mean_M0_Water", "mean_T1a" : "mean_T1_Water", "mean_T2a" : "mean_T2_Water"}
        for idx, pool in enumerate([p for p in self.pools[1:] if p.enabled]):
            pool_id = chr(ord('b') + idx)
            name = self._ivm.suggest_name(pool.name)
            renames["mean_M0%s_r" % pool_id] = "mean_M0_%s_r" % name
            renames["mean_k%sa" % pool_id] = "mean_exch_%s" % name
            renames["mean_ppm_%s" % pool_id] = "mean_ppm_%s" % name
            renames["mean_T1_%s" % pool_id] = "mean_T1_%s" % name
            renames["mean_T2_%s" % pool_id] = "mean_T2_%s" % name
            renames["cest_rstar_%s" % pool_id] = "cest_rstar_%s" % name
        options["output-rename"] = renames
        return options

class AnalysisOptions(QtWidgets.QWidget):
    """
    Widget allowing model and output options to be changed
    """
    
    def __init__(self, ivm=None):
        QtWidgets.QWidget.__init__(self)
        self._ivm = ivm
        self._poolvals_edited = False

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        self.optbox = OptionBox()
        vbox.addWidget(self.optbox)

        self.optbox.add("<b>Output options</b>")
        self.optbox.add("CEST R*", BoolOption(default=True), key="save-model-extras")
        self.optbox.add("Parameter maps", BoolOption(default=False), key="save-mean")
        #self.optbox.add("Parameter variance", BoolOption(default=False), key="var")
        self.optbox.add("Model fit", BoolOption(default=False), key="save-model-fit")
        self.optbox.add("Prefix for output", TextOption(), checked=True, key="output-prefix")

        self.optbox.add(" ")
        self.optbox.add("<b>Analysis options</b>")
        self.optbox.add("Spatial Regularization", BoolOption(), key="spatial")
        self.optbox.add("Allow uncertainty in T1/T2 values", BoolOption(), key="t12prior")
        self.optbox.add("Prior T1 map", DataOption(self._ivm), key="t1img", checked=True)
        self.optbox.add("Prior T2 map", DataOption(self._ivm), key="t2img", checked=True)
        self.optbox.add("Tissue PV map (GM+WM)", DataOption(self._ivm), key="pvimg", checked=True)
        self.optbox.option("t12prior").sig_changed.connect(self._update_ui)
        self.optbox.add("Use steady state solution for MT bias reduction", BoolOption(default=False), key="new-ss")
        self.optbox.option("new-ss").sig_changed.connect(self._update_ui)
        self.optbox.add("TR (s)", NumericOption(default=3.0, minval=0, maxval=5, digits=3, step=0.1), key="tr")
        self.optbox.add("Excitation flip angle (\N{DEGREE SIGN})", NumericOption(default=12.0, minval=0, maxval=25, digits=3, step=1.0), key="fa")
        self.optbox.add("MT pool Line shape", ChoiceOption(["None", "Gaussian", "Lorentzian", "Super Lorentzian"], 
                                                           ["none", "gaussian", "lorentzian", "superlorentzian"]),
                         key="lineshape")
        
        self.alexmt_cite = Citation(ALEXMT_CITE_TITLE, ALEXMT_CITE_AUTHOR, ALEXMT_CITE_JOURNAL)
        vbox.addWidget(self.alexmt_cite)

        vbox.addStretch(1)
        self._update_ui()

    def _update_ui(self):
        t12prior = self.optbox.option("t12prior").value
        self.optbox.set_visible("t1img", t12prior)
        self.optbox.set_visible("t2img", t12prior)
        newss = self.optbox.values().get("new-ss", False)
        self.optbox.set_visible("tr", newss)
        self.optbox.set_visible("fa", newss)
        self.optbox.set_visible("lineshape", newss)
        self.alexmt_cite.setVisible(newss)

    def set_pools(self, pools):
        self.optbox.set_visible("new-ss", "MT" in [p.name for p in pools if p.enabled])
        self._update_ui()

    def options(self):
        options = self.optbox.values()

        if options.pop("spatial", False):
            options["method"] = "spatialvb"
            options["param-spatial-priors"] = "MN+"
        else:
            options["method"] = "vb"
            options.pop("param-spatial-priors", None)

        # The new MT model is automatically triggered when the TR and FA options are given    
        options.pop("new-ss", None)

        prior_num = 1
        for idx in (1, 2):
            if "t%iimg" % idx in options:
                options["PSP_byname%i" % prior_num] = "T%ia" % idx
                options["PSP_byname%i_type" % prior_num] = "I"
                options["PSP_byname%i_image" % prior_num] = options.pop("t%iimg" % idx)
                prior_num += 1
        return options

class CESTWidget(QpWidget):
    """
    CEST-specific widget, using the Fabber process
    """

    def __init__(self, **kwargs):
        QpWidget.__init__(self, name="QuantiCEST", icon="cest", group="CEST", desc="Bayesian CEST analysis", **kwargs)
        
    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        try:
            self.fabber_process = get_plugins("processes", "FabberProcess")[0]
        except:
            self.fabber_process = None

        if self.fabber_process is None:
            vbox.addWidget(QtWidgets.QLabel("Fabber core library not found.\n\n You must install Fabber to use this widget"))
            return
    
        title = TitleWidget(self, help="cest", subtitle="Bayesian Modelling for Chemical Exchange Saturation Transfer MRI %s" % __version__)
        vbox.addWidget(title)
        
        cite = Citation(CEST_CITE_TITLE, CEST_CITE_AUTHOR, CEST_CITE_JOURNAL)
        vbox.addWidget(cite)

        self.tabs = QtWidgets.QTabWidget()
        self.seqtab = SequenceOptions(self.ivm)
        self.tabs.addTab(self.seqtab, "Sequence")

        self.pooltab = PoolOptions(self.ivm)
        self.tabs.addTab(self.pooltab, "Pools")

        self.analysistab = AnalysisOptions(self.ivm)
        self.tabs.addTab(self.analysistab, "Analysis")

        self.pooltab.sig_pools_changed.connect(self.analysistab.set_pools)
        self.seqtab.sig_b0_changed.connect(self.pooltab.set_b0)
        vbox.addWidget(self.tabs)

        run_tabs = QtWidgets.QTabWidget()
        run_box = RunBox(self._get_process_model, self._options, title="Run model-based analysis", save_option=True)
        run_tabs.addTab(run_box, "Model based analysis")
        run_box = RunBox(self._get_process_lda, self._options_lda, title="Run Lorentzian Difference analysis", save_option=True)
        run_tabs.addTab(run_box, "Lorentzian Difference analysis")
        vbox.addWidget(run_tabs)

        vbox.addStretch(1)
        self.analysistab.set_pools(self.pooltab.pools)
            
    def _options(self):
        # General defaults which never change
        options = {
            "model-group" : "cest",
            "model" : "cest",
            "noise" : "white",
            "max-iterations" : 20,
        }

        for idx in range(self.tabs.count()):
            options.update(self.tabs.widget(idx).options())

        # Apply output prefix
        output_prefix = options.pop("output-prefix", "")
        if output_prefix:
            output_renames = options["output-rename"]
            for output in ["modelfit", "mean_ppm_off", "mean_B1corr"]:
                output_renames[output] = output

            for key in list(output_renames.keys()):
                output_renames[key] = output_prefix + output_renames[key]

        return options

    def _options_lda(self):
        # Temporarily disable non-water pools just to generate the poolmat file
        enabled_pools = []
        for idx, p in enumerate(self.pooltab.pools):
            if p.enabled:
                enabled_pools.append(p.name)
            p.enabled = (idx == 0)

        options = self._options()
        
        # Return pools to previous state
        for idx, p in enumerate(self.pooltab.pools):
            p.enabled = (p.name in enabled_pools)

        # LDA uses the residual data (data - modelfit) only
        options.pop("save-mean", None)
        options.pop("save-zstat", None)
        options.pop("save-std", None)
        options.pop("save-model-fit", None)
        options.pop("save-model-extras", None)
        options["save-residuals"] = True

        # Restrict fitting to parts of the z-spectrum with |ppm| <= 1 or |ppm| >= 30
        # This is done by 'masking' the timepoints so Fabber still reads in the
        # full data and still outputs a prediction at each point, however the
        # masked points are not used in the parameter fitting
        masked_idx = 1
        freqs = self.seqtab.optbox.option("freqs").value
        for idx, f in enumerate(freqs):
            if f < 0: f = -f
            if f > 1 and f < 30:
                options["mt%i" % masked_idx] = idx+1
                masked_idx += 1

        for k in sorted(options.keys()):
            self.debug("%s: %s" % (k, options[k]))
        return options

    def _postproc_lda(self, status, log, exception):
        # Rename residuals and change sign convention
        residuals = self.ivm.data["residuals"]
        lorenz_diff = -residuals.raw()
        self.ivm.add(lorenz_diff, name="lorenz_diff", grid=residuals.grid, make_current=True)
        self.ivm.delete("residuals")

    def _get_process_model(self):
        return self.fabber_process(self.ivm)

    def _get_process_lda(self):
        # FIXME need special process to get the residuals only
        process = self.fabber_process(self.ivm)
        process.sig_finished.connect(self._postproc_lda)
        return process
        
    def batch_options(self):
        return "Fabber", self._options(), []
