from rest_framework.exceptions import PermissionDenied, ValidationError


class BaseExecuteService:
    def __init__(self) -> None:
        self.errors: dict = {}
        self.warnings: list[str] = []

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def raise_validation_error(self, msg: str | dict) -> None:
        raise ValidationError(msg)

    def raise_permission_error(self, msg: str | dict) -> None:
        raise PermissionDenied(msg)

    def add_validation_error(self, msg: str | dict[str, str]) -> None:
        if isinstance(msg, dict):
            for k, v in msg.items():
                self.errors.setdefault(k, []).append(v)
        else:
            self.errors.setdefault("__all__", []).append(msg)

    def is_valid(self, raise_exception: bool = False) -> bool:
        if raise_exception and self.errors:
            raise ValidationError(self.errors)
        return not bool(self.errors)
