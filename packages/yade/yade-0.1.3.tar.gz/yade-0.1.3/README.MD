# Yet another Django env (yade)

Simple library to set Django settings through environment variables in a way, inspired by ASP.NET Core.

Examples of variables, which will affect settings:
```
DJANGO__STATIC_URL  # Just string variable
DJANGO__REST_FRAMEWORK__PAGE_SIZE  # Dict value
DJANGO__AUTH_PASSWORD_VALIDATORS__0__NAME  # List value
```
True/False or ints (0,1,2...) values of env variables will be converted to python type (bool or int).
Json like arrays like `[1, 2, 3]`are supported too.

## Installation
`pip install yade`

## Usage
In settings.py:
```
from yade import update_settings_from_env

ALLOWED_HOSTS = ['*']
...  # Your settings here

update_settings_from_env(locals())
# End of file
```
Notice: this work only in modules, not in functions!