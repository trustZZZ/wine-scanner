from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Общие поля, которые есть везде
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    LOG_LVL: str = "INFO"

    # Поля БД (без значений по умолчанию, чтобы нельзя было забыть их настроить)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # URL приложения (для генерации ссылок, например, в письмах)
    URL: str

    model_config = ConfigDict(extra='allow')


class DevSettings(Settings):
    """Настройки для локальной разработки"""
    # Здесь мы можем задать удобные дефолты, чтобы не писать их в .env каждый раз
    ENV: str = "dev"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "password"  # ⚠️ В реальном проекте лучше выносить даже это в .env!
    DB_NAME: str = "my_app_dev"
    URL: str = "http://localhost:8000"
    LOG_LVL: str = "DEBUG"  # В разработке хотим видеть максимум логов


class ProdSettings(Settings):
    """Настройки для продакшена"""
    ENV: str = "prod"
    # Никаких дефолтов! Если переменная не передана, приложение упадет при старте.
    # Это защита от того, что ты случайно запустишь прод с настройками от локалки.

    # Можно добавить специфические настройки для прода
    LOG_LVL: str = "WARNING"  # На проде логируем только ошибки и предупреждения


def get_settings() -> Settings:
    """Фабрика для выбора настроек"""
    # Читаем переменную APP_ENV. Если её нет, считаем, что это разработка.
    env = BaseSettings(ENV="dev").model_validate({})
    # Но лучше читать явно из env:
    import os
    current_env = os.getenv("APP_ENV", "dev")

    if current_env == "prod":
        return ProdSettings()
    else:
        return DevSettings()


# Инициализируем настройки через фабрику
settings = get_settings()

# Для проверки можно вывести текущую среду
print(f"🚀 Запуск в режиме: {settings.ENV}")