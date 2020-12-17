# ProtonVPN Privoxy Docker

Docker container for setting up a [Privoxy](https://www.privoxy.org/) proxy that pushes traffic over a
[ProtonVPN](https://protonvpn.com/) connection.

Build Docker image:
```
docker build -t walt3rl/proton-privoxy .
```

Run Docker container:

```
docker run -d \
     --device=/dev/net/tun --cap-add=NET_ADMIN \
     -v /etc/localtime:/etc/localtime:ro \
     -p 8888:8080 \
     -e PVPN_USERNAME=my_protonvpn_openvpn_username \
     -e PVPN_PASSWORD=my_protonvpn_openvpn_password \
     --name proton-privoxy walt3rl/proton-privoxy
```

Or with this `docker-compose.yml`:

```yaml
---
version: "3"
services:
  proton-privoxy:
    image: walt3rl/proton-privoxy
    container_name: proton-privoxy
    environment:
      - PVPN_USERNAME=xxxxxxxxxxxxxxxxxxxxxxxx
      - PVPN_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxx
    volumes:
      - /etc/localtime:/etc/localtime:ro
    ports:
      - 8888:8080
    restart: unless-stopped
    devices:
      - /dev/net/tun
    cap_add:
      - NET_ADMIN
```

This will start a Docker container that

1. initializes a `protonvpn` CLI configuration
2. refreshes ProtonVPN server data (connects to https://api.protonvpn.ch)
3. sets up an OpenVPN connection to ProtonVPN with your ProtonVPN account details, and
4. starts a Privoxy server, accessible at http://127.0.0.1:8888, that directs traffic over your VPN connection.

Test:

```
curl --proxy http://127.0.0.1:8888 https://ipinfo.io/ip
```

## Configuration

You can set any of the following container environment variables with
`docker run`'s `-e` options.

### `PVPN_USERNAME` and `PVPN_PASSWORD`

**Required.** This is your ProtonVPN OpenVPN username and password. It's the
username and password you would normally provide to `protonvpn init`.

### `PVPN_TIER`

Your ProtonVPN account tier, called "your ProtonVPN Plan" in `protonvpn init`.
The value must be the number corresponding to your tier from the following
list (from `protonvpn init`):

```
1) Free
2) Basic
3) Plus
4) Visionary
```

Default: `2`

### `PVPN_PROTOCOL`

The protocol that the OpenVPN tunnel will use. Corresponds to the `-p` flag of
the `protonvpn` CLI tool, and the "default OpenVPN protocol" prompt in the
`protonvpn init` process.

Default: `udp`

### `PVPN_CMD_ARGS`

Any arguments you want to pass to `protonvpn`. For example, if you want
`protonvpn` to connect to a random server, set this to `"connect --random"`.
Remember the quotes.

See the [`protonvpn` docs](https://github.com/ProtonVPN/linux-cli/blob/master/USAGE.md#commands) for supported commands and arguments.

Default: `"connect --fastest"` (_Select the fastest ProtonVPN server._)

### `PVPN_DEBUG`

Set to `1` to log debugging details from `protonvpn` to the container's stdout.

Default: _empty_ (debug logging disabled)

### `HOST_NETWORK`

If you want to expose your proxy server to your local network, you need to
specify that network in `HOST_NETWORK`, so that it can be routed back through
your Docker network. E.g. if your LAN uses the 10.0.0.0/8 network, add
`-e HOST_NETWORK=10.0.0.0/8` to your `docker run` command.

Default: _empty_ (no network is routed)


## Pros and cons

### Pro: Multiple VPN connections on the same machine

While not impossible, it is quite the networking feat to route traffic over
specific VPN connections. With this Docker image you can run multiple
containers, each setting up a different VPN connection _which doesn't affect
your host's networking_. Routing traffic over a specific VPN connection is then
as simple as configuring a target application's proxy server.

### Pro: Share a VPN connection between devices on your LAN

Run a container on one machine, and configure multiple devices on your network
to connect to its proxy server. All connections that use that proxy server will
be routed over the same VPN connection.

### Pro: Free privacy filtering, courtesy of [Privoxy](https://www.privoxy.org/)

Why did I choose Privoxy? Mostly because it's the simplest HTTP proxy to
configure, that I've used before.

### Con: ProtonVPN's DNS leak protection doesn't work

Docker prevents containers from changing the servers used for DNS lookups,
after startup. This prevents ProtonVPN from using its own leak protecting DNS
server. In fact, at the moment it causes a non-fatal error in `protonvpn`.

Ensure that you're using privacy respecting DNS servers on your Docker host, or
manually specify secure servers for the container via [`--dns` options](https://docs.docker.com/config/containers/container-networking/#dns-services).
