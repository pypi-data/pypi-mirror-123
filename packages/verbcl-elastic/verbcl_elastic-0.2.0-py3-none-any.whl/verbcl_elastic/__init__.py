"""VerbCL Elastic."""
import multiprocessing
from typing import Any
from typing import List

from elasticsearch_dsl import analyzer
from elasticsearch_dsl import Boolean
from elasticsearch_dsl import connections
from elasticsearch_dsl import Document
from elasticsearch_dsl import Float
from elasticsearch_dsl import Integer
from elasticsearch_dsl import Text


class OpinionDocument(Document):  # type: ignore
    """Court Opinion."""

    opinion_id = Integer()
    raw_text = Text(
        analyzer=analyzer(
            "alpha_stop_stem",
            type="custom",
            tokenizer="classic",
            filter=["lowercase", "asciifolding", "stop", "snowball"],
        )
    )

    class Index:
        """Index Name for OpinionDocument."""

        name = "verbcl_opinions"

    @property
    def key(self) -> int:
        """Unique Key to identify one document."""
        # noinspection PyTypeChecker
        return self.opinion_id  # type: ignore


class OpinionSentence(Document):  # type: ignore
    """Single Sentence within a Court Opinion."""

    opinion_id = Integer()
    sentence_id = Integer()
    highlight = Boolean()
    count_citations = Integer()
    raw_text = Text(
        analyzer=analyzer(
            "alpha_stop_stem",
            type="custom",
            tokenizer="classic",
            filter=["lowercase", "asciifolding", "stop", "snowball"],
        )
    )

    class Index:
        """Index Name for OpinionSentence."""

        name = "verbcl_highlights"

    def save(self, **kwargs: Any) -> bool:
        """Overloads save to implement defaut values."""
        if self.highlight is None:
            self.highlight = False
        if self.count_citations is None:
            self.count_citations = 0

        return super().save(**kwargs)  # type: ignore

    @property
    def key(self) -> str:
        """Unique key to identify one sentence."""
        # noinspection PyTypeChecker
        return f"{self.opinion_id}-{self.sentence_id}"


class OpinionCitationGraph(Document):  # type: ignore
    """Citation of a Cited Opinion in a Citing Opinion, using a specific sentence of the Cited Opinion."""

    citing_opinion_id = Integer()
    cited_opinion_id = Integer()
    cited_sentence_id = Integer()
    verbatim = Text(
        analyzer=analyzer(
            "alpha_stop_stem",
            type="custom",
            tokenizer="classic",
            filter=["lowercase", "asciifolding", "stop", "snowball"],
        )
    )
    snippet = Text(
        analyzer=analyzer(
            "alpha_stop_stem",
            type="custom",
            tokenizer="classic",
            filter=["lowercase", "asciifolding", "stop", "snowball"],
        )
    )
    score = Float()

    class Index:
        """Index Name for OpinioNCitationGraph."""

        name = "verbcl_citation_graph"


def _create_connection(alias_name: str, **kwargs: Any) -> None:
    """
    Add an elasticsearch instance connection to the DSL classes, using an alias.

    :param alias_name
    """
    connections.create_connection(alias=alias_name, **kwargs)


# Global state variables for the connection management
_class_init: bool = False
_list_aliases: List[str] = []
_default_connection: str = "default"


def verbcl_es_init(**kwargs: Any) -> str:
    """
    Manages connections to ElasticSearch instance. There is one connection per process.

    :param kwargs: parameters for creating an elasticsearch connection
    :return: alias name for the connection to use
    """
    # Initialize the connection to Elasticsearch
    # Making use of elasticsearch_dsl persistence features
    proc = multiprocessing.current_process()
    alias_name = proc.name

    global _list_aliases
    if alias_name in _list_aliases:
        return alias_name

    _create_connection(alias_name=alias_name, **kwargs)
    _list_aliases.append(alias_name)

    global _class_init
    if not _class_init:
        # Always have a connection named "default"
        if _default_connection not in _list_aliases:
            _create_connection(_default_connection)

        OpinionDocument.init()
        OpinionSentence.init()
        OpinionCitationGraph.init()
        _class_init = True

    return alias_name
