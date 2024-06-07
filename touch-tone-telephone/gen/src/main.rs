use std::fs::File;

use gen::{
    keys_to_bytes::encode_bytes,
    seeding::get_seeded_message,
    sound::keys_to_wav::Params,
};

fn main() {
    let params = Params {
        sample_rate: 8000,
        on_duration: 0.05,
        off_duration: 0.025,
    };

    let message = get_seeded_message();
    let keys = encode_bytes(message.bytes());
    params.generate_from_keys::<i8>(
        keys,
        &mut File::create("output.wav").unwrap(),
    ).unwrap();
}
