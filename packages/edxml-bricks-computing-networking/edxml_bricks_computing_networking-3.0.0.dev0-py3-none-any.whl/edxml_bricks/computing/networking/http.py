import edxml
from edxml.ontology import Brick, DataType


class HttpBrick(Brick):
    """
    Brick that defines some object types and concepts that are specific to the HTTP protocol.
    """

    OBJECT_HTTP_URL = 'computing.networking.http.resource'
    OBJECT_HTTP_STATUS = 'computing.networking.http.response.status'
    OBJECT_HTTP_METHOD = 'computing.networking.http.method'
    OBJECT_HTTP_QUERY = 'computing.networking.http.query'
    OBJECT_HTTP_AGENT = 'computing.networking.http.user-agent'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_HTTP_URL)\
            .set_description('a locator for an HTTP resource') \
            .set_data_type(DataType.uri()) \
            .set_display_name('HTTP resource locator') \
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HTTP_STATUS)\
            .set_description('an HTTP response status') \
            .set_data_type(DataType.small_int(signed=False)) \
            .set_display_name('HTTP response status', 'HTTP response statuses')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HTTP_METHOD)\
            .set_description('an HTTP request method') \
            .set_data_type(DataType.string(255, require_unicode=False, lower_case=False)) \
            .set_display_name('HTTP request method')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HTTP_QUERY)\
            .set_description('a query part of a HTTP request') \
            .set_data_type(DataType.string()) \
            .set_display_name('HTTP query', 'HTTP queries') \
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HTTP_AGENT)\
            .set_description('an HTTP user agent') \
            .set_data_type(DataType.string(reverse_storage=True)) \
            .set_display_name('HTTP user agent') \
            .compress()\
            .set_version(1)


edxml.ontology.Ontology.register_brick(HttpBrick)
