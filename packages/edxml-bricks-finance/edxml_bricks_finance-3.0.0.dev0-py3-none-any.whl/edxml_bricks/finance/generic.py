import edxml
from edxml.ontology import Brick, DataType
from edxml_bricks.generic import GenericBrick


class FinanceBrick(Brick):
    """
    Brick that defines some object types and concepts from the field of finance.
    """

    OBJECT_BANKING_BIN = 'finance.banking.bin'
    OBJECT_BANKING_SWIFT_CODE = 'finance.banking.swift'

    CONCEPT_COMPANY = GenericBrick.CONCEPT_ORGANIZATION + '.company'
    CONCEPT_BANK = CONCEPT_COMPANY + '.bank'

    @classmethod
    def generate_object_types(cls, target_ontology):
        yield target_ontology.create_object_type(cls.OBJECT_BANKING_BIN) \
            .set_data_type(DataType.string(length=16)) \
            .set_display_name('BIN') \
            .set_description("a Bank Identification Number of a payment card") \
            .set_regex_hard(r'[\d]+') \
            .set_xref('https://en.wikipedia.org/wiki/Payment_card_number#Issuer_identification_number_(IIN)') \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_BANKING_SWIFT_CODE) \
            .set_data_type(DataType.string(length=11)) \
            .set_display_name('SWIFT code') \
            .set_description("an ISO 9362 Business Identifier Code (BIC)") \
            .set_regex_hard(r'[\dA-Z]+') \
            .set_regex_soft(r'[A-Z]{8}([A-Z]{3})?') \
            .set_xref('https://en.wikipedia.org/wiki/ISO_9362') \
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):
        yield target_ontology.create_concept(cls.CONCEPT_COMPANY)\
            .set_display_name('company', 'companies')\
            .set_description('an organization involved in commercial, industrial, or professional activity')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_BANK)\
            .set_display_name('bank')\
            .set_description('a financial institution that accepts deposits and makes loans')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(FinanceBrick)
