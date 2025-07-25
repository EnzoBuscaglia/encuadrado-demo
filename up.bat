@echo off
docker-compose up --remove-orphans -d postgres
docker-compose up --remove-orphans -d vitrina_web
