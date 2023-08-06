from ..node import Node
from .program_track_action import ProgramTrackAction, programTrackActionFragment
from .application import Application, applicationFragment
from .program_track_event import ProgramTrackEvent, programTrackEventFragment
from .user import User, userFragment

applicationRequestFragment = (
    """
fragment ApplicationRequest on ApplicationRequest {
    id
    createdAt
    application {
        ...Application
    }
    programTrackAction {
        ...ProgramTrackAction
    }
    user {
        ...User
    }
    programTrackEvent {
        ...ProgramTrackEvent
    }
}
"""
    + applicationFragment
    + programTrackActionFragment
    + userFragment
    + programTrackEventFragment
)


class ApplicationRequest(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)

    @property
    def application(self):
        return Application(self._data["application"], self._context)

    @property
    def action(self):
        return ProgramTrackAction(self._data["programTrackAction"], self._context)
    
    @property
    def user(self):
        if not self._data["user"]:
            return None

        return User(self._data["user"], self._context)

    @property
    def event(self):
        if not self._data["programTrackEvent"]:
            return None

        return ProgramTrackEvent(self._data["programTrackEvent"], self._context)
