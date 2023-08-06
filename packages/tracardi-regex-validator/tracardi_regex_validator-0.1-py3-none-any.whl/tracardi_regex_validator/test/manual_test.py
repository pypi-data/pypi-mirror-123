from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi_regex_validator.plugin import ValidatorAction

init = {'validation_regex': r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9](:?)([0-5]?[0-9]?)$',
        'data': "12:32"}
payload = {}
profile = Profile(id="profile-id")
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())
result = run_plugin(ValidatorAction, init, payload,
                    profile)

print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
