from snowflake import SnowflakeGenerator


def generate_snow_flake_id() -> int:
    generator = SnowflakeGenerator(instance=42)
    return next(generator)
