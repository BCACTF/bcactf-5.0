use std::path::Path;
use std::fs::read_to_string as read_file;

use std::env::var as env_var;

use crate::message_generator::generate_message;
use crate::rand::PcgRng;

pub fn flag_prefix() -> &'static str {
    "bcactf{"
}

pub fn flag_suffix() -> &'static str {
    "}"
}

pub fn get_flag() -> String {
    let full_flag = if let Ok(flag) = env_var("TEAM_FLAG") {
        flag
    } else if let Ok(flag) = read_file(Path::new("flag.txt")) {
        flag
    } else {
        panic!("No flag found");
    };

    let Some(prefixless) = full_flag.strip_prefix(flag_prefix()) else {
        panic!("Invalid flag format (missing prefix {:?})", flag_prefix());
    };

    let Some(suffixless) = prefixless.strip_suffix(flag_suffix()) else {
        panic!("Invalid flag format (missing suffix {:?})", flag_suffix());
    };

    suffixless.to_string()
}

pub fn get_seed() -> u64 {
    if let Ok(seed) = env_var("TEAM_SEED") {
        seed.parse().expect("Invalid env seed")
    } else {
        let flag = get_flag();

        flag
            .chars()
            .map(|c| c as u64)
            .fold(
                PcgRng::seeded(0xDEADBEEF), // Chose a random base seed
                |rng, char| rng.further_seeded(char),
            )
            .into_seed()
    }
}


const MAX_ITERS: u64 = 100_000;

pub fn get_seeded_message() -> String {
    let seed = get_seed();
    let flag = get_flag();

    // Not all seeds work, so we need to try until we find one that does
    for i in 0..MAX_ITERS {
        if let Some(message) = generate_message(seed + i, &flag) {
            return message;
        }
    }

    panic!("Failed to find adequate seed for message generation in {MAX_ITERS} iterations");
}
