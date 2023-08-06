import edxml
from edxml.ontology import Brick, DataType
from edxml_bricks.computing.generic import ComputingBrick


class NetworkingBrick(Brick):
    """
    Brick that defines some object types and concepts from the field of computer networking.
    """

    OBJECT_HOST_NAME = 'computing.networking.host.dns-name'
    OBJECT_HOST_NAME_WILDCARD = 'computing.networking.host.dns-name.wildcard'
    OBJECT_HOST_IPV4 = 'computing.networking.host.ipv4'
    OBJECT_HOST_IPV6 = 'computing.networking.host.ipv6'
    OBJECT_HOST_PORT = 'computing.networking.host.port'
    OBJECT_HOST_MAC = 'computing.networking.host.mac'

    OBJECT_NETWORK_CIDR_IPV4 = 'computing.networking.network.cidr.ipv4'
    OBJECT_NETWORK_CIDR_IPV6 = 'computing.networking.network.cidr.ipv6'

    OBJECT_PROTO_NUM = 'computing.networking.protocol.number'
    OBJECT_PROTOCOL_KEYWORD = 'computing.networking.protocol.keyword'

    CONCEPT_NETWORK_ROUTER = ComputingBrick.CONCEPT_COMPUTER + '.router'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_HOST_IPV4) \
            .set_description('an IPv4 address of a computer in a computer network')\
            .set_data_type(DataType.ip_v4())\
            .set_display_name('IPv4 address', 'IPv4 addresses')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HOST_IPV6) \
            .set_description('an IPv6 address of a computer in a computer network')\
            .set_data_type(DataType.ip_v6())\
            .set_display_name('IPv6 address', 'IPv6 addresses')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HOST_PORT) \
            .set_description('a TCP/IP networking port, consisting of a number followed by a '
                             'slash and protocol (TCP or UDP)')\
            .set_data_type(DataType.string(64, lower_case=False, require_unicode=False))\
            .set_regex_hard(r'\d+/(TCP|UDP)')\
            .set_display_name('TCP/IP network port')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HOST_NAME) \
            .set_description('a DNS name of a computer in a computer network')\
            .set_data_type(DataType.string(255, upper_case=False, reverse_storage=True, require_unicode=False))\
            .set_display_name('DNS name')\
            .fuzzy_match_tail(10)\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HOST_NAME_WILDCARD) \
            .set_description('a wildcard DNS name of set of computers in a computer network')\
            .set_data_type(DataType.string(255, upper_case=False, reverse_storage=True, require_unicode=False))\
            .set_display_name('wildcard host name')\
            .fuzzy_match_tail(10)\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_HOST_MAC) \
            .set_description('a MAC address of a physical network interface card')\
            .set_data_type(DataType.hex(length=6, separator=':', group_size=1))\
            .set_display_name('MAC address', 'MAC addresses')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_NETWORK_CIDR_IPV4) \
            .set_description('a block of IPv4 addresses in CIDR notation')\
            .set_data_type(DataType.string(length=18))\
            .set_regex_hard(r'((1?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]).){3}(1?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])/[0-9]{1,2}')\
            .set_display_name('IPv4 CIDR')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_NETWORK_CIDR_IPV6) \
            .set_description('a block of IPv6 addresses in CIDR notation')\
            .set_data_type(DataType.string(length=43))\
            .set_regex_hard(r'[a-f\d]{4}(:[a-f\d]{4}){7}/[\d]{1,3}')\
            .set_display_name('IPv6 CIDR')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_PROTO_NUM) \
            .set_description('an IANA internet protocol number')\
            .set_data_type(DataType.tiny_int(signed=False))\
            .set_display_name('protocol number')\
            .set_xref('https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_PROTOCOL_KEYWORD) \
            .set_description('a keyword of an IANA assigned internet protocol')\
            .set_data_type(DataType.string(24))\
            .set_display_name('internet protocol')\
            .set_xref('https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml')\
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):

        yield target_ontology.create_concept(cls.CONCEPT_NETWORK_ROUTER)\
            .set_description('a networking device that forwards data packets between computer networks')\
            .set_display_name('network router')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(NetworkingBrick)
