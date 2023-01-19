# simulverse
<p align="center">
    <em> A metaverse content management framework based on fastapi </em>
</p>

# Prerequisite
 * In order to execute the simulverse, you should setup the following variables in the `instance/config.py` file.
 ```
    MONGODB_URL = "mongodb://id:pw@mongo_db_:27017/"

    # to earn key run:
    # openssl rand -hex 32
    JWT_REFRESH_SECRET_KEY = "COMPLEX_KEY"
    JWT_SECRET_KEY = "COMPLEX_KEY"
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
 ```
 - You should put `instance` directory under the `app/core/`  to execute the simulverse
 - If you want to use management scripts, you should put `instance` directory under the `manage/`

# How to Execute
 - HTTPS support
```python
>$ python simulverse.py https
```
 - HTTP support
 ```python
>$ python simulverse.py http
```

# Project Structure
```
📦app
 ┣ 📂core
 ┃ ┣ 📂instance
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┗ 📜config.py
 ┃ ┣ 📂libs
 ┃ ┃ ┣ 📜oauth2_cookie.py
 ┃ ┃ ┣ 📜pyobjectid.py
 ┃ ┃ ┣ 📜resolve_error.py
 ┃ ┃ ┗ 📜utils.py
 ┃ ┣ 📂models
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜auth_manager.py
 ┃ ┃ ┗ 📜database.py
 ┃ ┣ 📂routers
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜asset.py
 ┃ ┃ ┣ 📜create.py
 ┃ ┃ ┣ 📜login.py
 ┃ ┃ ┣ 📜page_view.py
 ┃ ┃ ┣ 📜register.py
 ┃ ┃ ┗ 📜space.py
 ┃ ┣ 📂schemas
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜space_model.py
 ┃ ┃ ┣ 📜token_model.py
 ┃ ┃ ┗ 📜user_model.py
 ┃ ┣ 📂templates
 ┃ ┃ ┣ 📂aframe
 ┃ ┃ ┃ ┣ 📜scene.html
 ┃ ┃ ┃ ┗ 📜view_scenes.html
 ┃ ┃ ┣ 📂auth
 ┃ ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┃ ┗ 📜register.html
 ┃ ┃ ┣ 📂include
 ┃ ┃ ┃ ┣ 📜alerts.html
 ┃ ┃ ┃ ┣ 📜sidebar.html
 ┃ ┃ ┃ ┣ 📜topnav-sidebar.html
 ┃ ┃ ┃ ┗ 📜topnav.html
 ┃ ┃ ┣ 📂space
 ┃ ┃ ┃ ┣ 📜create_scene.html
 ┃ ┃ ┃ ┣ 📜create_space.html
 ┃ ┃ ┃ ┣ 📜update_scene.html
 ┃ ┃ ┃ ┣ 📜update_space.html
 ┃ ┃ ┃ ┗ 📜view_space.html
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜base.html
 ┃ ┃ ┣ 📜error.html
 ┃ ┃ ┗ 📜page.html
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜settings.py
 ┣ 📂static
 ┃ ┣ 📂css
 ┃ ┃ ┗ 📜custom_style.css
 ┃ ┣ 📂images
 ┃ ┃ ┗ 📜favicon.png
 ┃ ┗ 📂scripts
 ┃ ┃ ┣ 📜contents-save.js
 ┃ ┃ ┣ 📜dynamic_fields.js
 ┃ ┃ ┗ 📜link-controls.js
 ┣ 📜__init__.py
 ┗ 📜main.py
```

## `core/libs`
 - contains utility libraries

## `core/models`
 - drivers for database
 - dirvers for authentication

## `core/routers`
 - Contains routing map

## `core/schemas`
 - Contains database schemas

## `core/templates`
 - Continas jinja2 templates

## `core/static`
 - Contains css, images, and javascripts files.
