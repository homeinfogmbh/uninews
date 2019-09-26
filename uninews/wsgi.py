"""Administrative interface to enable news providers for customers."""

from flask import request

from his import CUSTOMER, authenticated, authorized, root, Application
from mdb import Customer
from newslib.dom import news
from newslib.enumerations import Provider
from newslib.filters import articles
from newslib.messages import NO_CUSTOMER_SPECIFIED
from newslib.messages import NO_SUCH_CUSTOMER
from newslib.messages import CUSTOMER_PROVIDER_ADDED
from newslib.messages import NO_SUCH_CUSTOMER_PROVIDER
from newslib.messages import CUSTOMER_PROVIDER_DELETED
from newslib.orm import CustomerProvider
from previewlib import preview, DeploymentPreviewToken, FileAccessToken
from wsgilib import JSON, XML

from uninews.functions import get_deployment_providers


__all__ = ['APPLICATION']


APPLICATION = Application('news')


@authenticated
@root
def list_providers():
    """Lists customer providers."""

    return JSON([provider.value for provider in Provider])


@authenticated
@authorized('news')
def list_customer_providers():
    """Lists customer providers."""

    return JSON([
        customer_provider.to_json() for customer_provider
        in CustomerProvider.select().where(
            CustomerProvider.customer == CUSTOMER.id)])


@authenticated
@root
def add_customer_provider():
    """Adds a new customer provider."""

    try:
        customer = Customer[request.json.pop('customer')]
    except (KeyError, TypeError):
        raise NO_CUSTOMER_SPECIFIED
    except Customer.DoesNotExist:
        raise NO_SUCH_CUSTOMER

    customer_provider = CustomerProvider.from_json(
        request.json, customer=customer, unique=True)
    customer_provider.save()
    return CUSTOMER_PROVIDER_ADDED.update(id=customer_provider.id)


@authenticated
@root
def delete_customer_provider(ident):
    """Removes the respective customer provider."""

    try:
        customer_provider = CustomerProvider[ident]
    except CustomerProvider.DoesNotExist:
        raise NO_SUCH_CUSTOMER_PROVIDER

    customer_provider.delete_instance()
    return CUSTOMER_PROVIDER_DELETED


@preview(DeploymentPreviewToken)
def preview_deployment(deployment):
    """Returns the news preview for the respective deployment."""

    wanted_providers = get_deployment_providers(deployment)
    xml = news()
    sha256sums = set()

    for article in articles(deployment.customer, wanted_providers):
        article_dom = article.to_dom()
        xml.article.append(article_dom)

        if article_dom.image:
            sha256sums.add(article_dom.image.sha256sum)

    headers = FileAccessToken.headers_for_sha256sums(sha256sums)
    return XML(xml, headers=headers)


APPLICATION.add_routes((
    ('GET', '/providers', list_providers),
    ('GET', '/customer-providers', list_customer_providers),
    ('POST', '/customer-providers', add_customer_provider),
    ('DELETE', '/customer-providers/<int:ident>', delete_customer_provider),
    ('GET', '/preview', preview_deployment)
))
