# Manual Despliegue Open Data Cube (ODC) 1.8.2 - Contenedores

A continuación se presentan los pasos requeridos para el despliegue del cubo de datos.

### Instalación de Requerimientos (CentOS 8)

Instalación de Git

```sh 
sudo dnf install -y git
```

Instalación de Docker

```sh 
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf install docker-ce --nobest -y
systemctl start docker
systemctl enable docker
sudo usermod -aG docker $USER
```

Reinicie el sistema

```sh 
sudo reboot now
```

Verifique que Docker funcione correctamente

```sh 
docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Instalar Docker Compose

```sh 
sudo dnf install curl -y
sudo curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verificar instalación de Docker Compose 

```sh 
docker-compose -version 

docker-compose version 1.25.0, build 0a186604
```

### Configuración Esquema de Directorios

Use los siguientes comandos para crear el esquema de directorios para el ODC.

```sh 
sudo mkdir /datasets_storage /ingested_storage /analysis_storage /database_storage
```

Asignar los directorios al gropu `bac (GID=1024)`.

```sh 
sudo chmod -R 777 /datasets_storage /ingested_storage /analysis_storage /database_storage
```

### Despliegue de Contenedores

Clone el siguiente repositorio.

```sh 
git clone https://github.com/DonAurelio/open-datacube-bac.git
```

Ingrese al directorio `open-datacube-bac`

```sh 
cd open-datacube-bac
```

Inicie los servicios (contenedores)

```sh
docker-compose up -d 
```

Verifique el estado de los servicios, observe que `State` debe ser `Up` para cada contenedor

```sh
docker-compose ps

            Name                          Command               State                      Ports                    
--------------------------------------------------------------------------------------------------------------------
open-datacube-bac_database_1   docker-entrypoint.sh postgres    Up      5432/tcp                                    
open-datacube-bac_datacube_1   entrypoint.sh bash -c cd / ...   Up      0.0.0.0:2222->22/tcp, 0.0.0.0:8081->8081/tcp
open-datacube-bac_explorer_1   entrypoint.sh gunicorn -b  ...   Up      0.0.0.0:2220->22/tcp, 0.0.0.0:8080->8080/tcp
open-datacube-bac_ingestor_1   entrypoint.sh tail -F /hom ...   Up      0.0.0.0:2221->22/tcp  
```

### Configuración Componente datacube


Ingrese al contenedor **datacube**

```sh
docker-compose exec datacube bash
```

Crear un nuevo grupo

```sh 
sudo groupadd --gid 1024 bac
```

Añadir el usuario actual al gropu `bac`

```sh 
sudo usermod -aG bac datacube
```

Use el comando mostrado a continuación para inicializar la base de datos del cubo de datos. Este paso se hace una única vez para la creación del esquema de datos que usa el ODC para indexar imágenes de satelite. 

```sh 
datacube@487239d46d68:~$ datacube system init

Initialising database...
Created.
Checking indexes/views.
Done.
```

Si al usar el comando `datacube system init` obtiene el error mostrado abajo, entonces realice la configuración mostrada a continuación.

```sh 
  File "/usr/local/lib/python3.6/dist-packages/sqlalchemy/engine/strategies.py", line 114, in connect
    return dialect.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.6/dist-packages/sqlalchemy/engine/default.py", line 493, in connect
    return self.dbapi.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.6/dist-packages/psycopg2/__init__.py", line 127, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server: No route to host
	Is the server running on host "database" (172.19.0.2) and accepting
	TCP/IP connections on port 5432?
```

Edite el archivo `/etc/firewalld/firewalld.conf`  y cambie la linea `FirewallBackend=nftables` por `FirewallBackend=iptables`.

```sh 
sudo nano /etc/firewalld/firewalld.conf

# FirewallBackend
# Selects the firewall backend implementation.
# Choices are:
#       - nftables (default)
#       - iptables (iptables, ip6tables, ebtables and ipset)
#FirewallBackend=nftables
FirewallBackend=iptables
```

Reinicie el Firewall y vuelva a aplicar el comando `datacube system init`

```sh 
sudo systemctl restart firewalld.service
```

Verfifique que el cubo de datos ha sido correctamente configurado usando el siguiente comando.

```sh 
datacube@487239d46d68:~$ datacube system check

Version:       1.8.2
Config files:  
Host:          database:5432
Database:      datacube
User:          datacube
Environment:   None
Index Driver:  default

Valid connection:	YES
```

Ejecute el siguiente comando pasa salir del contenedor **datacube**

```sh 
datacube@487239d46d68:~$ exit
```

Ingrese a la siguiente URL **http://[ip-cube-server]:8081/** para acceder a la interfaz de Jupyter Noternotebooks e inicar el desarrollo de algoirtmos.


### Configuración Componente Explorer

Ingrese al contenedor **explorer**

```sh
docker-compose exec explorer bash
```

Clone el siguiente repositorio.

```sh 
git clone https://github.com/DonAurelio/open-datacube-bac.git
```

Copiar la carpeta `open-datacube-bac/explorer` en la ubicación actual 

```sh
cp -r open-datacube-bac/explorer .
```

**NOTA:** Para habilitar la visualización de unidades de almacenamiento debe tener datos indexados o ingestados en el cubo de datos. Esta visualización debe ser generada de manera periódica con el objetivo de actualizar esta visualización con el contenido que se agrega de forma incremental. A continuación se muestran los pasos para crear una tarea de actualziación de vistas periódica.

Cree un **cronjob** para automatizar el proceso de generación de vistas del Open Data Cube.

```sh
crontab -e
```

Coloque **solo una** de las siguientes lineas al final del archivo para programar la tarea periódica de actualización de las visualizaciones del Open Data Cube.

* Cada Minuto: `*/1 * * * * /bin/bash /home/datacube/explorer/cubedash.sh`
* Cada Hora: `0 * * * * /bin/bash /home/datacube/explorer/cubedash.sh`
* Cada Día a la 1 AM: `0 1 * * * /bin/bash /home/datacube/explorer/cubedash.sh` 

```sh 
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
0 1 * * * /bin/bash /home/datacube/explorer/cubedash.sh
```

Inicie el servicio `cron` usando el siguiente comando. Cada que el contenedor sea reiniciado, debe volver a ejecutar el comando. 

```sh 
sudo cron 
```

Presione la tecla Cntrl+O y luego Enter para guardar. Finalmente presiones Cntrl+X para salir. Ingrese a la siguiente URL **http://[ip-cube-server]:8080/** para acceder a la interfaz de visualización del contenido del Open Dat Cube.

## Referencias 

1. [DNS Not Resolving under Network [CentOS8]](https://github.com/docker/for-linux/issues/957)
2. [Docker volumes and file system permissions](https://medium.com/@nielssj/docker-volumes-and-file-system-permissions-772c1aee23ca)
