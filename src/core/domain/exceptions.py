class DomainError(Exception):
    pass


class FormCanOnlyHaveUniqueFields(DomainError):
    pass


class NotFound(DomainError):
    pass


class FormNotFound(NotFound):
    pass


class FormDoesNotHaveAllRequiredFields(DomainError):
    pass


class InvalidFormSubmission(DomainError):
    pass


class FormDoesNotHaveThisField(DomainError):
    pass
