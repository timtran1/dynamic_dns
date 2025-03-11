from pydantic import BaseModel
from typing import Optional


class DomainConfig(BaseModel):
    name: str
    zone_id: str
    proxied: Optional[bool] = False
