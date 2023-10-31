ssh felixhellborg@aurore2.local mkdir -p mission

scp -r init.sh felixhellborg@aurore2.local:~/mission/

scp -r scripts felixhellborg@aurore2.local:~/mission/

ssh felixhellborg@aurore2.local 
