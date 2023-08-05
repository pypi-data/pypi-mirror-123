"""collection of data models"""
from datetime import datetime
from uuid import uuid4

from peewee import DateTimeField, Model, TextField, UUIDField


class Setting(Model):
    """setting model"""

    id = UUIDField(primary_key=True, default=uuid4)
    key = TextField(index=True, null=True)
    value = TextField(null=True)
    created_at = DateTimeField(default=datetime.utcnow, null=False)
    updated_at = DateTimeField(default=datetime.utcnow, null=False)

    class Meta:
        """defines meta information"""

        table_name = "settings"


class Timespan(Model):
    """timespan model"""

    id = UUIDField(primary_key=True, default=uuid4)
    start_time = DateTimeField(null=True)
    stop_time = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.utcnow, null=False)
    updated_at = DateTimeField(default=datetime.utcnow, null=False)

    class Meta:
        """defines meta information"""

        table_name = "timespans"
