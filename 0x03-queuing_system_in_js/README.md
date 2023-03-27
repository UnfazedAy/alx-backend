# 0x03. Queuing System in JS
This directory contains the solution for the task below based on Queuing system in JS

# Tasks
## 0. Install a redis instance
Download, extract, and compile the latest stable Redis version (higher than 5.0.7 - https://redis.io/download/):

    $ wget http://download.redis.io/releases/redis-6.0.10.tar.gz
    $ tar xzf redis-6.0.10.tar.gz
    $ cd redis-6.0.10
    $ make

- Start Redis in the background with src/redis-server

        $ src/redis-server &

- Make sure that the server is working with a ping src/redis-cli ping

        PONG

- Using the Redis client again, set the value School for the key Holberton

        127.0.0.1:[Port]> set Holberton School
        OK
        127.0.0.1:[Port]> get Holberton
        "School"

- Kill the server with the process id of the redis-server (hint: use ps and grep)

        $ kill [PID_OF_Redis_Server]

- Copy the dump.rdb from the redis-5.0.7 directory into the root of the Queuing project.

Requirements:
- Running get Holberton in the client, should return School

**Repo:**
- GitHub repository: alx-backend
- Directory: 0x03-queuing_system_in_js
- File: README.md, dump.rdb