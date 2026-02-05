from pydantic_settings import BaseSettings
from typing import List
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./payroll.db"
    ALLOWANCES: List[str] = ["hra", "ta", "medical"]
    DEDUCTIONS: List[str] = ["tax", "pf", "loan"]

    class Config:
        env_file = ".env"


settings = Settings()
