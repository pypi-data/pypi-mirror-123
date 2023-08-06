from pydantic import BaseModel
from pytimeparse import parse


class Configuration(BaseModel):
    event_type: str
    time_span: str

    def get_time_span(self) -> int:
        return int(parse(self.time_span.strip("-")))
