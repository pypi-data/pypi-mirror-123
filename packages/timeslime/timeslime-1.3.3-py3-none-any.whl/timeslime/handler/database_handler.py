"""database handler class"""
from datetime import datetime, timedelta
from os import mkdir
from os.path import dirname, exists, join, realpath

from peewee import SqliteDatabase

from timeslime.models import Setting, Timespan


class DatabaseHandler():
    """database handler class"""
    def __init__(self, database_connection):
        self.is_testing = False
        if isinstance(database_connection, SqliteDatabase):
            self.connection = database_connection
            self.is_testing = True
        else:
            if not exists(database_connection):
                directory = dirname(database_connection)
                if directory != '' and not exists(directory):
                    mkdir(directory)
            self.connection = SqliteDatabase(database_connection)

        models = [Setting, Timespan]
        self.connection.bind(models)
        self.connection.create_tables(models)

    def __del__(self):
        if not self.is_testing:
            self.connection.close()

    def update(self):
        """run update on database schema"""
        with open(
            join(dirname(realpath(__file__)), "..", "update", "1.2_to_1.3.sql"),
            "r",
            encoding="utf-8",
        ) as update:
            for line in update.readlines():
                self.connection.execute_sql(line)

    def get_tracked_time_in_seconds(self) -> timedelta:
        """get tracked time in seconds"""
        daily_sum_in_seconds = timedelta(seconds=0)
        cursor = self.connection.execute_sql(
            "SELECT round(sum((julianday(stop_time) - julianday(start_time)) * 24 * 60 * 60))"
            ' as timespan FROM timespans WHERE date("now") = date(start_time);'
        )
        response = cursor.fetchone()[0]
        if response != None:
            daily_sum_in_seconds = timedelta(seconds=response)
        self.connection.commit()
        return daily_sum_in_seconds

    def save_timespan(self, timespan: Timespan):
        """save timespan
        :param timespan: defines timespan"""
        if not isinstance(timespan, Timespan):
            raise ValueError

        if timespan.start_time is None:
            raise ValueError

        timespan.updated_at = datetime.utcnow()
        timespan.delete_by_id(timespan.id)
        timespan.save(force_insert=True)

    def get_recent_timespan(self) -> Timespan:
        """get recent timespan"""
        # pylint: disable=singleton-comparison
        return Timespan.get_or_none(Timespan.stop_time == None)

    def save_setting(self, setting: Setting):
        """save setting to database
        :param setting: define setting"""
        if not isinstance(setting, Setting):
            raise ValueError

        if setting.key is None:
            raise ValueError

        setting.updated_at = datetime.utcnow()
        setting.delete_by_id(setting.id)
        setting.save(force_insert=True)

    def read_setting(self, key: str) -> Setting:
        """read setting from database
        :param key: defines key"""
        if not key:
            return

        return Setting.get(Setting.key == key)

    def read_settings(self) -> list:
        """read all settings from database"""
        # pylint: disable=singleton-comparison
        return Setting.select().where(Setting.key != None)

    def delete_setting(self, key: str):
        """delete setting from database"""
        if not key:
            return

        query = Setting.delete().where(Setting.key == key)
        query.execute()
