ssh felixhellborg@aurore2.local mkdir -p mission

scp -r init.sh felixhellborg@aurore2.local:~/mission/

scp -r scripts felixhellborg@aurore2.local:~/mission/

(cd detect-system-failure || exit 1;
  cross build --release --target aarch64-unknown-linux-gnu
  scp -r ./target/aarch64-unknown-linux-gnu/release/detect-system-failure felixhellborg@aurore2.local:~/mission/scripts/detect_system_failure  
)

scp -r media felixhellborg@aurore2.local:~/mission/

scp reboot-watchdog-init/* felixhellborg@aurore2.local:~/

ssh felixhellborg@aurore2.local 
