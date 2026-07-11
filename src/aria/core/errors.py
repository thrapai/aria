class ARIAError(Exception):
    pass


class WorkflowParseError(ARIAError):
    pass


class WorkflowValidationError(ARIAError):
    pass


class TemplateRenderError(ARIAError):
    pass


class ExtensionNotFoundError(ARIAError):
    pass


class ExtensionExecutionError(ARIAError):
    pass


class InputResolutionError(ARIAError):
    pass
