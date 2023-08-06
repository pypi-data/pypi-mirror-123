import edxml
from edxml.ontology import Brick, DataType


class AllCurrenciesBrick(Brick):
    """
    Brick that defines currency object types. The object types are
    named after the ISO 4217 alpha codes.
    """

    OBJECT_CURRENCY_AED = "finance.currency.aed"
    OBJECT_CURRENCY_AFN = "finance.currency.afn"
    OBJECT_CURRENCY_ALL = "finance.currency.all"
    OBJECT_CURRENCY_AMD = "finance.currency.amd"
    OBJECT_CURRENCY_ANG = "finance.currency.ang"
    OBJECT_CURRENCY_AOA = "finance.currency.aoa"
    OBJECT_CURRENCY_ARS = "finance.currency.ars"
    OBJECT_CURRENCY_AUD = "finance.currency.aud"
    OBJECT_CURRENCY_AWG = "finance.currency.awg"
    OBJECT_CURRENCY_AZN = "finance.currency.azn"
    OBJECT_CURRENCY_BAM = "finance.currency.bam"
    OBJECT_CURRENCY_BBD = "finance.currency.bbd"
    OBJECT_CURRENCY_BDT = "finance.currency.bdt"
    OBJECT_CURRENCY_BGN = "finance.currency.bgn"
    OBJECT_CURRENCY_BHD = "finance.currency.bhd"
    OBJECT_CURRENCY_BIF = "finance.currency.bif"
    OBJECT_CURRENCY_BMD = "finance.currency.bmd"
    OBJECT_CURRENCY_BND = "finance.currency.bnd"
    OBJECT_CURRENCY_BOB = "finance.currency.bob"
    OBJECT_CURRENCY_BOV = "finance.currency.bov"
    OBJECT_CURRENCY_BRL = "finance.currency.brl"
    OBJECT_CURRENCY_BSD = "finance.currency.bsd"
    OBJECT_CURRENCY_BTN = "finance.currency.btn"
    OBJECT_CURRENCY_BWP = "finance.currency.bwp"
    OBJECT_CURRENCY_BYN = "finance.currency.byn"
    OBJECT_CURRENCY_BZD = "finance.currency.bzd"
    OBJECT_CURRENCY_CAD = "finance.currency.cad"
    OBJECT_CURRENCY_CDF = "finance.currency.cdf"
    OBJECT_CURRENCY_CHE = "finance.currency.che"
    OBJECT_CURRENCY_CHF = "finance.currency.chf"
    OBJECT_CURRENCY_CHW = "finance.currency.chw"
    OBJECT_CURRENCY_CLF = "finance.currency.clf"
    OBJECT_CURRENCY_CLP = "finance.currency.clp"
    OBJECT_CURRENCY_CNY = "finance.currency.cny"
    OBJECT_CURRENCY_COP = "finance.currency.cop"
    OBJECT_CURRENCY_COU = "finance.currency.cou"
    OBJECT_CURRENCY_CRC = "finance.currency.crc"
    OBJECT_CURRENCY_CUC = "finance.currency.cuc"
    OBJECT_CURRENCY_CUP = "finance.currency.cup"
    OBJECT_CURRENCY_CVE = "finance.currency.cve"
    OBJECT_CURRENCY_CZK = "finance.currency.czk"
    OBJECT_CURRENCY_DJF = "finance.currency.djf"
    OBJECT_CURRENCY_DKK = "finance.currency.dkk"
    OBJECT_CURRENCY_DOP = "finance.currency.dop"
    OBJECT_CURRENCY_DZD = "finance.currency.dzd"
    OBJECT_CURRENCY_EGP = "finance.currency.egp"
    OBJECT_CURRENCY_ERN = "finance.currency.ern"
    OBJECT_CURRENCY_ETB = "finance.currency.etb"
    OBJECT_CURRENCY_EUR = "finance.currency.eur"
    OBJECT_CURRENCY_FJD = "finance.currency.fjd"
    OBJECT_CURRENCY_FKP = "finance.currency.fkp"
    OBJECT_CURRENCY_GBP = "finance.currency.gbp"
    OBJECT_CURRENCY_GEL = "finance.currency.gel"
    OBJECT_CURRENCY_GHS = "finance.currency.ghs"
    OBJECT_CURRENCY_GIP = "finance.currency.gip"
    OBJECT_CURRENCY_GMD = "finance.currency.gmd"
    OBJECT_CURRENCY_GNF = "finance.currency.gnf"
    OBJECT_CURRENCY_GTQ = "finance.currency.gtq"
    OBJECT_CURRENCY_GYD = "finance.currency.gyd"
    OBJECT_CURRENCY_HKD = "finance.currency.hkd"
    OBJECT_CURRENCY_HNL = "finance.currency.hnl"
    OBJECT_CURRENCY_HRK = "finance.currency.hrk"
    OBJECT_CURRENCY_HTG = "finance.currency.htg"
    OBJECT_CURRENCY_HUF = "finance.currency.huf"
    OBJECT_CURRENCY_IDR = "finance.currency.idr"
    OBJECT_CURRENCY_ILS = "finance.currency.ils"
    OBJECT_CURRENCY_INR = "finance.currency.inr"
    OBJECT_CURRENCY_IQD = "finance.currency.iqd"
    OBJECT_CURRENCY_IRR = "finance.currency.irr"
    OBJECT_CURRENCY_ISK = "finance.currency.isk"
    OBJECT_CURRENCY_JMD = "finance.currency.jmd"
    OBJECT_CURRENCY_JOD = "finance.currency.jod"
    OBJECT_CURRENCY_JPY = "finance.currency.jpy"
    OBJECT_CURRENCY_KES = "finance.currency.kes"
    OBJECT_CURRENCY_KGS = "finance.currency.kgs"
    OBJECT_CURRENCY_KHR = "finance.currency.khr"
    OBJECT_CURRENCY_KMF = "finance.currency.kmf"
    OBJECT_CURRENCY_KPW = "finance.currency.kpw"
    OBJECT_CURRENCY_KRW = "finance.currency.krw"
    OBJECT_CURRENCY_KWD = "finance.currency.kwd"
    OBJECT_CURRENCY_KYD = "finance.currency.kyd"
    OBJECT_CURRENCY_KZT = "finance.currency.kzt"
    OBJECT_CURRENCY_LAK = "finance.currency.lak"
    OBJECT_CURRENCY_LBP = "finance.currency.lbp"
    OBJECT_CURRENCY_LKR = "finance.currency.lkr"
    OBJECT_CURRENCY_LRD = "finance.currency.lrd"
    OBJECT_CURRENCY_LSL = "finance.currency.lsl"
    OBJECT_CURRENCY_LYD = "finance.currency.lyd"
    OBJECT_CURRENCY_MAD = "finance.currency.mad"
    OBJECT_CURRENCY_MDL = "finance.currency.mdl"
    OBJECT_CURRENCY_MGA = "finance.currency.mga"
    OBJECT_CURRENCY_MKD = "finance.currency.mkd"
    OBJECT_CURRENCY_MMK = "finance.currency.mmk"
    OBJECT_CURRENCY_MNT = "finance.currency.mnt"
    OBJECT_CURRENCY_MOP = "finance.currency.mop"
    OBJECT_CURRENCY_MRU = "finance.currency.mru"
    OBJECT_CURRENCY_MUR = "finance.currency.mur"
    OBJECT_CURRENCY_MVR = "finance.currency.mvr"
    OBJECT_CURRENCY_MWK = "finance.currency.mwk"
    OBJECT_CURRENCY_MXN = "finance.currency.mxn"
    OBJECT_CURRENCY_MYR = "finance.currency.myr"
    OBJECT_CURRENCY_MZN = "finance.currency.mzn"
    OBJECT_CURRENCY_NAD = "finance.currency.nad"
    OBJECT_CURRENCY_NGN = "finance.currency.ngn"
    OBJECT_CURRENCY_NIO = "finance.currency.nio"
    OBJECT_CURRENCY_NOK = "finance.currency.nok"
    OBJECT_CURRENCY_NPR = "finance.currency.npr"
    OBJECT_CURRENCY_NZD = "finance.currency.nzd"
    OBJECT_CURRENCY_OMR = "finance.currency.omr"
    OBJECT_CURRENCY_PAB = "finance.currency.pab"
    OBJECT_CURRENCY_PEN = "finance.currency.pen"
    OBJECT_CURRENCY_PGK = "finance.currency.pgk"
    OBJECT_CURRENCY_PHP = "finance.currency.php"
    OBJECT_CURRENCY_PKR = "finance.currency.pkr"
    OBJECT_CURRENCY_PLN = "finance.currency.pln"
    OBJECT_CURRENCY_PYG = "finance.currency.pyg"
    OBJECT_CURRENCY_QAR = "finance.currency.qar"
    OBJECT_CURRENCY_RON = "finance.currency.ron"
    OBJECT_CURRENCY_RSD = "finance.currency.rsd"
    OBJECT_CURRENCY_RUB = "finance.currency.rub"
    OBJECT_CURRENCY_RWF = "finance.currency.rwf"
    OBJECT_CURRENCY_SAR = "finance.currency.sar"
    OBJECT_CURRENCY_SBD = "finance.currency.sbd"
    OBJECT_CURRENCY_SCR = "finance.currency.scr"
    OBJECT_CURRENCY_SDG = "finance.currency.sdg"
    OBJECT_CURRENCY_SEK = "finance.currency.sek"
    OBJECT_CURRENCY_SGD = "finance.currency.sgd"
    OBJECT_CURRENCY_SHP = "finance.currency.shp"
    OBJECT_CURRENCY_SLL = "finance.currency.sll"
    OBJECT_CURRENCY_SOS = "finance.currency.sos"
    OBJECT_CURRENCY_SRD = "finance.currency.srd"
    OBJECT_CURRENCY_SSP = "finance.currency.ssp"
    OBJECT_CURRENCY_STN = "finance.currency.stn"
    OBJECT_CURRENCY_SVC = "finance.currency.svc"
    OBJECT_CURRENCY_SYP = "finance.currency.syp"
    OBJECT_CURRENCY_SZL = "finance.currency.szl"
    OBJECT_CURRENCY_THB = "finance.currency.thb"
    OBJECT_CURRENCY_TJS = "finance.currency.tjs"
    OBJECT_CURRENCY_TMT = "finance.currency.tmt"
    OBJECT_CURRENCY_TND = "finance.currency.tnd"
    OBJECT_CURRENCY_TOP = "finance.currency.top"
    OBJECT_CURRENCY_TRY = "finance.currency.try"
    OBJECT_CURRENCY_TTD = "finance.currency.ttd"
    OBJECT_CURRENCY_TWD = "finance.currency.twd"
    OBJECT_CURRENCY_TZS = "finance.currency.tzs"
    OBJECT_CURRENCY_UAH = "finance.currency.uah"
    OBJECT_CURRENCY_UGX = "finance.currency.ugx"
    OBJECT_CURRENCY_USD = "finance.currency.usd"
    OBJECT_CURRENCY_UYU = "finance.currency.uyu"
    OBJECT_CURRENCY_UYW = "finance.currency.uyw"
    OBJECT_CURRENCY_UZS = "finance.currency.uzs"
    OBJECT_CURRENCY_VES = "finance.currency.ves"
    OBJECT_CURRENCY_VND = "finance.currency.vnd"
    OBJECT_CURRENCY_VUV = "finance.currency.vuv"
    OBJECT_CURRENCY_WST = "finance.currency.wst"
    OBJECT_CURRENCY_XAF = "finance.currency.xaf"
    OBJECT_CURRENCY_XCD = "finance.currency.xcd"
    OBJECT_CURRENCY_XOF = "finance.currency.xof"
    OBJECT_CURRENCY_XPF = "finance.currency.xpf"
    OBJECT_CURRENCY_XSU = "finance.currency.xsu"
    OBJECT_CURRENCY_XUA = "finance.currency.xua"
    OBJECT_CURRENCY_YER = "finance.currency.yer"
    OBJECT_CURRENCY_ZAR = "finance.currency.zar"
    OBJECT_CURRENCY_ZMW = "finance.currency.zmw"
    OBJECT_CURRENCY_ZWL = "finance.currency.zwl"

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AED) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of UAE Dirhams") \
            .set_unit("UAE Dirham", "AED") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AFN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Afghanis") \
            .set_unit("Afghani", "AFN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ALL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Leks") \
            .set_unit("Lek", "ALL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AMD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Armenian Drams") \
            .set_unit("Armenian Dram", "AMD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ANG) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Netherlands Antillean Guilders") \
            .set_unit("Netherlands Antillean Guilder", "ANG") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AOA) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Kwanzas") \
            .set_unit("Kwanza", "AOA") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ARS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Argentine Pesos") \
            .set_unit("Argentine Peso", "ARS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AUD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Australian Dollars") \
            .set_unit("Australian Dollar", "AUD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AWG) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Aruban Florins") \
            .set_unit("Aruban Florin", "AWG") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_AZN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Azerbaijan Manats") \
            .set_unit("Azerbaijan Manat", "AZN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BAM) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Convertible Marks") \
            .set_unit("Convertible Mark", "BAM") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BBD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Barbados Dollars") \
            .set_unit("Barbados Dollar", "BBD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BDT) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Takas") \
            .set_unit("Taka", "BDT") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BGN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bulgarian Levs") \
            .set_unit("Bulgarian Lev", "BGN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BHD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bahraini Dinars") \
            .set_unit("Bahraini Dinar", "BHD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BIF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Burundi Francs") \
            .set_unit("Burundi Franc", "BIF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BMD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bermudian Dollars") \
            .set_unit("Bermudian Dollar", "BMD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BND) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Brunei Dollars") \
            .set_unit("Brunei Dollar", "BND") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BOB) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bolivianos") \
            .set_unit("Boliviano", "BOB") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BOV) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Mvdols") \
            .set_unit("Mvdol", "BOV") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BRL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Brazilian Reals") \
            .set_unit("Brazilian Real", "BRL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BSD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bahamian Dollars") \
            .set_unit("Bahamian Dollar", "BSD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BTN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Ngultrums") \
            .set_unit("Ngultrum", "BTN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BWP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Pulas") \
            .set_unit("Pula", "BWP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BYN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Belarusian Rubles") \
            .set_unit("Belarusian Ruble", "BYN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_BZD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Belize Dollars") \
            .set_unit("Belize Dollar", "BZD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CAD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Canadian Dollars") \
            .set_unit("Canadian Dollar", "CAD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CDF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Congolese Francs") \
            .set_unit("Congolese Franc", "CDF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CHE) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of WIR Euros") \
            .set_unit("WIR Euro", "CHE") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CHF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Swiss Francs") \
            .set_unit("Swiss Franc", "CHF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CHW) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of WIR Francs") \
            .set_unit("WIR Franc", "CHW") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CLF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Unidad de Fomentos") \
            .set_unit("Unidad de Fomento", "CLF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CLP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Chilean Pesos") \
            .set_unit("Chilean Peso", "CLP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CNY) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Yuan Renminbis") \
            .set_unit("Yuan Renminbi", "CNY") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_COP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Colombian Pesos") \
            .set_unit("Colombian Peso", "COP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_COU) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Unidad de Valor Reals") \
            .set_unit("Unidad de Valor Real", "COU") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CRC) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Costa Rican Colons") \
            .set_unit("Costa Rican Colon", "CRC") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CUC) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Peso Convertibles") \
            .set_unit("Peso Convertible", "CUC") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CUP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Cuban Pesos") \
            .set_unit("Cuban Peso", "CUP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CVE) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Cabo Verde Escudos") \
            .set_unit("Cabo Verde Escudo", "CVE") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_CZK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Czech Korunas") \
            .set_unit("Czech Koruna", "CZK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_DJF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Djibouti Francs") \
            .set_unit("Djibouti Franc", "DJF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_DKK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Danish Krones") \
            .set_unit("Danish Krone", "DKK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_DOP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Dominican Pesos") \
            .set_unit("Dominican Peso", "DOP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_DZD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Algerian Dinars") \
            .set_unit("Algerian Dinar", "DZD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_EGP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Egyptian Pounds") \
            .set_unit("Egyptian Pound", "EGP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ERN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Nakfas") \
            .set_unit("Nakfa", "ERN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ETB) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Ethiopian Birrs") \
            .set_unit("Ethiopian Birr", "ETB") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_EUR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Euros") \
            .set_unit("Euro", "EUR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_FJD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Fiji Dollars") \
            .set_unit("Fiji Dollar", "FJD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_FKP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Falkland Islands Pounds") \
            .set_unit("Falkland Islands Pound", "FKP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GBP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Pound Sterlings") \
            .set_unit("Pound Sterling", "GBP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GEL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Laris") \
            .set_unit("Lari", "GEL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GHS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Ghana Cedis") \
            .set_unit("Ghana Cedi", "GHS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GIP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Gibraltar Pounds") \
            .set_unit("Gibraltar Pound", "GIP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GMD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Dalasis") \
            .set_unit("Dalasi", "GMD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GNF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Guinean Francs") \
            .set_unit("Guinean Franc", "GNF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GTQ) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Quetzals") \
            .set_unit("Quetzal", "GTQ") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_GYD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Guyana Dollars") \
            .set_unit("Guyana Dollar", "GYD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_HKD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Hong Kong Dollars") \
            .set_unit("Hong Kong Dollar", "HKD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_HNL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Lempiras") \
            .set_unit("Lempira", "HNL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_HRK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Kunas") \
            .set_unit("Kuna", "HRK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_HTG) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Gourdes") \
            .set_unit("Gourde", "HTG") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_HUF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Forints") \
            .set_unit("Forint", "HUF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_IDR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Rupiahs") \
            .set_unit("Rupiah", "IDR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ILS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of New Israeli Sheqels") \
            .set_unit("New Israeli Sheqel", "ILS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_INR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Indian Rupees") \
            .set_unit("Indian Rupee", "INR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_IQD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Iraqi Dinars") \
            .set_unit("Iraqi Dinar", "IQD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_IRR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Iranian Rials") \
            .set_unit("Iranian Rial", "IRR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ISK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Iceland Kronas") \
            .set_unit("Iceland Krona", "ISK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_JMD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Jamaican Dollars") \
            .set_unit("Jamaican Dollar", "JMD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_JOD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Jordanian Dinars") \
            .set_unit("Jordanian Dinar", "JOD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_JPY) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Yens") \
            .set_unit("Yen", "JPY") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KES) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Kenyan Shillings") \
            .set_unit("Kenyan Shilling", "KES") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KGS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Soms") \
            .set_unit("Som", "KGS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KHR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Riels") \
            .set_unit("Riel", "KHR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KMF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Comorian Francs") \
            .set_unit("Comorian Franc", "KMF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KPW) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of North Korean Wons") \
            .set_unit("North Korean Won", "KPW") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KRW) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Wons") \
            .set_unit("Won", "KRW") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KWD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Kuwaiti Dinars") \
            .set_unit("Kuwaiti Dinar", "KWD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KYD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Cayman Islands Dollars") \
            .set_unit("Cayman Islands Dollar", "KYD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_KZT) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Tenges") \
            .set_unit("Tenge", "KZT") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_LAK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Lao Kips") \
            .set_unit("Lao Kip", "LAK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_LBP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Lebanese Pounds") \
            .set_unit("Lebanese Pound", "LBP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_LKR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Sri Lanka Rupees") \
            .set_unit("Sri Lanka Rupee", "LKR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_LRD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Liberian Dollars") \
            .set_unit("Liberian Dollar", "LRD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_LSL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Lotis") \
            .set_unit("Loti", "LSL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_LYD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Libyan Dinars") \
            .set_unit("Libyan Dinar", "LYD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MAD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Moroccan Dirhams") \
            .set_unit("Moroccan Dirham", "MAD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MDL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Moldovan Leus") \
            .set_unit("Moldovan Leu", "MDL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MGA) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Malagasy Ariarys") \
            .set_unit("Malagasy Ariary", "MGA") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MKD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Denars") \
            .set_unit("Denar", "MKD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MMK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Kyats") \
            .set_unit("Kyat", "MMK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MNT) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Tugriks") \
            .set_unit("Tugrik", "MNT") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MOP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Patacas") \
            .set_unit("Pataca", "MOP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MRU) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Ouguiyas") \
            .set_unit("Ouguiya", "MRU") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MUR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Mauritius Rupees") \
            .set_unit("Mauritius Rupee", "MUR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MVR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Rufiyaas") \
            .set_unit("Rufiyaa", "MVR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MWK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Malawi Kwachas") \
            .set_unit("Malawi Kwacha", "MWK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MXN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Mexican Pesos") \
            .set_unit("Mexican Peso", "MXN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MYR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Malaysian Ringgits") \
            .set_unit("Malaysian Ringgit", "MYR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_MZN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Mozambique Meticals") \
            .set_unit("Mozambique Metical", "MZN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_NAD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Namibia Dollars") \
            .set_unit("Namibia Dollar", "NAD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_NGN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Nairas") \
            .set_unit("Naira", "NGN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_NIO) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Cordoba Oros") \
            .set_unit("Cordoba Oro", "NIO") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_NOK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Norwegian Krones") \
            .set_unit("Norwegian Krone", "NOK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_NPR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Nepalese Rupees") \
            .set_unit("Nepalese Rupee", "NPR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_NZD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of New Zealand Dollars") \
            .set_unit("New Zealand Dollar", "NZD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_OMR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Rial Omanis") \
            .set_unit("Rial Omani", "OMR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PAB) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Balboas") \
            .set_unit("Balboa", "PAB") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PEN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Sols") \
            .set_unit("Sol", "PEN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PGK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Kinas") \
            .set_unit("Kina", "PGK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PHP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Philippine Pesos") \
            .set_unit("Philippine Peso", "PHP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PKR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Pakistan Rupees") \
            .set_unit("Pakistan Rupee", "PKR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PLN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Zlotys") \
            .set_unit("Zloty", "PLN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_PYG) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Guaranis") \
            .set_unit("Guarani", "PYG") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_QAR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Qatari Rials") \
            .set_unit("Qatari Rial", "QAR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_RON) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Romanian Leus") \
            .set_unit("Romanian Leu", "RON") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_RSD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Serbian Dinars") \
            .set_unit("Serbian Dinar", "RSD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_RUB) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Russian Rubles") \
            .set_unit("Russian Ruble", "RUB") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_RWF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Rwanda Francs") \
            .set_unit("Rwanda Franc", "RWF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SAR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Saudi Riyals") \
            .set_unit("Saudi Riyal", "SAR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SBD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Solomon Islands Dollars") \
            .set_unit("Solomon Islands Dollar", "SBD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SCR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Seychelles Rupees") \
            .set_unit("Seychelles Rupee", "SCR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SDG) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Sudanese Pounds") \
            .set_unit("Sudanese Pound", "SDG") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SEK) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Swedish Kronas") \
            .set_unit("Swedish Krona", "SEK") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SGD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Singapore Dollars") \
            .set_unit("Singapore Dollar", "SGD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SHP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Saint Helena Pounds") \
            .set_unit("Saint Helena Pound", "SHP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SLL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Leones") \
            .set_unit("Leone", "SLL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SOS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Somali Shillings") \
            .set_unit("Somali Shilling", "SOS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SRD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Surinam Dollars") \
            .set_unit("Surinam Dollar", "SRD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SSP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of South Sudanese Pounds") \
            .set_unit("South Sudanese Pound", "SSP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_STN) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Dobras") \
            .set_unit("Dobra", "STN") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SVC) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of El Salvador Colons") \
            .set_unit("El Salvador Colon", "SVC") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SYP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Syrian Pounds") \
            .set_unit("Syrian Pound", "SYP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_SZL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Lilangenis") \
            .set_unit("Lilangeni", "SZL") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_THB) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bahts") \
            .set_unit("Baht", "THB") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TJS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Somonis") \
            .set_unit("Somoni", "TJS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TMT) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Turkmenistan New Manats") \
            .set_unit("Turkmenistan New Manat", "TMT") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TND) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Tunisian Dinars") \
            .set_unit("Tunisian Dinar", "TND") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TOP) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Pa’angas") \
            .set_unit("Pa’anga", "TOP") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TRY) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Turkish Liras") \
            .set_unit("Turkish Lira", "TRY") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TTD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Trinidad and Tobago Dollars") \
            .set_unit("Trinidad and Tobago Dollar", "TTD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TWD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of New Taiwan Dollars") \
            .set_unit("New Taiwan Dollar", "TWD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_TZS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Tanzanian Shillings") \
            .set_unit("Tanzanian Shilling", "TZS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_UAH) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Hryvnias") \
            .set_unit("Hryvnia", "UAH") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_UGX) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Uganda Shillings") \
            .set_unit("Uganda Shilling", "UGX") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_USD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of US Dollars") \
            .set_unit("US Dollar", "USD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_UYU) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Peso Uruguayos") \
            .set_unit("Peso Uruguayo", "UYU") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_UYW) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Unidad Previsionals") \
            .set_unit("Unidad Previsional", "UYW") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_UZS) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Uzbekistan Sums") \
            .set_unit("Uzbekistan Sum", "UZS") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_VES) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Bolívar Soberanos") \
            .set_unit("Bolívar Soberano", "VES") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_VND) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Dongs") \
            .set_unit("Dong", "VND") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_VUV) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Vatus") \
            .set_unit("Vatu", "VUV") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_WST) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Talas") \
            .set_unit("Tala", "WST") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_XAF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of CFA Franc BEACs") \
            .set_unit("CFA Franc BEAC", "XAF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_XCD) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of East Caribbean Dollars") \
            .set_unit("East Caribbean Dollar", "XCD") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_XOF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of CFA Franc BCEAOs") \
            .set_unit("CFA Franc BCEAO", "XOF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_XPF) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of CFP Francs") \
            .set_unit("CFP Franc", "XPF") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_XSU) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Sucres") \
            .set_unit("Sucre", "XSU") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_XUA) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of ADB Unit of Accounts") \
            .set_unit("ADB Unit of Account", "XUA") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_YER) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Yemeni Rials") \
            .set_unit("Yemeni Rial", "YER") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ZAR) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Rands") \
            .set_unit("Rand", "ZAR") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ZMW) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Zambian Kwachas") \
            .set_unit("Zambian Kwacha", "ZMW") \
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CURRENCY_ZWL) \
            .set_data_type(DataType.currency()) \
            .set_display_name('amount') \
            .set_description("an amount of Zimbabwe Dollars") \
            .set_unit("Zimbabwe Dollar", "ZWL") \
            .set_version(1)


edxml.ontology.Ontology.register_brick(AllCurrenciesBrick)
