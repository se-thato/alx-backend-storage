# 0x02. Redis Basic

## Description

This project focuses on implementing a simple Redis-based caching system using Python and the `redis` library. The main objective is to create a `Cache` class that interacts with Redis to store arbitrary data types (`str`, `bytes`, `int`, `float`) using randomly generated keys.

## Files

- `exercise.py`: Contains the implementation of the `Cache` class.
- `main.py`: Sample script to test the functionality of the `Cache` class.

## Learning Objectives

- Understand the basics of Redis as an in-memory data store.
- Learn how to interact with Redis using Python (`redis-py` client).
- Practice using `uuid` for generating unique keys.
- Handle various data types with Redis.
- Flush and reset Redis databases for clean testing environments.

## Requirements

- Python 3.x
- Redis server running locally
- `redis` Python package (`pip install redis`)

## Example Usage

```bash
$ python3 main.py
3a3e8231-b2f6-450d-8b0e-0f38f16e8ca2
b'hello'
