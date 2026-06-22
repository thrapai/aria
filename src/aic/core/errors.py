class AICError(Exception):
    pass


class WorkflowParseError(AICError):
    pass


class WorkflowValidationError(AICError):
    pass


class TemplateRenderError(AICError):
    pass


class ExtensionNotFoundError(AICError):
    pass


class ExtensionExecutionError(AICError):
    pass


class InputResolutionError(AICError):
    pass
