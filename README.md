# Ayomi Interview Task

## Setup Guide

This guide explains how to set up and run the project using Docker.

---

### 1. Install Docker

#### For macOS & Windows

Download and install Docker Desktop from the official Docker website:  
👉 https://www.docker.com/products/docker-desktop

#### For Linux (Debian/Ubuntu-based)

Run the following commands to install Docker and Docker Compose:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
```

#### Verify Docker Installation

Check that Docker and Docker Compose are installed correctly:

```bash
docker --version
docker compose version
```

---

### 2. Clone the Project

Clone the repository to your local machine:

```bash
git clone https://github.com/janukasama/ayomi-interview-task.git
```

---

### 3. Navigate to Project Root

Make sure you're in the root directory of the project before proceeding:

```bash
cd <repository-directory>
```

---

### 3. Create secrets and set environment variables

Set the following environment variables with your desired values:

```bash
mkdir devops/secrets
echo "desired_value" > devops/secrets/calculation_db_username.txt
echo "desired_value" > devops/secrets/calculation_db_password.txt
export AYOMI_ENV="prod"
```

---

### 5. Start the Application

Start the application using Docker Compose:

```bash
docker compose -f devops/compose-files/docker-compose.base.yml up -d
```

This will:

- Start the required services (e.g., api server, database).

---

### 6. Access the API

Once the containers are running, access the API documentation using Swagger UI:

👉 http://0.0.0.0:8000/docs

---

## Troubleshooting

- Make sure Docker is running in the background.
- Ensure no other service is using port `8000`.
- View logs using:

```bash
docker compose logs
```

---
