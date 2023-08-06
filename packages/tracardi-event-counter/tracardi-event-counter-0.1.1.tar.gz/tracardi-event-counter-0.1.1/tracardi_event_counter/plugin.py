from tracardi.service.storage.driver import storage
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result


from tracardi_event_counter.model.configuration import Configuration


class EventCounter(ActionRunner):

    def __init__(self, **kwargs):
        self.config = Configuration(**kwargs)

    async def run(self, payload) -> Result:
        result = await storage.driver.event.search({
            "bool": {
                "must": [
                    {
                        "range": {
                            "metadata.time.insert": {
                                "gte": "now-{}s".format(self.config.get_time_span()),
                                "lte": "now"}
                        }
                    },
                    {
                        "match": {
                            "type": self.config.event_type
                        }
                    }
                ]
            }
        })
        return Result(port="payload", value=result["hits"]["total"]["value"])


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_event_counter.plugin',
            className='EventCounter',
            inputs=["payload"],
            outputs=['payload'],
            version='0.1.1',
            license="MIT",
            author="Dawid Kruk",
            init={
                "event_type": "",
                "time_span": "-15m"
            }
        ),
        metadata=MetaData(
            name='Event Counter',
            desc='This plugin reads how many events of defined type were triggered within defined time.',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["General"]
        )
    )
