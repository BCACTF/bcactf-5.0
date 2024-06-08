use solve::{
    decode_flag,
    ingest_wav,
    keys::{ get_key_by_key, key_chars_to_string },
};


fn main() {
    let (orig_samples, rate) = ingest_wav::wav_to_samples("beep_boop.wav");
    let keys = get_key_by_key(&orig_samples, rate);
    println!("{:?}", keys);
    let message = key_chars_to_string(keys.into_iter()).unwrap();
    println!("bcactf{{{}}}", decode_flag::decode_flag(&message).unwrap());
}
