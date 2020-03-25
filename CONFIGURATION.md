## Configuration
By default(and not customizable for now), grc-rpc-manager looks for a file called rpc.ini in the current working directory. File structure is similar to the Microsoft Windows INI file structure. It contains 3 sections.
### Server
* port -> int: The port that will be used by the server
### Wallet
* username -> str: The username for RPC (rpcuser)
* password -> str: The password for RPC (rpcpassword)
* url -> str: The URL for RPC (http://{ip}:{rpcport})
### User:<username>
* password -> str: The hashed password
* password_hash -> str: The algorithm used to hash the password. Must be defined by python's hashlib
* allowed_commands -> str: Semi-colon(;) separated list of allowed methods
