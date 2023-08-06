from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from tracardi_regex_validator.model.configuration import Configuration
from tracardi_regex_validator.service.validator import Validator


class ValidatorAction(ActionRunner):
    def __init__(self, **kwargs):
        self.config = Configuration(**kwargs)
        self.validator = Validator(self.config)

    async def run(self, payload):
        if self.validator.check() is not None:
            return Result(port='payload', value=True)
        else:
            return Result(port='payload', value=False)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_regex_validator.plugin',
            className='ValidatorAction',
            inputs=["payload"],
            outputs=["payload"],
            init={
                'validation_regex': None,
                'data': None
            },
            version='0.1.1',
            license="MIT",
            author="Patryk Migaj"

        ),
        metadata=MetaData(
            name='Regex validator',
            desc='Validation of data with custom regex',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["Validations"]
        )
    )
