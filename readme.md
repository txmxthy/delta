# Delta Lake Local Demo

This project demonstrates Delta Lake features using Python and Docker.

## Project Structure
```
delta-lake-demo/
├── docker/
│   └── Dockerfile
├── src/
│   ├── main.py
│   └── examples/
│       ├── basic_operations.py
│       ├── streaming.py
│       └── time_travel.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup

1. Install Docker and Docker Compose
2. Create the directory structure shown above
3. Copy all files to their respective locations
4. Create required directories for data:
```bash
mkdir -p data/delta-table data/products data/streaming-source data/streaming-output data/checkpoints
```
5. Build and run:
```bash
docker-compose up -d
```
6. Execute the examples:
```bash
docker exec -it delta-spark-1 python3 -m src.main
```


## Features Demonstrated

* Basic CRUD operations with Delta Lake
* Time travel capabilities (version history and data recovery)
* Streaming operations with Delta Lake
* ACID transactions demonstration

## Examples Explained

* `basic_operations.py`: Shows create, read, update, and merge operations
* `time_travel.py`: Demonstrates version history and accessing previous versions
* `streaming.py`: Shows how to use Delta Lake with streaming data

## Troubleshooting

If you see permission errors, you may need to change the data directory permissions:
```bash
chmod -R 777 data/
```
```

The key changes are:
1. Added complete directory structure
2. Added data directory creation step
3. Corrected the run command to use docker exec
4. Added troubleshooting section
5. Removed schema evolution (as it's not explicitly demonstrated in the examples)
6. Added more specific descriptions of each example
7. Added data directory permissions note