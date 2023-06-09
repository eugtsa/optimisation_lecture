from pydantic import BaseModel

class Origin(BaseModel):
    x: float 
    y: float

class DisplaySettings(BaseModel):
    sizex: int
    sizey: int
    pixels_in_one_x_scale: int
    origin: Origin