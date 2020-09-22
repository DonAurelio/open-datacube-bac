# Manual Despliegue Open Data Cube (ODC) 1.8.2 - Contenedores

A continuación se presentan los pasos requeridos para el despliegue del cubo de datos.

### Instalación de Requerimientos (CentOS 8)

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
sudo mkdir mnt/datasets_storage mnt/ingested_storage mnt/analysis_storage mnt/database_storage
sudo chown $USER:root mnt/datasets_storage mnt/ingested_storage mnt/analysis_storage mnt/database_storage
```

Clone el siguiente repositorio.

```sh 
git clone https://github.com/DonAurelio/open-datacube-bac.git
```

Copie los archivos de definición y configuración de la carpeta `datasets_storage`.

```sh 
cp -r open-datacube-bac/datasets_storage/* /mnt/datasets_storage
```

### Despliegue de Contenedores

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

Use el comando mostrado a continuación para inicializar la base de datos del cubo de datos. Este paso se hace una única vez para la creación del esquema de datos que usa el ODC para indexar imágenes de satelite. 

```sh 
datacube@487239d46d68:~$ datacube system init

Initialising database...
Created.
Checking indexes/views.
Done.
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

### Configuración Componente Explorer

Ingrese al contenedor **explorer**

```sh
docker-compose exec explorer bash
```

Para habilitar la visualización de unidades de almacenamiento debe tener datos indexados o ingestado en el cubo de datos. Cuando tenga datos que cumplan con el requerimiento anterior, puede ejecutar el comando siguiente para generar la visualización del contendo disponible en el cubo de datos. Esta visualización debe ser generada de manera periódica con el objetivo de actualizar esta visualización con el contenido que se agrega de forma incremental al cubo de datos. El usuraio es libre de usar mecanismos como **crontab** para programar esta tarea. Las visualizaciones se generan empleando el siguiente comando.


```sh
cubedash-gen --init --all
```


### Configuración Componente Ingestor

Para indexar/ingestar escenas de un determinado satelite se debe crear un producto en el cubo de datos. Un producto debe ser creado por cada satelite. A continuación se muestran los pasos para la creación del Producto `ls8_collections_sr_scene`.

Ingrese al contenedor **ingestor**

```sh
docker-compose exec ingestor bash
```

Liste los archivos de la carpeta `products`

```sh
datacube@b5d6c817587a:~$ ls -l /datasets_storage

drwxr-xr-x 2 datacube datacube 4096 Jul 20 15:37 LS8_OLI_LASRC
```

En la carpeta `/datasets_storage/LS8_OLI_LASRC` va a encontrar los archivos necesarios para definir un producto, indexar un escena que corresponda al producto creado, y ingestar (opcional). Use el comando que se muestra a continaución para listar los productos creados en el cubo de datos. 


```sh
datacube@b5d6c817587a:~$ datacube product list

```

Dado que tiene una instalación nueva del cubo, aún no tiene productos definidos, por tal motivo el comando anterior mostró un listado vacío. A continuación use comando mostrado abajo para crear el producto `ls8_collections_sr_scene`.

```sh
datacube@b5d6c817587a:~$ datacube product add /datasets_storage/LS8_OLI_LASRC/description_file.yml

Adding "ls8_collections_sr_scene" (this might take a while) DONE
```

Liste de nuevo los produtos definidos en el cubo de datos. Debería obtener un listado con los productos definidos hasta el momento en el cubo de datos.


```sh
datacube@b5d6c817587a:~$ datacube product list 

ls8_collections_sr_scene  Landsat 8 USGS Collection 1 Higher Level SR scene proessed using LaSRC. 30m UTM based projection.
```

Ejecute el siguiente comando pasa salir del contenedor **datacube**

```sh 
datacube@487239d46d68:~$ exit
```

