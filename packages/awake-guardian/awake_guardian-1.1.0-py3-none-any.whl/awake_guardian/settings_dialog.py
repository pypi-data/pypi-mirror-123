from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
)

from .autostart import create_autostart, is_autostart, remove_autostart
from .config import system
from .lang import L
from .power_management import SYSTEM_COMMANDS


class SettingsDialog(QDialog):
    def __init__(self, aw):
        def spacer():
            return QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.aw = aw
        QDialog.__init__(self)
        self.setWindowFlag(Qt.SubWindow, True)
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle(L.SETTINGS)

        layout = QVBoxLayout()

        remind_label = QLabel(L.TR)
        self.remind_m_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_MINUTES)
        self.remind_s_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_SECONDS)
        remind_hbox = QHBoxLayout()
        remind_hbox.addWidget(remind_label)
        remind_hbox.addSpacerItem(spacer())
        remind_hbox.addWidget(self.remind_m_spinbox)
        remind_hbox.addWidget(self.remind_s_spinbox)
        layout.addLayout(remind_hbox)

        nag_label = QLabel(L.TN)
        self.nag_m_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_MINUTES)
        self.nag_s_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_SECONDS)
        nag_hbox = QHBoxLayout()
        nag_hbox.addWidget(nag_label)
        nag_hbox.addSpacerItem(spacer())
        nag_hbox.addWidget(self.nag_m_spinbox)
        nag_hbox.addWidget(self.nag_s_spinbox)
        layout.addLayout(nag_hbox)

        self.inc_volume_nag_checkbox = QCheckBox(L.ING)
        layout.addWidget(self.inc_volume_nag_checkbox)

        self.powermngmt_group_box = QGroupBox(L.PWRMNGMT)
        self.powermngmt_group_box.setCheckable(True)
        powermngmt_layout = QVBoxLayout()
        event_hbox = QHBoxLayout()
        event_label = QLabel(L.TE)
        self.event_m_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_MINUTES)
        self.event_s_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_SECONDS)
        event_hbox.addWidget(event_label)
        event_hbox.addSpacerItem(spacer())
        event_hbox.addWidget(self.event_m_spinbox)
        event_hbox.addWidget(self.event_s_spinbox)
        powermngmt_layout.addLayout(event_hbox)
        action_hbox = QHBoxLayout()
        action_label = QLabel(L.PWRMNGMT_ACTION)
        self.pma = QComboBox()
        self.pma.addItems(SYSTEM_COMMANDS.keys())
        action_hbox.addWidget(action_label)
        action_hbox.addWidget(self.pma)
        powermngmt_layout.addLayout(action_hbox)
        self.powermngmt_group_box.setLayout(powermngmt_layout)
        layout.addWidget(self.powermngmt_group_box)

        s = system()
        if s == "Windows":
            str_autostart = L.WIN_AUTOSTART
            supported_system = True
        elif s == "Linux":
            str_autostart = L.LIN_AUTOSTART
            supported_system = True
        else:
            str_autostart = "Autostart"
            supported_system = False

        self.autostart_checkbox = QCheckBox(str_autostart)
        self.autostart_checkbox.setEnabled(supported_system)
        layout.addWidget(self.autostart_checkbox)

        self.time_range_group_box = QGroupBox(L.WOITM)
        self.time_range_group_box.setCheckable(True)
        time_range_from_label = QLabel(L.TIME_FROM)
        self.time_range_from = QTimeEdit()
        self.time_range_from.setDisplayFormat("hh:mm:ss")
        time_range_to_label = QLabel(L.TIME_TO)
        self.time_range_to = QTimeEdit()
        self.time_range_to.setDisplayFormat("hh:mm:ss")
        time_range_layout = QHBoxLayout()
        time_range_layout.addWidget(time_range_from_label)
        time_range_layout.addWidget(self.time_range_from)
        time_range_layout.addWidget(time_range_to_label)
        time_range_layout.addWidget(self.time_range_to)
        self.time_range_group_box.setLayout(time_range_layout)
        layout.addWidget(self.time_range_group_box)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.RestoreDefaults
        self.button_box = QDialogButtonBox(buttons)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

        self.set_values()
        self.make_connections()

    def set_values(self):
        self.remind_m_spinbox.setValue(self.aw.cfg.t_to_remind_m)
        self.remind_s_spinbox.setValue(self.aw.cfg.t_to_remind_s)
        self.nag_m_spinbox.setValue(self.aw.cfg.t_to_nag_m)
        self.nag_s_spinbox.setValue(self.aw.cfg.t_to_nag_s)
        self.inc_volume_nag_checkbox.setChecked(self.aw.cfg.inc_volume_nag)
        self.powermngmt_group_box.setChecked(self.aw.cfg.power_management)
        self.event_m_spinbox.setValue(self.aw.cfg.t_to_event_m)
        self.event_s_spinbox.setValue(self.aw.cfg.t_to_event_s)
        self.pma.setCurrentIndex(self.aw.cfg.power_management_action)
        self.autostart_checkbox.setChecked(True)
        self.time_range_group_box.setChecked(self.aw.cfg.t_range)
        self.time_range_from.setTime(self.aw.cfg.t_range_f)
        self.time_range_to.setTime(self.aw.cfg.t_range_t)

    def make_connections(self):
        self.remind_m_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_remind(val, None)
        )
        self.remind_s_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_remind(None, val)
        )
        self.nag_m_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_nag(val, None)
        )
        self.nag_s_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_nag(None, val)
        )
        self.inc_volume_nag_checkbox.stateChanged.connect(
            lambda val: self.aw.cfg.set_inc_volume_nag(val)
        )
        self.powermngmt_group_box.toggled.connect(
            lambda val: self.aw.cfg.set_power_management(val)
        )
        self.event_m_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_event(val, None)
        )
        self.event_s_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_event(None, val)
        )
        self.pma.activated.connect(
            lambda val: self.aw.cfg.set_power_management_action(val)
        )
        self.autostart_checkbox.stateChanged.connect(
            lambda val: self.toggle_autostart(val)
        )
        self.time_range_group_box.toggled.connect(
            lambda val: self.aw.cfg.set_time_range(val)
        )
        self.time_range_from.timeChanged.connect(
            lambda val: self.set_time_range_from(val)
        )
        self.time_range_to.timeChanged.connect(lambda val: self.set_time_range_to(val))
        self.button_box.accepted.connect(self.hide_dialog)
        self.button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(
            self.restore_defaults
        )

    def hide_dialog(self):
        self.aw.cfg.save_config()
        self.hide()

    def restore_defaults(self):
        self.aw.cfg.restore_defaults()
        self.set_values()

    def showEvent(self, event):
        self.autostart_checkbox.setChecked(is_autostart())

    def toggle_autostart(self, value):
        if value:
            create_autostart()
        else:
            remove_autostart()

    def set_time_range_from(self, val):
        self.aw.cfg.set_time_range_from(val)
        self.time_range_to.setMaximumTime(self.time_range_from.time().addSecs(-1))

    def set_time_range_to(self, val):
        self.aw.cfg.set_time_range_to(val)
        self.time_range_from.setMinimumTime(self.time_range_to.time().addSecs(1))
