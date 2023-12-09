
from pydantic_settings import BaseSettings

# note : how to handle all of those variables without let any one look at theme on githup,
#        can using the Environment variables, where can create a BaseSettings class and assign
#        all of those variables into this class and assign this class instance as a machine
#        variable into the path url .


# later in a real project instead of using this Config class, you should use a real environemnt 
# variables of the used machine TODO [ maybe the one you deployde this back-end on it] ? 

# now we can access those varaibles throughout the .env file variables values, with Config class...
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'



settings = Settings() 
 