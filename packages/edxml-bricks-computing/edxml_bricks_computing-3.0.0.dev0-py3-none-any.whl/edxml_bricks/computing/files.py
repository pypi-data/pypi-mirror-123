import edxml
from edxml.ontology import Brick, DataType


class FilesBrick(Brick):
    """
    Brick that defines some object types and concepts related to computer files.
    """

    OBJECT_FILE_NAME = 'computing.file.name'
    OBJECT_FILE_NAME_CI = 'computing.file.name.ci'
    OBJECT_FILE_PATH = 'computing.file.path'
    OBJECT_FILE_PATH_CI = 'computing.file.path.ci'

    CONCEPT_FILE = 'entity.abstraction.communication.indication.evidence.record.file'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_FILE_NAME) \
            .set_description('a name of a computer file')\
            .set_data_type(DataType.string(reverse_storage=True))\
            .set_display_name('file name')\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_FILE_NAME_CI) \
            .set_description('a name of a computer file in a case insensitive file system') \
            .set_data_type(DataType.string(reverse_storage=True, lower_case=False))\
            .set_display_name('file name')\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_FILE_PATH) \
            .set_description('a location on a computer filesystem') \
            .set_data_type(DataType.string(reverse_storage=True))\
            .set_display_name('path')\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_FILE_PATH_CI) \
            .set_description('a location on a case insensitive computer filesystem') \
            .set_data_type(DataType.string(reverse_storage=True, lower_case=False))\
            .set_display_name('path')\
            .compress()\
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):
        yield target_ontology.create_concept(cls.CONCEPT_FILE) \
            .set_description('a computer resource for recording data') \
            .set_display_name('file')


edxml.ontology.Ontology.register_brick(FilesBrick)
