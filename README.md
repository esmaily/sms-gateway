# Python Async Sms Gateway

> This project a good example implements python async service gateway.

### Licensing

The project operates under the MIT license, which not only facilitates its use in commercial and open-source projects
but also encourages further development and sharing within the community.

### Setting Up the Project With Docker

Before diving into the details, let's go through the steps required to set up the project:

##### Supporting Gateway now:

- `kavenegar`
- `ghasedak`

#### 1. Create project environment:

Isolation is key to maintaining a clean and organized development environment. By creating a virtual environment, you
ensure that the project's dependencies don't interfere with your system-wide packages.

```sh
$ cp .env.example .env
$ vim .env
```

#### 2. Create Docker machine or  connect your network machine:

```sh
$ docker-machine create --driver virtualbox smsmanager 
$ eval $(docker-machine env smsmanager) 
```
#### 2. Init docker swarm :

```sh
$  docker swarm init --advertise-addr YOUR_MACHINE_IP

```

#### 3. Run local register (if you don't have global registry):
After create machine should be create or connect to your registry.
can you read more information [Docker Register](https://hub.docker.com/_/registry)

```sh
$  docker run -d -p 5000:5000 --restart always --name registry registry:2

```
#### 4. Build & Push service image:

```sh
$  docker compose -f docker-swarm.yml build
$  docker compose -f docker-swarm.yml push

```
 

#### 5. Deploy application with Swarm :

```sh
$  docker stack deploy -c docker-swarm.yml smsgateway
```

#### 6. Create or Seed gateways Data :
> Before run this command set your gateways data in `main.py` file and run this command
```sh
$ curl -X POST YOUR_MACHINE_IP/seed-data
```

#### 7. Run Test :

```sh
$ docker compose exec app pytest
```

#### Test with postman

> You can install postman and import postman file.

### Project link

1. [Project root path](http://YOUR_MACHINE_IP:8008/)
2. [Swagger ui](http://YOUR_MACHINE_IP/docs/)
3. [Manage database](http://YOUR_MACHINE_IP:5050/browser/)
4. [Service visualizer](http://YOUR_MACHINE_IP:8080/)


### install weave network manager
```sh

docker plugin install --grant-all-permissions weaveworks/net-plugin
```
 