from dataclasses import dataclass

"""Forms are data objects like Django models but without data persisting the data to a DB"""


@dataclass
class VcfForm:
    """Representation of a VcfFile"""

    filename: str
    content: bytes


@dataclass
class VepForm:
    """Representation of the VepFile i.e. variant effect output of the VEP script"""

    raw_data: bytes
    error: str

    def is_valid(self):
        return bool(self.raw_data)
