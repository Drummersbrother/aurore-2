#!/bin/bash -e
cross build --release --target aarch64-unknown-linux-gnu

scp -r ./target/aarch64-unknown-linux-gnu/release/detect-system-failure felixhellborg@aurore2.local:/tmp/

