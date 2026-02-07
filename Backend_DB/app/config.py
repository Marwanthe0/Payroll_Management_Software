from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./payroll.db"

    # Allowances (added to salary)
    ALLOWANCES: dict = {
        "hra": 0.20,  # House Rent Allowance - 20% of basic salary
        "ta": 0.10,  # Travel Allowance - 10% of basic salary
        "medical": 2000.0,  # Medical Allowance - fixed amount
    }

    # Deductions (subtracted from salary)
    DEDUCTIONS: dict = {
        "tax": 0.05,  # VAT/TAX - 5% of basic salary
        "pf": 0.03,  # Provident Fund - 3% of basic salary
    }

    # Display names for allowances and deductions
    ALLOWANCE_NAMES: dict = {
        "hra": "House Rent Allowance",
        "ta": "Travel Allowance",
        "medical": "Medical Allowance",
    }

    DEDUCTION_NAMES: dict = {
        "tax": "VAT/TAX",
        "pf": "Provident Fund",
    }

    class Config:
        env_file = ".env"


settings = Settings()
