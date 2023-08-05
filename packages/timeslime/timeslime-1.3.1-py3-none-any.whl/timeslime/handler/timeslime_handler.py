from ast import literal_eval
from datetime import date, datetime, timedelta

from requests.exceptions import ConnectionError as RequestConnectionError

from timeslime.handler import (
    DatabaseHandler,
    NtpServerHandler,
    SettingsHandler,
    TimeslimeServerHandler,
)
from timeslime.models import Timespan


class TimeslimeHandler():
    def __init__(self, settings_handler: SettingsHandler, database_handler: DatabaseHandler, ntp_server_handler: NtpServerHandler, timeslime_server_handler: TimeslimeServerHandler = None):
        self.settings_handler = settings_handler
        self.database_handler = database_handler
        self.ntp_server_handler = ntp_server_handler
        self.timeslime_server_handler = timeslime_server_handler
        self.timespan = self.database_handler.get_recent_timespan()
        self.on_start = None
        self.on_stop = None

        if self.settings_handler:
            self.settings_handler.sync()
            self._set_daily_working_time(self.settings_handler, date.today().weekday())
            self._set_timeslime_server_handler(self.settings_handler)

    def _set_daily_working_time(self, settings_handler: SettingsHandler, weekday: int):
        if not settings_handler.contains('weekly_hours'):
            print('Please run `timeslime init` to configure timeslime')
            raise KeyError

        weekly_hours = literal_eval(settings_handler.get('weekly_hours').value)
        daily_working_time_array = weekly_hours[weekday].split(':')
        self._daily_working_time = timedelta(hours=int(daily_working_time_array[0]), minutes=int(daily_working_time_array[1]), seconds=int(daily_working_time_array[2]))

    def _set_timeslime_server_handler(self, settings_handler: SettingsHandler):
        if self.timeslime_server_handler is not None:
            return

        if settings_handler.contains('timeslime_server'):
            setting = settings_handler.get('timeslime_server')
            self.timeslime_server_handler = TimeslimeServerHandler(setting.value)
        else:
            self.timeslime_server_handler = None

    def start_time(self):
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        self.stop_time()
        self.timespan = Timespan()
        self.timespan.start_time = datetime.now()
        self.database_handler.save_timespan(self.timespan)
        if self.timeslime_server_handler is not None:
            try:
                self.timeslime_server_handler.send_timespan(self.timespan)
            except RequestConnectionError:
                pass
        if self.on_start is not None:
            self.on_start()

    def stop_time(self):
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        if self.timespan is not None and self.timespan.start_time is not None and self.timespan.stop_time is None:
            self.timespan.stop_time = datetime.now()
            self.database_handler.save_timespan(self.timespan)
            if self.timeslime_server_handler is not None:
                try:
                    self.timeslime_server_handler.send_timespan(self.timespan)
                except RequestConnectionError:
                    pass
        if self.on_stop is not None:
            self.on_stop()

    def get_elapsed_time(self) -> bool:
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        daily_sum_in_seconds = self.database_handler.get_tracked_time_in_seconds()
        current_timedelta = timedelta(seconds=0)
        if self.timespan is not None and self.timespan.stop_time is None:
            current_timedelta = datetime.now() - self.timespan.start_time
        return self._daily_working_time - daily_sum_in_seconds - current_timedelta

    def is_running(self):
        if self.database_handler.get_recent_timespan() is not None:
            return True
        else:
            return False
