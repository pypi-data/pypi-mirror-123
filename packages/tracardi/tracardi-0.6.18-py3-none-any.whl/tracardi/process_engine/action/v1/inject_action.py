from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result


class InjectAction(ActionRunner):

    def __init__(self, value):
        self.value = value

    async def run(self, payload):
        return Result(value=self.value, port="payload")


def register() -> Plugin:
    return Plugin(
        start=True,
        debug=True,
        spec=Spec(
            module='tracardi.process_engine.action.v1.inject_action',
            className='InjectAction',
            inputs=[],
            outputs=["payload"],
            init={"value": {}},
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="value",
                            name="Object to inject",
                            description="Provide object as JSON to be injected into payload and returned "
                                        "on output port.",
                            component=FormComponent(type="json", props={"label": "object"})
                        )
                    ]
                ),
            ]),
            manual='inject_action',
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski"
        ),
        metadata=MetaData(
            name='Inject',
            desc='Injector.',
            keywords=['start node'],
            type='flowNode',
            width=100,
            height=100,
            icon='json',
            group=["Input/Output"]
        )
    )
