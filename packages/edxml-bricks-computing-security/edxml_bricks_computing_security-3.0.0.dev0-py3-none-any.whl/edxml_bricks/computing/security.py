import edxml
from edxml.ontology import Brick, DataType
from edxml_bricks.computing.generic import ComputingBrick


class SecurityBrick(Brick):
    """
    Brick that defines some object types and concepts that describe various
    concepts specifically related to computer security.
    """

    OBJECT_MALWARE_SAMPLE_NAME = 'computing.security.malware.sample.name'
    OBJECT_CVSS_VECTOR = 'computing.security.cvss.vector'
    OBJECT_CVSS_SCORE = 'computing.security.cvss.score'
    OBJECT_CVE = 'computing.security.vulnerability.cve'
    OBJECT_BID = 'computing.security.vulnerability.bid'

    CONCEPT_VULNERABILITY_SCANNER = ComputingBrick.CONCEPT_COMPUTER + '.vulnerability-scanner'
    CONCEPT_MALWARE_SAMPLE = 'entity.abstraction.communication.written-communication.writing' \
                             '.coding-system.code.software.malware'
    CONCEPT_THREAT = 'entity.physical-entity.causal-agent.danger.threat'
    CONCEPT_VULNERABILITY = 'entity.abstraction.attribute.state.condition.danger.vulnerability'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_MALWARE_SAMPLE_NAME)\
            .set_description('a name of a malware sample')\
            .set_data_type(DataType.string())\
            .set_display_name('malware sample name')\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CVSS_VECTOR) \
            .set_description('a base vector in the Common Vulnerability Scoring System')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('CVSS base vector')\
            .set_regex_soft('AV:[LAN]/AC:[HML]/Au:[MSN]/C:[NPC]/I:[NPC]/A:[NPC]')\
            .compress()\
            .set_xref('https://en.wikipedia.org/wiki/Common_Vulnerability_Scoring_System')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CVSS_SCORE) \
            .set_description('a base score in the Common Vulnerability Scoring System')\
            .set_data_type(DataType.decimal(total_digits=3, fractional_digits=1, signed=False))\
            .set_display_name('CVSS base score')\
            .set_xref('https://en.wikipedia.org/wiki/Common_Vulnerability_Scoring_System')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CVE) \
            .set_description('a unique identifier of a security vulnerability in the CVE dictionary')\
            .set_data_type(DataType.string(length=255, require_unicode=False, lower_case=False))\
            .set_display_name('CVE number')\
            .set_regex_hard(r'CVE-[\d]{4}-\d+')\
            .set_regex_soft(r'CVE-202\d-00\d{2}')\
            .set_xref('https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_BID) \
            .set_description('a unique identifier of a security vulnerability on Bugtraq')\
            .set_data_type(DataType.int(signed=False))\
            .set_display_name('BID number')\
            .set_xref('https://en.wikipedia.org/wiki/Bugtraq')\
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):
        yield target_ontology.create_concept(cls.CONCEPT_MALWARE_SAMPLE)\
            .set_description('a malicious computer file') \
            .set_display_name('malware sample')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_THREAT)\
            .set_description('a security threat') \
            .set_display_name('security threat')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_VULNERABILITY) \
            .set_description('a security defect reducing a systems\'s information assurance')\
            .set_display_name('vulnerability', 'vulnerabilities')

        yield target_ontology.create_concept(cls.CONCEPT_VULNERABILITY_SCANNER)\
            .set_description('a computer instrumented to perform vulnerability scans')\
            .set_display_name('vulnerability scanner')\
            .set_version(1)


