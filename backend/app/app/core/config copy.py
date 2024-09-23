class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Media"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "72b6dc51f41263d45c111670951419ef171a16abaccb201189144ea9d5ea13a6"
    EXPIRE_MINUTES: int = 60
    DATA_BASE: str = "mysql+pymysql://root:Nitin%401999@localhost:3306/db"

    current_directory: str | None = None
    parent_directory: str | None  = None
    image_dir: str | None  = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_directory = os.getcwd()
        self.parent_directory = os.path.abspath(os.path.join(self.current_directory, '.'))
        self.image_dir = os.path.join(self.parent_directory, "images")
        self.create_image_dir()

    def create_image_dir(self):
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    class Config:
        case_sensitive = True


settings = Settings()
