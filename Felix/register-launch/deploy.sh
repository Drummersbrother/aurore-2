#!/bin/bash -e
cross build --release --target aarch64-unknown-linux-gnu

scp -r ./target/aarch64-unknown-linux-gnu/release/register-launch felixhellborg@aurore2.local:/tmp/

#ssh felixhellborg@aurore2.local /tmp/register-launch
