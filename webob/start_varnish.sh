# Start varnish with a size of 1M, we are after all just caching a 1 12K HTML
# file.
sudo varnishd -F -f ./varnish.vcl -s malloc,1M -T 127.0.0.1:2000 -a 127.0.0.1:10002
