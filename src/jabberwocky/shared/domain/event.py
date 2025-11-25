from dataclasses import asdict, dataclass, is_dataclass


@dataclass(frozen=True)
class Event:
    def to_dict(self) -> dict:
        if is_dataclass(self):
            return asdict(self)

        raise NotImplementedError
