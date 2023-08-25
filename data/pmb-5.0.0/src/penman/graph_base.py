from enum import Enum
from os import PathLike
from typing import Any, Dict, List, Tuple
from pathlib import Path

import networkx as nx


__all__ = [
    "_ID",
    "NODE",
    "EDGE",
    "BaseEnum",
    "BaseGraph",
]

def ensure_ext(path: PathLike, extension: str) -> Path:
    """Make sure a path ends with a desired file extension."""
    return (
        Path(path)
        if str(path).endswith(extension)
        else Path(f"{path}{extension}")
    )


class BaseEnum(str, Enum):
    @classmethod
    def all_values(cls) -> List[str]:
        return [i for i in cls]

    def __str__(self):
        return str(self.value)


_ID = Tuple[str, int]
NODE = Tuple[_ID, Dict[str, Any]]
EDGE = Tuple[_ID, _ID, Dict[str, Any]]

class BaseGraph(nx.DiGraph):
    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)

    def from_string(self, input_text: str):
        """Method to construct nodes and edges from input text"""
        raise NotImplementedError("Cannot be called directly.")

    @property
    def type_style_mapping(self):
        """Style per node and/or edge type to use in dot export"""
        raise NotImplementedError("Cannot be called directly.")

    @staticmethod
    def _node_label(node_data) -> str:
        raise NotImplementedError("Overwrite this to create a node label.")

    @staticmethod
    def _edge_label(edge_data) -> str:
        raise NotImplementedError("Overwrite this to create an edge label.")

    def to_pydot(self):
        """Creates a pydot graph object from the graph"""
        import pydot

        p_graph = pydot.Dot()

        token_count: Dict[str, int] = dict()
        node_dict = dict()
        for node_id, node_data in self.nodes.items():
            # Need to do some trickery so no duplicate nodes get added, for
            # example when a synset occurs > 1 times. Example:
            # pmb-4.0.0/data/en/bronze/p00/d0075
            # The tuple ids themselves are not great here.
            tok = node_data["token"]
            if tok in token_count:
                token_count[tok] += 1
                token_id = f"{tok}-{token_count[tok]}"
            else:
                token_id = f"{tok}"
                token_count[tok] = 0
            node_dict[node_id] = token_id

            p_graph.add_node(
                pydot.Node(
                    token_id,
                    **{
                        "label": f'{self._node_label(node_data).replace(":", "-")}',
                        **self.type_style_mapping[node_data["type"]],
                    },
                )
            )

        for (from_id, to_id), edge_data in self.edges.items():
            p_graph.add_edge(
                pydot.Edge(
                    node_dict[from_id],
                    node_dict[to_id],
                    **{
                        "label": f'{self._edge_label(edge_data).replace(":", "-")}',
                        **self.type_style_mapping[edge_data["type"]],
                    },
                )
            )
        return p_graph

    def to_dot_str(self) -> str:
        """Creates a dot graph string from the graph"""
        return self.to_pydot().to_string()

    def to(self, format: str, save_path: PathLike):
        """
        Creates a dot graph visualization and saves it in the provided format
        at the provided path.
        Available formats (NOTE: taken from pydot, not all tested):
            'canon', 'cmap', 'cmapx',
            'cmapx_np', 'dia', 'dot',
            'fig', 'gd', 'gd2', 'gif',
            'hpgl', 'imap', 'imap_np', 'ismap',
            'jpe', 'jpeg', 'jpg', 'mif',
            'mp', 'pcl', 'pdf', 'pic', 'plain',
            'plain-ext', 'png', 'ps', 'ps2',
            'svg', 'svgz', 'vml', 'vmlz',
            'vrml', 'vtx', 'wbmp', 'xdot', 'xlib'
        """
        final_path = str(ensure_ext(save_path, f".{format}").resolve())
        self.to_pydot().write(final_path, format=format)
        return self

    def to_pdf(self, save_path: PathLike):
        """Creates a dot graph pdf and saves it at the provided path"""
        return self.to("pdf", save_path)

    def to_png(self, save_path: PathLike):
        """Creates a dot graph png and saves it at the provided path"""
        return self.to("png", save_path)
