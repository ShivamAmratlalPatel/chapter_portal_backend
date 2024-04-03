ssh-keygen -t rsa -N "" -m pem -b 4096 -C "test-keys" -f ./test.key
openssl rsa -in ./test.key -pubout > ./test.key.pem