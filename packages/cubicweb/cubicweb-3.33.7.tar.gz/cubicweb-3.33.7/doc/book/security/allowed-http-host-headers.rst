.. _allowed-http-host-headers:

Allowed HTTP Host Headers or protection against HTTP Host header attacks
========================================================================

*introduced in CubicWeb 3.33*

Introduction
------------

allowed-http-host-headers is a CubicWeb settings used to configure the
protection against `HTTP Host header attacks
<https://docs.djangoproject.com/en/3.2/topics/security/#host-headers-virtual-hosting>`_.
It is based on Django's mechanism.

The main things you need to remember are:

- you need to add the setting :file:`allowed-http-host-headers` in the :file:`[WEB]` section
  of your config file :file:`all-in-one.conf`. This setting have to be
  a comma separated list of hostname from which your server will be reachable.
  For example:

::

    [WEB]
    allowed-http-host-headers = cubicweb.org,cubicweb.fr

- every request that comes in have to have a header :file:`Host:`
  or :file:`X-Forwarded-Host` with a value contained in this comma separated
  list of headers. Otherwise, the request will be rejected with a 403 error.
- if you don't configure this settings and launch your webserver without
  debug mode it will refuse to start
- if you don't configure this settings and launch the server in debug mode,
  :file:`allowed-http-host-headers` will be set as :file:`localhost,.locahost,127.0.0.1`
  (:file:`.` at the beginning of a domain means "wildcard")

Other things are:

- :file:`.` like in :file:`.localhost` means "wildcard" which means "every
  subdomain of this domain are accepted" like :file:`data.localhost` AND the domain itself
- :file:`*` means "accept all domains". You really should avoid this unless you
  have a very good reason too.

Web server configuration
------------------------

If you are using a webserver like apache or nginx in a mod_proxy fashion you
**need** to configure it to forward the host to your proxified application.

In nginx you need to have this line in your :file:`location` section:

::

    proxy_set_header Host $host;

Other information
-----------------

Extract from `Django's documentation <https://docs.djangoproject.com/en/3.2/topics/security/#host-headers-virtual-hosting>`_:


   Previous versions of this document recommended configuring your web server to
   ensure it validates incoming HTTP Host headers. While this is still
   recommended, in many common web servers a configuration that seems to validate
   the Host header may not in fact do so. For instance, even if Apache is
   configured such that your Django site is served from a non-default virtual host
   with the ServerName set, it is still possible for an HTTP request to match this
   virtual host and supply a fake Host header. Thus, Django now requires that you
   set ALLOWED_HOSTS explicitly rather than relying on web server configuration.

External reference
------------------

If you want to have more information on the Host header you can either read w3c
documentation or MDN:

- https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.23
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Host
