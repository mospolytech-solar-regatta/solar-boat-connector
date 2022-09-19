from typing import Optional

from pydantic import BaseModel


class SerialConfig(BaseModel):
    port: str
    baudrate: Optional[int] = 115200
    bytesize: Optional[int] = 8
    parity: Optional[str] = 'N'
    stopbits: Optional[int] = 1
    timeout: Optional[int] = 0
