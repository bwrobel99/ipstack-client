from abc import ABC, abstractmethod
from dataclasses import dataclass

from databases import Database


@dataclass(frozen=True)
class BaseRepository(ABC):
    db: Database
