"""Common functions."""

from functoolsplus import coerce

from cmslib.orm.charts import News
from cmslib.presentation.deployment import Presentation


__all__ = ["get_deployment_providers"]


@coerce(frozenset)
def get_deployment_providers(deployment):
    """Yields the providers for the respective deployment."""

    for chart in Presentation(deployment).charts:
        if isinstance(chart, News):
            for provider in chart.providers:
                yield provider.provider
