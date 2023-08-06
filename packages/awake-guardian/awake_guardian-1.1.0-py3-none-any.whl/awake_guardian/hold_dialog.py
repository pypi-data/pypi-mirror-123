from datetime import datetime, timedelta

from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
)

from .lang import L


class HoldDialog(QDialog):
    def __init__(self, aw):
        self.aw = aw
        QDialog.__init__(self)
        self.setWindowFlag(Qt.SubWindow, True)
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.setWindowTitle(L.PAUSE)

        hold_label = QLabel(L.PAUSE_LABEL)
        self.hold_m_spinbox = QSpinBox(
            value=aw.cfg.last_hold_time, maximum=1440, suffix=L.SUFFIX_MINUTES
        )
        self.hold_m_spinbox.valueChanged.connect(lambda val: aw.cfg.set_hold_time(val))

        spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout()
        hold_hbox = QHBoxLayout()
        hold_hbox.addWidget(hold_label)
        hold_hbox.addSpacerItem(spacer1)
        hold_hbox.addWidget(self.hold_m_spinbox)

        layout.addLayout(hold_hbox)

        self.button_box = QDialogButtonBox(standardButtons=buttons)
        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.cancel)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def ok(self):
        lht = self.aw.cfg.last_hold_time * 60
        t = datetime.now() + timedelta(0, lht)
        self.aw.hold(f'{L.RESUME} ({L.STR_AUTO}: {t.strftime("%H:%M:%S")})')
        self.aw.hold_timer.singleShot(lht * 1000, self.aw.resume)
        self.aw.cfg.save_config()
        self.close()

    def cancel(self):
        self.aw.resume()
        self.close()
