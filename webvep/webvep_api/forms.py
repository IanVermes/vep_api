from dataclasses import dataclass

"""Forms are data objects like Django models but without data persisting the data to a DB"""


@dataclass
class VcfForm:
    """Representation of a VcfFile"""

    filename: str
    content: bytes
