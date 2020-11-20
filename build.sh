IMAGE_URI=cfxl/image-syncer:latest
docker build -t $IMAGE_URI .
docker push $IMAGE_URI
