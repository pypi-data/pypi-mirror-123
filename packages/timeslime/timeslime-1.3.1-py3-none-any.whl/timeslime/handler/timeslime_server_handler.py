"""handler to a timeslime-server"""
from urllib.parse import urljoin

from requests import get, post

from timeslime.models import Setting, Timespan
from timeslime.serializer import SettingSerializer, TimespanSerializer


class TimeslimeServerHandler():
    """handler to a timeslime-server"""
    def __init__(self, server_url):
        self.server_url = server_url
        self.timespan_route = urljoin(self.server_url, "api/v1/timespans")
        self.setting_route = urljoin(self.server_url, "api/v1/settings")

    def send_timespan(self, timespan: Timespan) -> Timespan:
        """send a POST request to create a timespan"""
        if timespan is None or timespan.start_time is None:
            raise TypeError

        if not self.server_url:
            return timespan

        timespan_serializer = TimespanSerializer()
        data = timespan_serializer.serialize(timespan)
        response = post(self.timespan_route, json=data)
        response.raise_for_status()
        response_timespan = timespan_serializer.deserialize(response.text)

        return response_timespan

    def send_setting(self, setting: Setting) -> Setting:
        """send a POST request to create a setting"""
        if setting is None or setting.key is None:
            raise TypeError

        if not self.server_url:
            return setting

        setting_serializer = SettingSerializer()
        data = setting_serializer.serialize(setting)
        response = post(self.setting_route, json=data)
        response.raise_for_status()
        response_setting = setting_serializer.deserialize(response.json())

        return response_setting

    def send_setting_list(self, settings: list) -> list:
        """send a POST request to create a setting"""
        if settings is None:
            raise TypeError

        if not self.server_url:
            return settings

        setting_serializer = SettingSerializer()
        data = setting_serializer.serialize_list(settings)
        response = post(self.setting_route, json=data)
        response.raise_for_status()

        settings = []
        for setting in response.json():
            try:
                settings.append(setting_serializer.deserialize(setting))
            except KeyError:
                pass

        return settings

    def get_settings(self) -> list:
        """send a GET request to get all settings"""
        if not self.server_url:
            return []

        response = get(self.setting_route)
        response.raise_for_status()

        setting_serializer = SettingSerializer()
        settings = []
        for setting in response.json():
            try:
                settings.append(setting_serializer.deserialize(setting))
            except KeyError:
                pass

        return settings
