from typing import Type, TypeVar
from pydantic import BaseSettings
from fakts.fakts import Facts, get_current_fakts


Class = TypeVar("Class")

class Config(BaseSettings):

    class Config:
        extra = "ignore"
        group = "undefined"


    @classmethod
    def from_fakts(cls: Type[Class], konfik: Facts = None, **overwrites) -> Class:
        group = cls.__config__.group
        assert group is not "undefined", f"Please overwrite the Metaclass Config parameter group and point at your group {cls}"
        konfik = konfik or get_current_fakts()
        return cls(**konfik.load_group(group))