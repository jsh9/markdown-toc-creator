class HeaderLevelNotContinuousError(Exception):
    """Exception when header levels are not continuous"""


class HeaderLevelOutOfBoundError(Exception):
    """Exception when current header level is higher than the initial level"""
