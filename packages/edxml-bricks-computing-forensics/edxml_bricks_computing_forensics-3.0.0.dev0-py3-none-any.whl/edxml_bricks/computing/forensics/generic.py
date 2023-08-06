import edxml
from edxml.ontology import Brick, DataType


class ForensicsBrick(Brick):
    """
    Brick that defines some object types and concepts from the field of computer forensics.
    """

    OBJECT_FILE_UPDATE_OPERATION = 'computing.forensics.filesystem.update-operation'
    OBJECT_FILE_TYPE = 'computing.forensics.filesystem.entry.type'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_FILE_UPDATE_OPERATION) \
            .set_description('a type of operation to update a filesystem entry')\
            .set_data_type(DataType.enum('changed (metadata)', 'modified (content)', 'accessed'))\
            .set_display_name('update operation')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_FILE_TYPE) \
            .set_description('a type of filesystem entry')\
            .set_display_name('filesystem entry type')\
            .set_data_type(DataType.enum('file', 'directory'))\
            .set_version(1)


edxml.ontology.Ontology.register_brick(ForensicsBrick)
