from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any, Iterator, Iterable, Callable, List


@dataclass
class Node:
    name: str
    parent: Optional["Node"] = field(default=None, repr=False)
    children: List["Node"] = field(default_factory=list, repr=False)
    attrs: dict[str, Any] = field(default_factory=dict)

    # -------------------------------
    # Initialization & registration
    # -------------------------------
    def __post_init__(self):
        # Ensure root has registry
        root = self.root()
        if not hasattr(root, "_registry"):
            root._registry = {}
        # Enforce unique names
        if self.name in root._registry:
            raise ValueError(f"Duplicate node name: {self.name}")
        root._registry[self.name] = self

        # Attach to parent if provided
        if self.parent:
            self.parent.add_child(self)

    # -------------------------------
    # Core relationships
    # -------------------------------
    def add_child(self, child: "Node") -> None:
        """Attach a child to this node, enforcing unique names and safe reparenting."""
        if child is self:
            raise ValueError("A node cannot be its own child.")
        if self.is_descendant_of(child):
            raise ValueError("Cannot create cycle (child is ancestor).")

        # Ensure global name uniqueness via root registry
        root = self.root()
        if not hasattr(root, "_registry"):
            root._registry = {}
        if child.name in root._registry and root._registry[child.name] is not child:
            raise ValueError(f"Duplicate node name: {child.name}")

        # If child already has another parent, detach first
        if child.parent and child.parent is not self:
            child.parent.remove_child(child)

        self.children.append(child)
        child.parent = self
        root._registry[child.name] = child

    def add_parent(self, new_parent: "Node") -> None:
        """Reparent this node under a new parent."""
        new_parent.add_child(self)

    def remove_child(self, child: "Node") -> None:
        """Detach a child."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            root = self.root()
            if hasattr(root, "_registry"):
                root._registry.pop(child.name, None)

    def detach(self) -> None:
        """Detach self from current parent."""
        if self.parent:
            self.parent.remove_child(self)

    # -------------------------------
    # Queries & utilities
    # -------------------------------
    def is_root(self) -> bool:
        return self.parent is None

    def root(self) -> "Node":
        n = self
        while n.parent is not None:
            n = n.parent
        return n

    def path(self, sep: str = "/") -> str:
        parts = []
        n = self
        while n is not None:
            parts.append(n.name)
            n = n.parent
        return sep.join(reversed(parts))

    def depth(self) -> int:
        d, n = 0, self.parent
        while n is not None:
            d += 1
            n = n.parent
        return d

    def is_descendant_of(self, other: "Node") -> bool:
        n = self.parent
        while n is not None:
            if n is other:
                return True
            n = n.parent
        return False

    # -------------------------------
    # Traversal & search
    # -------------------------------
    def iter_dfs(self) -> Iterator["Node"]:
        yield self
        for ch in self.children:
            yield from ch.iter_dfs()

    def iter_bfs(self) -> Iterator["Node"]:
        q = [self]
        while q:
            cur = q.pop(0)
            yield cur
            q.extend(cur.children)

    def find(self, pred: Callable[["Node"], bool]) -> Optional["Node"]:
        for n in self.iter_dfs():
            if pred(n):
                return n
        return None

    def find_by_name(self, name: str) -> Optional["Node"]:
        r = self.root()
        if hasattr(r, "_registry"):
            return r._registry.get(name)
        # fallback slow search
        return self.find(lambda n: n.name == name)

    # -------------------------------
    # Display
    # -------------------------------
    def show(self, attr_list: Iterable[str] | None = None) -> None:
        attr_list = list(attr_list or [])
        for n in self.iter_dfs():
            indent = "  " * n.depth()
            extras = ""
            if attr_list:
                pairs = []
                for a in attr_list:
                    val = n.attrs.get(a, None)
                    pairs.append(f"{a}={val!r}")
                extras = "  [" + ", ".join(pairs) + "]"
            print(f"{indent}- {n.name}{extras}")
    
    def show2(self, attr_list: Iterable[str] | None = None, show_level: bool = True) -> None:
        attr_list = list(attr_list or [])
        for n in self.iter_dfs():
            d = n.depth()
            indent = "  " * d
            pairs = []
            if show_level:
                pairs.append(f"level={d}")
            for a in attr_list:
                pairs.append(f"{a}={n.attrs.get(a, None)!r}")
            extras = f"  [{', '.join(pairs)}]" if pairs else ""
            print(f"{indent}- {n.name}{extras}")

    def __repr__(self) -> str:
        return f"Node({self.name!r})"
