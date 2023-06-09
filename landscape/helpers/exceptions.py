class OptimizationExceptions(Exception):
    pass

class QuitGameException(OptimizationExceptions):
    pass


class RetryLevelException(OptimizationExceptions):
    pass


class NextLevelException(OptimizationExceptions):
    pass

class TargetFunctionCalledOnPointOutOfDomainError(OptimizationExceptions):
    pass