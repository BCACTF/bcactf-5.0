use crate::rand::PcgRng;

const BEGINNING: &str = r##"
Hello. Welcome to the BCACTF Helpline.
This call may be recorded for quality assurance purposes.
"##;
const AFTER_INDICIES: &str = r##"
Please hold while we send you random garbage that you should index into to get the flag.
When you're finished, make sure to wrap the flag in the proper format.
"##;

const RANDOM_ALPHABET: &str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";

pub fn generate_message(seed: u64, flag: &str) -> Option<String> {
    use std::fmt::Write;

    let stripped_flag = flag.trim_start_matches("bcactf{").trim_end_matches('}');
    let random = psuedo_random_chars(seed, RANDOM_ALPHABET, 128);

    let mut message = BEGINNING.trim().to_string();
    let mut rng = PcgRng::seeded(seed);

    message.push('\n');
    message.push('\n');

    for (char_idx, target_char) in stripped_flag.chars().enumerate() {
        let matching_indicies: Vec<_> = random
            .chars()
            .enumerate()
            .filter_map(|(idx, rand_char)| (rand_char == target_char).then_some(idx))
            .collect();

        if matching_indicies.is_empty() {
            return None;
        }
        
        let random_idx = rng.advance() as usize % matching_indicies.len();

        writeln!(
            &mut message,
            "For char {:2}, get index 0x{:02x}.",
            char_idx,
            matching_indicies[random_idx],
        ).ok()?;
    }

    message.push('\n');
    message.push('\n');

    message.push_str(AFTER_INDICIES.trim());
    message.push('\n');

    message.push_str(&random);

    Some(message)
}

fn psuedo_random_chars(seed: u64, chars: &str, len: usize) -> String {
    let mut rng = PcgRng::seeded(seed);
    let mut message = String::new();

    for _ in 0..len {
        let idx = rng.advance() as usize % chars.len();
        let random_char = chars.as_bytes()[idx] as char;
        message.push(random_char);
    }

    message
}
