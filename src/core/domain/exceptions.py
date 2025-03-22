class DomainError(Exception):
    pass


class FormCanOnlyHaveUniqueFields(DomainError):
    pass
