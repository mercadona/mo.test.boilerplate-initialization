from jabberwocky.shared.domain.flag_client import Flag, FlagClient


class FakeFlagClient(FlagClient):
    _flags: list[Flag]

    def __init__(self) -> None:
        self._flags = []

    def is_active(self, flag: Flag) -> bool:
        return flag in self._flags

    def active_flag(self, flag: Flag) -> None:
        self._flags.append(flag)
