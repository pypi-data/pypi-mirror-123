import edxml
from edxml.ontology import Brick, DataType


class EmailBrick(Brick):
    """
    Brick that defines some object types and concepts related to e-mail.
    """

    OBJECT_EMAIL_ADDRESS = 'computing.email.address'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_EMAIL_ADDRESS)\
            .set_description('an RFC 5322 e-mail address') \
            .set_data_type(DataType.string(length=254))\
            .set_regex_soft(r'[\S]+@[\S]+\.[a-z]+')\
            .set_display_name('e-mail address', 'e-mail addresses')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(EmailBrick)
