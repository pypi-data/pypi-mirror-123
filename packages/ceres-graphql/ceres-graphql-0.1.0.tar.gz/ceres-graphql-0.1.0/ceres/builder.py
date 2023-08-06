from __future__ import annotations

from typing import Collection

from graphql import (
    GraphQLDirective,
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLOutputType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
)

__all__ = ("SchemaBuilder",)


class SchemaBuilder:
    """
    The schema builder provides an interface to incrementally
    create your GraphQL schema.

    :param auto_camelcase: Whether schema types should be converted
        to camelcase, for better compatibility with GraphQL clients.
    """

    def __init__(self, auto_camelcase: bool = True) -> None:
        #: The schema registry is used to store output types.
        #: It is used in finding resolver types, when schema types
        #: provided happen to be a string.
        self.__registry: dict[str, GraphQLOutputType] = {}
        self.auto_camelcase = auto_camelcase

    def create_schema(
        self,
        description: str | None = None,
        directives: Collection[GraphQLDirective] | None = None,
    ) -> GraphQLSchema:
        """
        Creates a GraphQLSchema instance with the
        types collected in the registry.

        :param description: The description of the schema.
        :param directives: The directives to add to the schema.
        :return: The created GraphQL schema.
        """
        pass

    def add_builder(self, builder: SchemaBuilder) -> None:
        """
        Adds the schema types that the builder has to the registry.

        :param builder: The builder to extract schema types from.
        """
        pass

    def add_object_type(
        self, name: str, description: str | None = None
    ) -> GraphQLObjectType:
        """
        Stores the given object type in the registry.

        :param name: The name of the object type.
        :param description: The description of the object type.
        :return: The added object type.
        """
        pass

    def add_input_object_type(
        self, name: str, description: str | None = None
    ) -> GraphQLInputObjectType:
        """
        Stores the given input object type in the registry.

        :param name: The name of the input object type.
        :param description: The description of the input object type.
        :return: The added input object type.
        """
        pass

    def add_scalar_type(
        self,
        name: str,
        description: str | None = None,
        specified_by_url: str | None = None,
    ) -> GraphQLScalarType:
        """
        Stores the given scalar type in the registry.

        :param name: The name of the scalar type.
        :param description: The description of the scalar type.
        :param specified_by_url: The URI pointing to a document holding
            data-format, serialization, and coercion rules for the scalar.
        :return: The added scalar type.

        TODO: I think it would be better to define a scalar like:

        class MyScalar(Scalar):
            def parse(self, ...):
                ...

        builder.add_scalar_type(scalar=MyScalar)
        """
        pass

    def add_enum_type(
        self, name: str, description: str | None = None
    ) -> GraphQLEnumType:
        """
        Stores the given enum type in the registry.

        :param name: The name of the enum type.
        :param description: The description of the enum type.
        :return: The added enum type.
        """
        pass

    def add_union_type(
        self, name: str, description: str | None = None
    ) -> GraphQLUnionType:
        """
        Stores the given union type in the registry.

        :param name: The name of the union type.
        :param description: The description of the union type.
        :return: The added union type.
        """
        pass

    def add_interface_type(
        self, name: str, description: str | None = None
    ) -> GraphQLInterfaceType:
        """
        Stores the given interface type in the registry.

        :param name: The name of the interface type.
        :param description: The description of the interface type.
        :return: The added interface type.
        """
        pass
