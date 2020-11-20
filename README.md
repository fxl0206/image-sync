# image-sync

depend docker registry v2 api and docker command for python simple tool

## quick start on linux

### requirements

* you must install docker or skopeo

### steps

```shell
git clone https://github.com/fxl0206/image-sync
cd image-sync
python syncer.py -s https://source.registry.xxx -t target.registry.xxxx -m sk
```

## quick start docker

### docker steps

you must set /etc/containers/registries.conf [registries.insecure] 

```shell
docker run --rm -it --net host cfxl/image-syncer
python syncer.py -s https://source.registry.xxx -t target.registry.xxxx -m sk
```
