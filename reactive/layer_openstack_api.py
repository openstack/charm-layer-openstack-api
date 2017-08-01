# attempt to move the default status handler here:
import charmhelpers.core.hookenv as hookenv

import charms_openstack.charm as charm
import charms.reactive as reactive


@reactive.when('amqp.connected',
               'charms.openstack.do-default-amqp.connected')
def default_amqp_connection(amqp):
    """Handle the default amqp connection.

    This requires that the charm implements get_amqp_credentials() to
    provide a tuple of the (user, vhost) for the amqp server
    """
    with charm.provide_charm_instance() as instance:
        user, vhost = instance.get_amqp_credentials()
        amqp.request_access(username=user, vhost=vhost)
        instance.assess_status()


@reactive.when('shared-db.connected',
               'charms.openstack.do-default-shared-db.connected')
def default_setup_database(database):
    """Handle the default database connection setup

    This requires that the charm implements get_database_setup() to provide
    a list of dictionaries;
    [{'database': ..., 'username': ..., 'hostname': ..., 'prefix': ...}]

    The prefix can be missing: it defaults to None.
    """
    with charm.provide_charm_instance() as instance:
        for db in instance.get_database_setup():
            database.configure(**db)
        instance.assess_status()


@reactive.when('identity-service.connected',
               'charms.openstack.do-default-identity-service.connected')
def default_setup_endpoint_connection(keystone):
    """When the keystone interface connects, register this unit into the
    catalog.  This is the default handler, and calls on the charm class to
    provide the endpoint information.  If multiple endpoints are needed,
    then a custom endpoint handler will be needed.
    """
    with charm.provide_charm_instance() as instance:
        keystone.register_endpoints(instance.service_type,
                                    instance.region,
                                    instance.public_url,
                                    instance.internal_url,
                                    instance.admin_url)
        instance.assess_status()


@reactive.when('identity-service.available',
               'charms.openstack.do-default-identity-service.available')
def default_setup_endpoint_available(keystone):
    """When the identity-service interface is available, this default
    handler switches on the SSL support.
    """
    with charm.provide_charm_instance() as instance:
        instance.configure_ssl(keystone)
        instance.assess_status()
