from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_language_detection.plugin import LanguageDetectAction

init = payload = {
    'source': {
        'id': '32ccc6e3-0084-4989-8ce2-edd35d888f29'
    },
    "message": """Cześć jak się masz""",
    }

payload = {}
profile = Profile(id="profile-id")
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())
result = run_plugin(LanguageDetectAction, init, payload,
                    profile, event)

print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
