import asyncio

from aiohttp import ClientConnectorError
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_dot_notation.dot_template import DotTemplate
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_language_detection.model.configuration import Key, Configuration
from tracardi.service.storage.driver import storage
from tracardi_language_detection.service.http_client import HttpClient
from tracardi_plugin_sdk.domain.result import Result


def validate(config: dict):
    return Configuration(**config)


class LanguageDetectAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'LanguageDetectAction':

        # This reads config
        config = validate(kwargs)

        # This reads resource
        source = await storage.driver.resource.load(config.source.id)

        return LanguageDetectAction(config, Key(**source.config))

    def __init__(self, config:Configuration, key: Key):
        self.message = config.message
        self.client = HttpClient(key.token, config.timeout)

    async def run(self, payload):
        dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)
        template = DotTemplate()
        string = template.render(self.message, dot)
        try:
            status, result = await self.client.send(string)

            if status in [200, 201, 202, 203, 204]:

                return Result(port="response", value=result), Result(port="error", value=None)
            else:
                return Result(port="response", value=None), Result(port="error", value=result)

        except ClientConnectorError as e:
            return Result(port="response", value=None), Result(port="error", value=str(e))

        except asyncio.exceptions.TimeoutError:
            return Result(port="response", value=None), Result(port="error", value="Timeout.")


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_language_detection.plugin',
            className='LanguageDetectAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1.4',
            license="MIT",
            author="Patryk Migaj",
            init={
                'source': {
                    'id': None
                },
                "message": "Hello world",
                "timeout": 15
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="source",
                            name="Token resource",
                            description="Select resource that have API token.",
                            component=FormComponent(type="resource", props={"label": "resource"})
                        )
                    ]
                ),
                FormGroup(
                    fields=[
                        FormField(
                            id="message",
                            name="Text",
                            description="Type text or path to text to be detected.",
                            component=FormComponent(type="textarea", props={"label": "template"})
                        )
                    ]
                )
            ]
            )
        ),
        metadata=MetaData(
            name='Language detection',
            desc='This plugin detect language from given string with meaningcloud API',
            type='flowNode',
            width=200,
            height=100,
            icon='language',
            group=["Language"]
        )
    )
