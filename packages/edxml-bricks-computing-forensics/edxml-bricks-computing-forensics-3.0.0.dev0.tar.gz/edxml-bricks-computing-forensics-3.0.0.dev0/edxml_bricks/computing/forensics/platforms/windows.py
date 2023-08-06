import edxml
from edxml.ontology import Brick, DataType


class WindowsBrick(Brick):
    """
    Brick that defines some object types and concepts that are specific to Microsoft Windows.
    """

    OBJECT_VOLUME_SERIAL = 'computing.forensics.windows.volume.serial'
    OBJECT_DEVICE_PATH = 'computing.forensics.windows.device.path'
    OBJECT_DRIVE_LETTER = 'computing.forensics.windows.drive-letter'
    OBJECT_SID = 'computing.forensics.windows.sid'
    OBJECT_EVENTLOG_ID = 'computing.forensics.windows.eventlog.id'
    OBJECT_EVENTLOG_SEVERITY = 'computing.forensics.windows.eventlog.severity'
    OBJECT_EVENTLOG_SOURCE = 'computing.forensics.windows.eventlog.source'
    OBJECT_DOMAIN = 'computing.forensics.windows.domain'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_VOLUME_SERIAL) \
            .set_description('a Windows volume serial number')\
            .set_data_type(DataType.hex(length=4, separator='-', group_size=2))\
            .set_display_name('volume serial')\
            .set_xref('https://en.wikipedia.org/wiki/Volume_serial_number')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_DEVICE_PATH) \
            .set_description('a Windows device path')\
            .set_data_type(DataType.string())\
            .set_display_name('device path')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_DRIVE_LETTER)\
            .set_description('a Windows drive letter')\
            .set_data_type(DataType.string(length=1, lower_case=False, require_unicode=False))\
            .set_display_name('drive letter')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_SID)\
            .set_description('a Windows security identifier')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('SID')\
            .set_xref('https://en.wikipedia.org/wiki/Security_Identifier')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_EVENTLOG_ID) \
            .set_description('a message type identifier in a Windows event log')\
            .set_data_type(DataType.int(signed=False))\
            .set_display_name('Windows event ID')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_EVENTLOG_SEVERITY) \
            .set_description('a message type identifier in a Windows event log')\
            .set_data_type(DataType.tiny_int(signed=False))\
            .set_display_name('Windows event severity', 'Windows event severities')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_EVENTLOG_SOURCE) \
            .set_description('a source of Windows event log messages')\
            .set_data_type(DataType.string())\
            .set_display_name('Windows event source')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_DOMAIN) \
            .set_description('a name of a Windows network domain') \
            .set_data_type(DataType.string(lower_case=False, require_unicode=False)) \
            .set_display_name('windows domain') \
            .compress()\
            .set_version(1)


edxml.ontology.Ontology.register_brick(WindowsBrick)
