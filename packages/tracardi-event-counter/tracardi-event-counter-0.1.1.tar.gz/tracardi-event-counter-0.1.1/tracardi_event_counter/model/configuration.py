from pydantic import BaseModel
from pytimeparse import parse


class Configuration(BaseModel):
    event_type: str
    time_span: str

    def get_time_span(self) -> int:
        result = parse(self.time_span.strip("-"))
        if result is None:
            raise ValueError("Could not parse {} as time span".format(self.time_span))
        return int(result)
