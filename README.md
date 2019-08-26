# Overview

This layer provides the base layer for OpenStack charms that are will deploy
API services, and provides all of the core functionality for:

 - HA (using the hacluster charm)
 - Juju 2.0 network space support for API endpoints
 - Configuration based network binding of API endpoints

To use this layer, including the following in the layer.yaml of your charm:

    include: ['layer:openstack-api']

And then read the [new API charm](https://github.com/openstack/charm-guide/blob/master/doc/source/new-charm.rst)
guide for details on how to use this layer in-conjuction with the
charms.openstack Python module to quickly and easily put together a
new API charm.
