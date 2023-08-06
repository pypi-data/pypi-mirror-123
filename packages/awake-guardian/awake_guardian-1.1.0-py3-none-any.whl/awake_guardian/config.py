from appdirs import AppDirs
from configparser import ConfigParser
from os import mkdir
from os.path import dirname, isdir
from platform import system
from PySide2.QtCore import QTime
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

app = QApplication()
path = dirname(__file__)

CONFIG_FILE = "AwakeGuardian"
CONFIG_FILE_EXT = ".conf"

D = "DEFAULT"
LHT = "last_hold_time"
TTRM = "time_to_remind_m"
TTRS = "time_to_remind_s"
TTNM = "time_to_nag_m"
TTNS = "time_to_nag_s"
PM = "power_management"
PMA = "power_management_action"
TTEM = "time_to_event_m"
TTES = "time_to_event_s"
IVG = "increase_volume_nag"
TR = "time_range_active"  # FUTURE: this should be just "time_range" in v2.x, kept for backward compatibility
TRF = "time_range_from"
TRT = "time_range_to"


def defaults(key):
    d = {
        LHT: 15,
        TTRM: 10,
        TTRS: 0,
        TTNM: 15,
        TTNS: 0,
        PM: 0,
        PMA: 1,
        TTEM: 20,
        TTES: 0,
        IVG: 1,
        TR: 1,
        TRF: "20:00:00",
        TRT: "08:00:00",
    }
    return key, d[key]


class Icon:
    beep = QIcon(f"{path}/images/beep.png")
    clock = QIcon(f"{path}/images/clock.png")
    exit = QIcon(f"{path}/images/exit.png")
    eyes = QIcon(f"{path}/images/eyes.png")
    inactive = QIcon(f"{path}/images/inactive.png")
    settings = QIcon(f"{path}/images/settings.png")
    shout = QIcon(f"{path}/images/shout.png")


class Audio:
    coin = f"{path}/audio/coin.wav"
    wilhelm = f"{path}/audio/wilhelm.wav"


class Config:
    def __init__(self):
        self.load_config()

    def setup_config_file(self):
        dirs = AppDirs(CONFIG_FILE)
        config_dir = dirname(dirs.user_config_dir)
        if not isdir(config_dir):
            try:
                mkdir(config_dir)
            except Exception as e:
                raise e
        return f"{dirs.user_config_dir}{CONFIG_FILE_EXT}"

    def set_hold_time(self, minutes):
        self.last_hold_time = minutes
        self.save_config()

    def set_time_to_remind(self, minutes, seconds):
        if minutes is not None:
            self.t_to_remind_m = minutes
        if seconds is not None:
            self.t_to_remind_s = seconds
        self.save_config()

    def set_time_to_nag(self, minutes, seconds):
        if minutes is not None:
            self.t_to_nag_m = minutes
        if seconds is not None:
            self.t_to_nag_s = seconds
        self.save_config()

    def set_time_to_event(self, minutes, seconds):
        if minutes is not None:
            self.t_to_event_m = minutes
        if seconds is not None:
            self.t_to_event_s = seconds
        self.save_config()

    def set_power_management(self, value):
        self.power_management = int(value)
        self.save_config()

    def set_power_management_action(self, value):
        self.power_management_action = int(value)
        self.save_config()

    def set_inc_volume_nag(self, value):
        self.inc_volume_nag = value
        self.save_config()

    def set_time_range(self, value):
        self.t_range = int(value)
        self.save_config()

    def set_time_range_from(self, time):
        self.t_range_f = time
        self.save_config()

    def set_time_range_to(self, time):
        self.t_range_t = time
        self.save_config()

    def save_config(self):
        settings = {
            TTRM: self.t_to_remind_m,
            TTRS: self.t_to_remind_s,
            TTNM: self.t_to_nag_m,
            TTNS: self.t_to_nag_s,
            IVG: self.inc_volume_nag,
            PM: self.power_management,
            PMA: self.power_management_action,
            TTEM: self.t_to_event_m,
            TTES: self.t_to_event_s,
            LHT: self.last_hold_time,
            TR: self.t_range,
            TRF: self.t_range_f.toString(),
            TRT: self.t_range_t.toString(),
        }
        self.config_parser[D] = settings
        with open(self.config_file, "w") as cf:
            self.config_parser.write(cf)

    def clear_config(self):
        open(self.config_file, "w")

    def load_config(self):
        self.config_file = self.setup_config_file()
        self.config_parser = ConfigParser()
        self.config_parser.read(self.config_file)

        self.last_hold_time = int(self.config_parser[D].get(*defaults(LHT)))
        self.t_to_remind_m = int(self.config_parser[D].get(*defaults(TTRM)))
        self.t_to_remind_s = int(self.config_parser[D].get(*defaults(TTRS)))
        self.t_to_nag_m = int(self.config_parser[D].get(*defaults(TTNM)))
        self.t_to_nag_s = int(self.config_parser[D].get(*defaults(TTNS)))

        self.inc_volume_nag = int(self.config_parser[D].get(*defaults(IVG)))
        self.volume = None

        self.power_management = int(self.config_parser[D].get(*defaults(PM)))
        self.power_management_action = int(self.config_parser[D].get(*defaults(PMA)))
        self.t_to_event_m = int(self.config_parser[D].get(*defaults(TTEM)))
        self.t_to_event_s = int(self.config_parser[D].get(*defaults(TTES)))

        self.t_range = int(self.config_parser[D].get(*defaults(TR)))
        self.t_range_f = QTime.fromString(self.config_parser[D].get(*defaults(TRF)))
        self.t_range_t = QTime.fromString(self.config_parser[D].get(*defaults(TRT)))

    def restore_defaults(self):
        self.clear_config()
        self.load_config()
        self.save_config()
