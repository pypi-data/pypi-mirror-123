import edxml
from edxml.ontology import Brick, DataType


class GeoBrick(Brick):
    """
    Brick that defines generic object types and concepts related to the field of geography.
    """

    OBJECT_COUNTRY_NAME = 'geo.location.country.name'
    OBJECT_COUNTRYCODE_ALPHA2 = 'geo.location.country.iso3166-1-alpha2'
    OBJECT_REGION = 'geo.location.region.name'
    OBJECT_CITY = 'geo.location.city.name'
    OBJECT_LOCATION_GWS84 = 'geo.location.wgs84'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_COUNTRYCODE_ALPHA2) \
            .set_description('an ISO 3166-1 alpha-2 country code')\
            .set_data_type(DataType.string(2, lower_case=False, require_unicode=False))\
            .set_display_name('country code')\
            .set_regex_hard('[A-Z]{2}')\
            .set_xref('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_COUNTRY_NAME) \
            .set_description('a name of a country')\
            .set_data_type(DataType.string())\
            .set_display_name('country', 'countries')\
            .fuzzy_match_phonetic()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_REGION) \
            .set_description('a name of a geopolitical region')\
            .set_data_type(DataType.string())\
            .set_display_name('region')\
            .fuzzy_match_phonetic()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CITY) \
            .set_description('a name of a city')\
            .set_data_type(DataType.string())\
            .set_display_name('city', 'cities')\
            .fuzzy_match_phonetic()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_LOCATION_GWS84) \
            .set_description('a location on Earth, in the WGS84 coordinate system')\
            .set_data_type(DataType.geo_point())\
            .set_display_name('coordinate')\
            .set_xref('https://en.wikipedia.org/wiki/World_Geodetic_System')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(GeoBrick)
