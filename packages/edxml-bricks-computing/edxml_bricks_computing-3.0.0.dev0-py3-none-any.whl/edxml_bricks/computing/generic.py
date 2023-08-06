import edxml
from edxml.ontology import Brick, DataType


class ComputingBrick(Brick):
    """
    Brick that defines some object types and concepts related to some generic
    concepts from computer science.
    """

    OBJECT_UUID = 'computing.identifier.uuid'
    OBJECT_OID = 'computing.identifier.oid'
    OBJECT_USER_NAME = 'computing.user.name'
    OBJECT_SOFTWARE_PRODUCT_NAME = 'computing.software.product.name'
    OBJECT_HARDWARE_PRODUCT_NAME = 'computing.hardware.product.name'
    OBJECT_SOFTWARE_VERSION = 'computing.software.product.version'
    OBJECT_OS_NAME = 'computing.software.os.name'
    OBJECT_CPE_URI = 'computing.cpe.uri'
    OBJECT_DATA_SIZE_BYTES = 'computing.data.size.bytes'

    CONCEPT_COMPUTER = 'entity.physical-entity.object.whole.artifact.instrumentality.device.machine.computer'
    CONCEPT_USER_ACCOUNT = 'entity.physical-entity.object.whole.living-thing.organism.person.user'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_UUID) \
            .set_description('a universally unique identifier')\
            .set_data_type(DataType.uuid())\
            .set_display_name('UUID')\
            .set_xref('https://en.wikipedia.org/wiki/Universally_unique_identifier')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_OID) \
            .set_description('an object identifier (OID) as standardized by '
                             'the International Telecommunications Union')\
            .set_data_type(DataType.string(255, upper_case=False, require_unicode=False))\
            .set_display_name('OID')\
            .set_regex_hard(r'[0-2]\.[\d]+(.\d+)*')\
            .set_xref('https://en.wikipedia.org/wiki/Object_identifier')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_DATA_SIZE_BYTES) \
            .set_description('an amount of data measured in bytes')\
            .set_data_type(DataType.big_int(signed=False))\
            .set_unit('Byte', 'B')\
            .set_prefix_radix(2)\
            .set_display_name('size')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_USER_NAME) \
            .set_description('a name of a computer user account')\
            .set_data_type(DataType.string(length=255)) \
            .set_display_name('user name')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_SOFTWARE_PRODUCT_NAME) \
            .set_description('a name of a computer program') \
            .set_data_type(DataType.string(length=255, upper_case=False)) \
            .set_display_name('software product') \
            .fuzzy_match_phonetic()\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HARDWARE_PRODUCT_NAME) \
            .set_description('a name of a computer system or computer component') \
            .set_data_type(DataType.string(length=255)) \
            .set_display_name('hardware product') \
            .fuzzy_match_phonetic()\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_SOFTWARE_VERSION) \
            .set_description('a version of a computer program') \
            .set_data_type(DataType.string(length=255, upper_case=False)) \
            .set_display_name('software version') \
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_OS_NAME) \
            .set_description('a name of a computer operating system') \
            .set_data_type(DataType.string(length=255, upper_case=False)) \
            .set_display_name('operating system')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CPE_URI)\
            .set_description('a Common Platform Enumeration (CPE) URI') \
            .set_data_type(DataType.uri(path_separator=':')) \
            .set_display_name('CPE URI')\
            .set_xref('https://en.wikipedia.org/wiki/Common_Platform_Enumeration')\
            .compress()\
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):

        yield target_ontology.create_concept(cls.CONCEPT_COMPUTER) \
            .set_description('a kind of a computing device') \
            .set_display_name('computer')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_USER_ACCOUNT) \
            .set_description('a name of a user account on a computer system') \
            .set_display_name('user')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(ComputingBrick)
