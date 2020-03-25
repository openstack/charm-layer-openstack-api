import charms.reactive as reactive

import charms_openstack.charm as charm


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


@reactive.when('cluster.available')
def default_update_peers(cluster):
    """Inform peers about this unit's API addresses.

    Set public-address, internal-address and admin-address on the
    (openstack-ha) peer relation.
    """
    with charm.provide_charm_instance() as instance:
        # This function ONLY updates the peers if the data has changed.  Thus
        # it's okay to call it on every hook invocation.
        instance.update_peers(cluster)
