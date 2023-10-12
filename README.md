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

#### 2. Build project  :

```sh
$ docker compose build
```

#### 3. Run project:

```sh
$ docker compose up -d

```

#### 4. Create or Seed gateways Data :
> Before run this command set your gateways data in `main.py` file and run this command
```sh
$ curl -X POST 127.0.0.1:8008/seed-data
```

#### 2. Run Test :

```sh
$ docker compose exec app pytest
```

#### Test with postman

> You can install postman and import postman file.

### Project link

1. [Project root path](http://127.0.0.1:8008/)
2. [Swagger ui](http://127.0.0.1:8008/docs/)
3. [Manage database](http://127.0.0.1:5050/browser/)



 