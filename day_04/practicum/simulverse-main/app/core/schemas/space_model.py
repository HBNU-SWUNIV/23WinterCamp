from fastapi import Request
from pydantic import BaseModel, Field
from bson import ObjectId

class SpaceModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str = ""
    explain: str = ""
    creator: ObjectId = Field(default_factory=ObjectId)
    viewers: dict | None = None
    scenes: dict | None = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    pass
    
class CreateSpaceForm: 
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.form_data = {}

    async def load_data(self):
        form = await self.request.form()
        contents = form.multi_items()
        
        for k, v in contents:
            if k not in self.form_data:
                self.form_data.setdefault(k, []).append(v)
            else:
                self.form_data[k].append(v)

    async def is_valid(self):
        if not self.form_data['space_name'][0]:
            self.errors.append("Space name is required")
        if not self.form_data['space_explain'][0]:
            self.errors.append("Space explanation is required")
        if not self.errors:
            return True
        return False
class CreateSceneForm: 
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.form_data = {}

    async def load_data(self):
        form = await self.request.form()
        contents = form.multi_items()
        
        for k, v in contents:
            if k not in self.form_data:
                self.form_data.setdefault(k, []).append(v)
            else:
                self.form_data[k].append(v)

        for key, val in self.form_data.items():
            if len(val) > 1:
                setattr(self, key, val)
            else:
                setattr(self, key, val[0])

        self.scene = self.scene[1:]
        self.x = self.x[1:]
        self.y = self.y[1:]
        self.z = self.z[1:]

    async def is_valid(self):
        if not self.scene_name:
            self.errors.append("Name is required")
        if not self.file:
            self.errors.append("Image File is required")
        if not self.errors:
            return True
        return False

class UpdateSceneForm: 
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.form_data = {}

    async def load_data(self):
        form = await self.request.form()
        contents = form.multi_items()
        
        for k, v in contents:
            if k not in self.form_data:
                self.form_data.setdefault(k, []).append(v)
            else:
                self.form_data[k].append(v)

        for key, val in self.form_data.items():
            if len(val) > 1:
                setattr(self, key, val)
            else:
                setattr(self, key, val[0])

        self.scene = self.scene[1:]
        self.x = self.x[1:]
        self.y = self.y[1:]
        self.z = self.z[1:]

    async def is_valid(self):
        if not self.scene_name:
            self.errors.append("Name is required")
        if not self.errors:
            return True
        return False