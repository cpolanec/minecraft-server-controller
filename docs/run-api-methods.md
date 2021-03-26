# Run API methods

See below for descriptions and examples of the available API methods in this application. The following substitutions are required in these examples:

- `MY_API_KEY` should bu substituted for the API key defined in the API gateway usage plan and aligns with the `API_KEY` in the `.env` file.
- `MY_DOMAIN.NET` should be substituted for the `API_DOMAIN_NAME` value defined in the `.env` file.

## Method: GET /servers

```shell
> # return all Minecraft game servers in your server farm
> curl -s -H 'x-api-key:MY_API_KEY' -X GET 'https://MY_DOMAIN.NET/servers' | jq .
{
  "servers": [
    {
      "name": "myworld",
      "fullName": "minecraft-main-server-myworld",
      "environment": "main",
      "instanceId": "i-0123abcd4567efghi",
      "state": "running",
      "publicIpAddress": "10.32.54.76"
    },
    {
      "name": "otherworld",
      "fullName": "minecraft-main-server-otherworld",
      "environment": "main",
      "instanceId": "i-abcd1234efgh56789",
      "state": "stopped",
      "publicIpAddress": "10.32.54.78"
    }
}
```

## Method: GET /servers/myworld

```shell
> # return info about a Minecraft game server in your farm by name
> curl -s -H 'x-api-key:MY_API_KEY' -X GET 'https://MY_DOMAIN.NET/servers/myworld' | jq .
{
  "name": "myworld",
  "fullName": "minecraft-main-server-myworld",
  "environment": "main",
  "instanceId": "i-0123abcd4567efghi",
  "state": "running",
  "publicIpAddress": "10.32.54.76"
}
```

## Method: POST /servers/myworld

```shell
> # change state of a Minecraft game server to "stopped"
> curl -s -H 'x-api-key:MY_API_KEY' -X POST -d '{"state": "stopped"}' 'https://MY_DOMAIN.NET/servers/myworld' | jq .
{
  "name": "myworld",
  "fullName": "minecraft-main-server-myworld",
  "environment": "main",
  "instanceId": "i-0123abcd4567efghi",
  "state": "stopped",
  "publicIpAddress": "10.32.54.76"
}
> # change state of a Minecraft game server to "running"
> curl -s -H 'x-api-key:MY_API_KEY' -X POST -d '{"state": "running"}' 'https://MY_DOMAIN.NET/servers/myworld' | jq .
{
  "name": "myworld",
  "fullName": "minecraft-main-server-myworld",
  "environment": "main",
  "instanceId": "i-0123abcd4567efghi",
  "state": "running",
  "publicIpAddress": "10.32.54.76"
}
```

## Method: GET /servers/myworld/users

```shell
> # return users on a Minecraft game server in your farm by name
> curl -s -X GET -H 'x-api-key:MY_API_KEY' 'https://MY_DOMAIN.NET/servers/myworld/users' | jq .
{
  "count": 2,
  "names": [
    "user1",
    "anotheruser"
  ]
}
```
