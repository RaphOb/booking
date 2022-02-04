from datetime import datetime

from pydantic import BaseModel


class Agendas(BaseModel):
    start: datetime
    end: datetime