class RiskManagementBrick(Brick):
    """
    Brick that defines some object types and concepts related to risk management in computer security.
    """

    OBJECT_MAGMA_L1_TAG = 'computing.security.management.magma.l1.tag'
    OBJECT_MAGMA_L2_TAG = 'computing.security.management.magma.l2.tag'
    OBJECT_MAGMA_L3_TAG = 'computing.security.management.magma.l3.tag'

    OBJECT_MAGMA_L1_NAME = 'computing.security.management.magma.l1.name'
    OBJECT_MAGMA_L2_NAME = 'computing.security.management.magma.l2.name'
    OBJECT_MAGMA_L3_NAME = 'computing.security.management.magma.l3.name'

    OBJECT_RAVIB_L1_TAG = 'computing.security.management.ravib.l1.tag'
    OBJECT_RAVIB_L2_TAG = 'computing.security.management.ravib.l2.tag'

    OBJECT_RAVIB_L1_NAME = 'computing.security.management.ravib.l1.name'
    OBJECT_RAVIB_L2_NAME = 'computing.security.management.ravib.l2.name'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_MAGMA_L1_TAG) \
            .set_description('a level 1 tag of a use case in the MaGMa framework')\
            .set_data_type(DataType.string(length=255, lower_case=False, require_unicode=False))\
            .set_regex_hard('[A-Z0-9-]*')\
            .set_display_name('MaGMa L1 use case tag')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_MAGMA_L2_TAG) \
            .set_description('a level 2 tag of a use case in the MaGMa framework')\
            .set_data_type(DataType.string(length=255, lower_case=False, require_unicode=False))\
            .set_regex_hard('[A-Z0-9-]*')\
            .set_display_name('MaGMa L2 use case tag')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_MAGMA_L3_TAG) \
            .set_description('a level 3 tag of a use case in the MaGMa framework')\
            .set_data_type(DataType.string(length=255, lower_case=False, require_unicode=False))\
            .set_regex_hard('[A-Z0-9-]*')\
            .set_display_name('MaGMa L3 use case tag')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_MAGMA_L1_NAME) \
            .set_description('a level 1 name of a use case in the MaGMa framework')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('MaGMa L1 use case name')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_MAGMA_L2_NAME) \
            .set_description('a level 2 name of a use case in the MaGMa framework')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('MaGMa L2 use case name')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_MAGMA_L3_NAME) \
            .set_description('a level 3 name of a use case in the MaGMa framework')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('MaGMa L3 use case name')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_RAVIB_L1_TAG) \
            .set_description('a level 1 tag of a threat defined by the RAVIB model')\
            .set_data_type(DataType.string(length=255, lower_case=False, require_unicode=False))\
            .set_regex_hard('[A-Z0-9-]*')\
            .set_display_name('RAVIB L1 threat tag')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_RAVIB_L2_TAG) \
            .set_description('a level 2 tag of a threat defined by the RAVIB model')\
            .set_data_type(DataType.string(length=255, lower_case=False, require_unicode=False))\
            .set_regex_hard('[A-Z0-9-]*')\
            .set_display_name('RAVIB L2 threat tag')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_RAVIB_L1_NAME) \
            .set_description('a level 1 name of a threat defined by the RAVIB model')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('RAVIB L1 threat name')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_RAVIB_L2_NAME) \
            .set_description('a level 2 name of a threat defined by the RAVIB model')\
            .set_data_type(DataType.string(length=255, require_unicode=False))\
            .set_display_name('RAVIB L2 threat name')\
            .set_version(1)


class CryptoBrick(Brick):
    """
    Brick that defines some object types and concepts related to cryptography.
    """

    OBJECT_MD5 = 'computing.crypto.hash.md5'
    OBJECT_SHA1 = 'computing.crypto.hash.sha1'
    OBJECT_SHA256 = 'computing.crypto.hash.sha256'

    OBJECT_CERTIFICATE_DN = 'computing.crypto.certificate.dn'
    OBJECT_CERTIFICATE_CN = 'computing.crypto.certificate.cn'
    OBJECT_CERTIFICATE_FINGERPRINT_SHA1 = 'computing.crypto.certificate.fingerprint.sha1'

    CONCEPT_PUBKEY_CERTIFICATE = 'document.deed.certificate.pk-certificate'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_MD5)\
            .set_description('an MD5 cryptographic hash') \
            .set_data_type(DataType.hex(length=16))\
            .set_display_name('MD5 hash', 'MD5 hashes')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_SHA1)\
            .set_description('a SHA-1 cryptographic hash') \
            .set_data_type(DataType.hex(length=20))\
            .set_display_name('SHA1 hash', 'SHA1 hashes')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_SHA256)\
            .set_description('a SHA-256 cryptographic hash') \
            .set_data_type(DataType.hex(length=32))\
            .set_display_name('SHA256 hash', 'SHA256 hashes')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CERTIFICATE_DN)\
            .set_description('a Distinguished Name of a public key certificate')\
            .set_data_type(DataType.string())\
            .set_display_name('Distinguished Name')\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CERTIFICATE_CN)\
            .set_description('a Common Name of a public key certificate')\
            .set_data_type(DataType.string())\
            .set_display_name('Common Name')\
            .compress()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_CERTIFICATE_FINGERPRINT_SHA1)\
            .set_description('a SHA-1 fingerprint of a public key certificate') \
            .set_data_type(DataType.hex(length=20))\
            .set_display_name('certificate fingerprint')\
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):

        yield target_ontology.create_concept(cls.CONCEPT_PUBKEY_CERTIFICATE) \
            .set_description('a cryptographic public key certificate') \
            .set_display_name('certificate')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(SecurityBrick)
edxml.ontology.Ontology.register_brick(CryptoBrick)
