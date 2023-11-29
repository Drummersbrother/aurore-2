use std::{
    env, error::Error, fs::File, io::Write, path::Path, process::Command, thread, time::Duration,
};

fn main() {
    // There should be two environmental arguments. The first one should be the path to the mission root,
    // the other should be the log executable path
    let args: Vec<String> = env::args().collect();
    let (mission_root, log_path) = (&args[1], &args[2]);

    let _ = match run_sys_check(mission_root, log_path) {
        Ok(_) => {}
        Err(err) => {
            let message = format!("[Error from detect system failure script] - {err}");
            log(log_path, &message);
        }
    };
}

fn log(log_path: &str, message: &str) {
    Command::new("sh")
        .args([log_path, message])
        .spawn()
        .unwrap();
}

fn run_sys_check(mission_root: &str, log_path: &str) -> Result<(), Box<dyn Error>> {
    log(log_path, "I'm Alive!");

    let path = Path::new(mission_root);

    loop {
        if !path.exists() {
            trigger_kernel_panic()?;
        }
        thread::sleep(Duration::from_millis(500));
    }
}

fn trigger_kernel_panic() -> Result<(), Box<dyn Error>> {
    let mut trigger_file = File::create("/proc/sysrq-trigger")?;
    trigger_file.write_all("c".as_bytes())?;
    Ok(())
}
