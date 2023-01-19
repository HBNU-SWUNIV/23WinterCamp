import motor.motor_asyncio

from bson.objectid import ObjectId
from fastapi import Request

from ..libs.utils import verify_password
from ..libs.utils import get_password_hash

from ..schemas.user_model import UserRegisterForm, UserInDB
from ..schemas.space_model import CreateSpaceForm, SpaceModel, CreateSceneForm, UpdateSceneForm


class db_manager(object):
    client = None
    db = None

    @classmethod
    def init_manager(cls, _url, _dbname):
        cls.client = motor.motor_asyncio.AsyncIOMotorClient(_url)
        cls.db = cls.client[_dbname]

    @classmethod
    def get_collection(cls, name):
        return cls.db[name]

    @classmethod
    async def get_user_by_email(cls, email: str) -> UserInDB|None:
        document = await cls.get_collection("users").find_one({'email': email})
        if document:
            return UserInDB(**document)
        else:
            return None
    
    @classmethod
    async def get_user_by_id(cls, userid:ObjectId) -> UserInDB|None:
        document = await cls.get_collection("users").find_one({'_id': userid})
        if document:
            return UserInDB(**document)
        else:
            return None

    @classmethod
    async def authenticate_user(cls, userid: str, password: str):
        user = await cls.get_user_by_email(userid)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    @classmethod
    async def create_user(cls, user:UserRegisterForm):
        userdata = await cls.get_user_by_email(user.email)
        if userdata:
            return False
        else:
            data = {'userid':user.username, 'email':user.email, 'spaces':{}, 'hashed_password':get_password_hash(user.password)}
            await db_manager.get_collection('users').insert_one(data) 
            return True

    @classmethod
    async def create_space(cls, creator: str, space:CreateSpaceForm):
        userdata = await cls.get_user_by_email(creator)
        viewers = {str(userdata.id):'Editor'}
        for _id, role in zip(space.form_data['username'], space.form_data['role']):
            view = await cls.get_user_by_email(_id)
            if view :
                if userdata.id != view.id:
                    viewers[str(view.id)] = role

        data = {'name':space.form_data['space_name'][0], 'explain': space.form_data['space_explain'][0], 
                'creator': userdata.id, 'viewers':viewers, 'scenes':{}}
        space_id = await db_manager.get_collection('spaces').insert_one(data) 

        for viewer, val in viewers.items():
            if creator != viewer:
                await db_manager.get_collection('users').update_one({'_id':ObjectId(viewer)}, [{"$set": {'spaces': {str(space_id.inserted_id): val}}}]) 
            else:
                await db_manager.get_collection('users').update_one({'_id':ObjectId(viewer)}, [{"$set": {'spaces': {str(space_id.inserted_id): "Editor"}}}]) 

    @classmethod
    async def update_space(cls, creator: UserInDB, space_id:ObjectId, space:CreateSpaceForm):
        viewers = {str(creator.id):'Editor'}
        
        for _id, role in zip(space.form_data['username'], space.form_data['role']):
            view = await cls.get_user_by_email(_id)
            if view :
                if str(creator.id) != str(view.id):
                    viewers[str(view.id)] = role
        
        for _id, role in viewers.items():
            await db_manager.get_collection('users').update_one({'_id':ObjectId(_id)}, [{"$set": {'spaces': {str(space_id): role}}}])

        found_space = await db_manager.get_collection('spaces').find_one({'_id':space_id})
        for viewer, val in found_space['viewers'].items():
            if viewer not in viewers:
                #print("1",viewer)
                await db_manager.get_collection('users').update_one({'_id':ObjectId(viewer)}, {"$unset": {f'spaces.{str(space_id)}': ""}}) 

        data = {'name':space.form_data['space_name'][0], 'explain': space.form_data['space_explain'][0], 'viewers':viewers}

        await db_manager.get_collection('spaces').update_one({'_id':space_id}, {"$unset": {f'viewers': ""}})
        await db_manager.get_collection('spaces').update_one({'_id':space_id}, [{'$set':data}]) 
    
    @classmethod
    async def create_scene(cls, form:CreateSceneForm, space_id:ObjectId ):
        image_id = await cls.store_image(form.form_data['file'][0].filename, 
                                        form.form_data['file'][0].content_type, 
                                        form.form_data['file'][0].file )
        '''
        link: link_name, scene_id, x, y, z
        '''
        proc_links = list(zip(form.scene, form.x, form.y, form.z, form.yaw, form.pitch, form.roll))

        check_list = []
        for plink in proc_links:
            target_id, _ = plink[0].split(".")
            
            if target_id != "":
                data = {'x':plink[1], 'y':plink[2], 'z':plink[3],'target_id':ObjectId(target_id), 'yaw':plink[4], 'pitch':plink[5], 'roll':plink[6],}
                res = await db_manager.get_collection('links').insert_one(data)
                check_list.append(res.inserted_id)

        data = {'name':form.scene_name, 'image_id':image_id, 'links':check_list}
        scene_id = await db_manager.get_collection('scenes').insert_one(data)
        await db_manager.get_collection('spaces').update_one({'_id':ObjectId(space_id)}, [{"$set": {'scenes': {str(scene_id.inserted_id): form.scene_name}}}]) 

    async def create_link(cls, data:dict):
        link_id = await db_manager.get_collection('links').insert_one(data)
        return link_id

    @classmethod
    async def update_scene(cls, form:UpdateSceneForm, space_id:ObjectId, scene_id:ObjectId ):
        '''
        link: link_name, scene_id, x, y, z
        '''
        # insert new link
        # update prev_link

        prev_scene = await db_manager.get_collection('scenes').find_one(scene_id)
        proc_links = list(zip(form.scene, form.x, form.y, form.z, form.yaw, form.pitch, form.roll))
        #print(proc_links)

        prev_links = prev_scene['links']

        check_list = []
        for plink in proc_links:
            target_id, link_id = plink[0].split(".")

            if link_id != "":
                if ObjectId(link_id) in prev_links:
                    prev_links.remove(ObjectId(link_id))
                data = {'x':plink[1], 'y':plink[2], 'z':plink[3],'target_id':ObjectId(target_id), 'yaw':plink[4], 'pitch':plink[5], 'roll':plink[6],}
                #print(data)
                await db_manager.get_collection('links').update_one({'_id':ObjectId(link_id)}, {'$set':data})
            else:
                if target_id != "":
                    data = {'x':plink[1], 'y':plink[2], 'z':plink[3],'target_id':ObjectId(target_id), 'yaw':plink[4], 'pitch':plink[5], 'roll':plink[6],}
                    res = await db_manager.get_collection('links').insert_one(data)
                    await db_manager.get_collection('scenes').update_one({'_id':ObjectId(scene_id)}, {'$push':{'links':ObjectId(res.inserted_id)}})

        for link in prev_links:
            await db_manager.get_collection('scenes').update_one({'_id':ObjectId(scene_id)}, {'$pull':{'links':ObjectId(link)}})

        data = {'name':form.scene_name, 'links':check_list}
        #scene_id = await db_manager.get_collection('scenes').insert_one(data)

        result = await db_manager.get_collection('spaces').update_one({'_id':space_id}, [{"$set": {'scenes': {str(scene_id): form.scene_name}}}]) 

    @classmethod
    async def get_scene(cls, scene_id:ObjectId ):
        scene = await db_manager.get_collection('scenes').find_one({"_id":scene_id})
        return scene

    @classmethod
    async def get_link(cls, link_id:ObjectId ):
        link = await db_manager.get_collection('links').find_one({"_id":link_id})
        return link
    
    @classmethod
    async def get_scenes(cls, spaceid: ObjectId):
        scenes = []
        cursor = await cls.get_collection("spaces").find_one({"_id":spaceid})
        for sceneid, scene_name in cursor["scenes"].items():
            scenes.append((sceneid, scene_name))
        
        return scenes

    @classmethod
    async def get_spaces(cls, creator: UserInDB):
        spaces = {}
        for spaceid, role in creator.spaces.items():
            cursor = await cls.get_collection("spaces").find_one({"_id":ObjectId(spaceid)})
            spaces[spaceid] = [cursor["name"], cursor['explain'], role]

        return spaces
    
    @classmethod
    async def get_scenes_from_space(cls, spaceid: ObjectId):
        scenes = []
        cursor = await cls.get_collection("spaces").find_one({"_id":spaceid})
        for sceneid, scene_name in cursor["scenes"].items():
            scenes.append((sceneid, scene_name))
        
        return scenes

    @classmethod
    async def get_space(cls, space_id: ObjectId):
        cursor = await cls.get_collection("spaces").find_one({"_id":space_id})
        if cursor:
            return SpaceModel(**cursor)
        else:
            return None

    @classmethod
    async def store_image(cls, filename:str, metadata, contents):
        fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(cls.db, bucket_name="images")
        return await fs.upload_from_stream(filename=filename, source=contents, metadata=metadata)

    @classmethod
    async def download_file(cls, file_id):
        """Returns iterator over AsyncIOMotorGridOut object"""
        fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(cls.db, bucket_name="images")
        gridout = await fs.open_download_stream(file_id)
        content = await gridout.read()

        return (content, gridout.content_type)
        
    @classmethod
    async def delete_scene(cls, space_id:ObjectId, scene_id:ObjectId):
        await db_manager.get_collection('scenes').delete_one({'_id':scene_id})
        d = await db_manager.get_collection('links').delete_many({'target_id':scene_id})
        res = db_manager.get_collection('links').find({})

        await db_manager.get_collection('spaces').update_one({'_id':space_id}, {'$unset':{f"scenes.{str(scene_id)}":""}})