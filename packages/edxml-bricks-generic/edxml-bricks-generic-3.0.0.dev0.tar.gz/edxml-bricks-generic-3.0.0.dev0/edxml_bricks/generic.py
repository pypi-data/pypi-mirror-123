import edxml
from edxml.ontology import Brick, DataType


class GenericBrick(Brick):
    """
    Brick that defines some generic object types and concepts.
    """

    OBJECT_DATETIME = 'datetime'
    OBJECT_SEQUENCE = 'sequence'
    OBJECT_DURATION_SECONDS = 'datetime.duration.seconds'
    OBJECT_BOOLEAN = 'boolean'
    OBJECT_COUNT_SMALL = 'count.small'
    OBJECT_COUNT_BIG = 'count.big'

    OBJECT_PERSON_NAME = 'person.name'
    OBJECT_ORGANIZATION_NAME = 'organization.name'
    OBJECT_ORGANIZATION_UNIT_NAME = 'organization.unit.name'

    CONCEPT_ENTITY = 'entity'
    CONCEPT_ENTITY_PHYSICAL = 'entity.physical-entity'
    CONCEPT_ENTITY_ABSTRACTION = 'entity.abstraction'

    CONCEPT_OBJECT = 'entity.physical-entity.object'
    CONCEPT_WHOLE = 'entity.physical-entity.object.whole'
    CONCEPT_LIVING_THING = 'entity.physical-entity.object.whole.living-thing'
    CONCEPT_ORGANISM = 'entity.physical-entity.object.whole.living-thing.organism'
    CONCEPT_PERSON = 'entity.physical-entity.object.whole.living-thing.organism.person'

    CONCEPT_GROUP = 'entity.abstraction.group'
    CONCEPT_SOCIAL_GROUP = 'entity.abstraction.group.social-group'
    CONCEPT_ORGANIZATION = 'entity.abstraction.group.social-group.organization'

    @classmethod
    def generate_object_types(cls, target_ontology):

        yield target_ontology.create_object_type(cls.OBJECT_DATETIME) \
            .set_description('a date and time in ISO 8601 format')\
            .set_data_type(DataType.datetime())\
            .set_display_name('time stamp')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_DURATION_SECONDS) \
            .set_description('an extent of time')\
            .set_data_type(DataType.double(signed=False))\
            .set_unit('seconds', 's')\
            .set_prefix_radix(60)\
            .set_display_name('time span')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_SEQUENCE) \
            .set_description('a positive integer from a series of consecutive numbers')\
            .set_data_type(DataType.sequence())\
            .set_display_name('sequence number')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_BOOLEAN) \
            .set_description('a boolean value (true or false)') \
            .set_data_type(DataType.boolean()) \
            .set_display_name('boolean value')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_COUNT_SMALL) \
            .set_description('an integer number, representing a quantity')\
            .set_data_type(DataType.small_int(signed=False))\
            .set_display_name('count')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_COUNT_BIG) \
            .set_description('an integer number, representing a quantity') \
            .set_data_type(DataType.big_int(signed=False)) \
            .set_display_name('count')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_PERSON_NAME) \
            .set_description('a name of a person') \
            .set_data_type(DataType.string()) \
            .set_display_name('name')\
            .fuzzy_match_phonetic()\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_ORGANIZATION_NAME) \
            .set_description('a name of an organized group of people with a particular purpose') \
            .set_data_type(DataType.string()) \
            .fuzzy_match_phonetic() \
            .set_display_name('organization name')\
            .set_version(1)

        yield target_ontology.create_object_type(cls.OBJECT_ORGANIZATION_UNIT_NAME) \
            .set_description('a name of a specific unit within an organization') \
            .set_data_type(DataType.string()) \
            .fuzzy_match_phonetic() \
            .set_display_name('unit name')\
            .set_version(1)

    @classmethod
    def generate_concepts(cls, target_ontology):

        yield target_ontology.create_concept(cls.CONCEPT_ENTITY) \
            .set_description('that which is perceived or known or inferred to have its own distinct existence') \
            .set_display_name('entity', 'entities')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_ENTITY_PHYSICAL) \
            .set_description('an entity that has physical existence') \
            .set_display_name('physical entity', 'physical entities')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_ENTITY_ABSTRACTION) \
            .set_description('a concept or idea not associated with any specific instance') \
            .set_display_name('abstraction')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_OBJECT) \
            .set_description('a tangible and visible entity') \
            .set_display_name('object')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_WHOLE) \
            .set_description('an assemblage of parts that is regarded as a single entity') \
            .set_display_name('whole')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_LIVING_THING) \
            .set_description('a living (or once living) entity') \
            .set_display_name('living thing')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_ORGANISM) \
            .set_description('a living thing that has (or can develop) the ability to act or function independently') \
            .set_display_name('organism')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_PERSON) \
            .set_description('a human being') \
            .set_display_name('person', 'people')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_GROUP) \
            .set_description('any number of entities (members) considered as a unit') \
            .set_display_name('group')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_SOCIAL_GROUP) \
            .set_description('a number of people sharing some social relation') \
            .set_display_name('social group')\
            .set_version(1)

        yield target_ontology.create_concept(cls.CONCEPT_ORGANIZATION) \
            .set_description('an organized group of people working together') \
            .set_display_name('organization')\
            .set_version(1)


edxml.ontology.Ontology.register_brick(GenericBrick)
