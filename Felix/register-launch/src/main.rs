use rppal::gpio;
use std::{process::ExitCode, thread, time::Duration};

const PINNUMBER: u8 = 21;

fn main() -> ExitCode {
    let gpio = gpio::Gpio::new().unwrap();

    let pin_input = gpio.get(PINNUMBER).unwrap().into_input();

    loop {
        thread::sleep(Duration::from_millis(500));

        if pin_input.is_high() {
            println!("Found high");
            return ExitCode::SUCCESS;
        } else {
            println!("Found low");
        }
    }
}
