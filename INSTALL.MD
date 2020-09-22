# Manual Despliegue Open Data Cube (ODC) 1.8.2 - Contenedores

Clone el siguiente repositorio
Clone this repository and get into the **open-datacube-workshop/version_1.8.2** foder.

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

### Definición de Productos

Para indexar/ingestar escenas de un determinado satelite se debe crear un producto en el cubo de datos. Un producto debe ser creado por cada satelite. A continuación se muestran los pasos para la creación del Producto `ls8_collections_sr_scene`.

Ingrese al contenedor **datacube**

```sh
docker-compose exec datacube bash
```

Liste los archivos de la carpeta `products`

```sh
datacube@b5d6c817587a:~$ ls -l products/

total 20
drwxr-xr-x 2 datacube datacube 4096 Jul 20 23:21 LS5_TM_LEDAPS
drwxr-xr-x 2 datacube datacube 4096 Jul 21 00:23 LS7_ETM_LEDAPS
drwxr-xr-x 2 datacube datacube 4096 Jul 20 15:37 LS8_OLI_LASRC
-rw-rw-r-- 1 datacube datacube 1143 Jul 21 03:57 README.MD
drwxr-xr-x 2 datacube datacube 4096 Jul 21 00:23 S1_SAR_GAMMA0
```

En la carpeta `products` va a encontrar los archivos necesarios para definir un producto, indexar un escena que corresponda al producto creado, y ingestar (opcional). Use el comando que se muestra a continaución para listar los productos creados en el cubo de datos. 


```sh
datacube@b5d6c817587a:~$ datacube product list

```

Dado que tiene una instalación nueva del cubo, aún no tiene productos definidos, por tal motivo el comando anterior mostró un listado vacío. A continuación use comando mostrado abajo para crear el producto `ls8_collections_sr_scene`.

```sh
datacube@b5d6c817587a:~$ datacube product add products/LS8_OLI_LASRC/description_file.yml

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

### Indexa de Escenas


