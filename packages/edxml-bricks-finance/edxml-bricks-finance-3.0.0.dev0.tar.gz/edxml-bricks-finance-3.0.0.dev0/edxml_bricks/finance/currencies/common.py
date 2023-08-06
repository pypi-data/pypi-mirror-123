import edxml
from edxml.ontology import Brick, DataType


class CommonCurrenciesBrick(Brick):
    """
    Brick that defines object types for common currencies.
    The object types are named after the ISO 4217 alpha codes.
    """

    OBJECT_CURRENCY_CHF = "finance.currency.chf"
    OBJECT_CURRENCY_CNY = "finance.currency.cny"
    OBJECT_CURRENCY_EUR = "finance.currency.eur"
    OBJECT_CURRENCY_GBP = "finance.currency.gbp"
    OBJECT_CURRENCY_CAD = "finance.currency.cad"
    OBJECT_CURRENCY_JPY = "finance.currency.jpy"
    OBJECT_CURRENCY_USD = "finance.currency.usd"

    @classmethod
    def generate_object_types(cls, target_ontology):
        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CHF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Swiss Francs") \
            .set_unit("Swiss Franc", "CHF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CNY) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Yuan Renminbis") \
            .set_unit("Yuan Renminbi", "CNY") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_EUR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Euros") \
            .set_unit("Euro", "EUR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GBP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Pound Sterlings") \
            .set_unit("Pound Sterling", "GBP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CAD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Canadian Dollars") \
            .set_unit("Canadian Dollar", "CAD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_JPY) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Yens") \
            .set_unit("Yen", "JPY") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_USD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of US Dollars") \
            .set_unit("US Dollar", "USD") \
            .set_version(1)


edxml.ontology.Ontology.register_brick(CommonCurrenciesBrick)
