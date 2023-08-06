from dataclasses import dataclass, field
from typing import Optional
import traceback

from igi_gc_reader.sample_data import IGIUserFriendlyException
from igi_gc_reader.utils import gc_logger

IGI_SUPPORT_EMAIL = 'support@igiltd.com'
FAO = 'Chris Prosser'


@dataclass
class Status:
    success: bool
    only_unsupported_sheets: bool = field(default=False)
    igi_exception: Optional[Exception] = field(default_factory=lambda: None)

    @property
    def failure_message(self) -> str:
        if self.success:
            return ""
        # note: in a future version of the webservice it would be good to just ask them if
        #       we can use the file uploaded to consider adding support...
        please_submit_msg = (f"Please consider submitting the file to IGI to request for "
                             f"support to be added ({IGI_SUPPORT_EMAIL} - FAO: {FAO}).")
                             
        if self.igi_exception is not None:
            if isinstance(self.igi_exception, IGIUserFriendlyException):
                return (f"Column alignment error. Error details: {self.igi_exception}")
            else:
                gc_logger.error(f"Got exception, but not a subclass of IGIUserFriendlyException, "
                      f"so not including in web response:")
                traceback.print_exception(type(self.igi_exception), self.igi_exception,
                                          self.igi_exception.__traceback__)
        if self.only_unsupported_sheets:
            return  (f"The structure of this file is not currently supported. "
                     f"{please_submit_msg}")
        return f"Unexpected error - {please_submit_msg}"


SuccessStatus = Status(success=True)


@dataclass
class TransformationResult:
    status: Status
    output_filepath: str = field(default="")

    @property
    def message(self) -> str:
        if self.status.success:
            return "Success"
        return self.status.failure_message
