@echo off
title Iniciando Apache Kafka

echo Iniciando ZooKeeper...
start powershell -NoExit -Command "& 'zookeeper-server-start.bat' '%KAFKA_CONFIG%\zookeeper.properties'"

timeout /t 5 /nobreak >nul

echo Iniciando Kafka...
start powershell -NoExit -Command "& 'kafka-server-start.bat' '%KAFKA_CONFIG%\server.properties'"

echo Servicios iniciados correctamente.
exit
