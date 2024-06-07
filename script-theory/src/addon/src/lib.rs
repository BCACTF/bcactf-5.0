use rand::prelude::*;
use rand_chacha::ChaCha20Rng;

use chacha20::ChaCha20;
use chacha20::cipher::KeyIvInit;
use chacha20::cipher::StreamCipher;

use napi::JsNumber;
use napi::bindgen_prelude::*;

use napi_derive::napi;

pub const OIL_BASE: [u8; 30] = [
    0x05, 0x14, 0x02, 0x74, 0xdd, 0xe3, 0x1c, 0xe1, 0xa7, 0xab,
    0x05, 0x7e, 0xae, 0x09, 0x1b, 0x18, 0x3a, 0x03, 0xae, 0x9d,
    0x8d, 0xd1, 0x4e, 0x93, 0x7e, 0x68, 0x27, 0xda, 0x79, 0x2a
];

#[napi]
fn bring_oil(value: JsNumber) -> Buffer {
    let mut rng = ChaCha20Rng::seed_from_u64(452890686835);

    let mut oil_key: [u8; 32] = [0; 32];
    oil_key[0..30].copy_from_slice(&OIL_BASE);

    let sub = value.get_int32().unwrap() as u8;

    for i in 0..30 {
        oil_key[i] ^= rng.gen::<u8>();

        if i % 2 == 0 {
            oil_key[i] = sub + 157 - oil_key[i];
        } else {
            oil_key[30] += oil_key[i] % 10;
        }
    }

    oil_key[31] = oil_key[0] + (oil_key[1] % 3);

    return oil_key.to_vec().into();
}

#[napi]
fn diplomat_accurate(oil_key: Buffer, data: Buffer) -> Buffer {
    let n = [0x32; 12];

    let key: Vec<u8> = oil_key.to_vec();

    let mut cipher = ChaCha20::new(key.as_slice().into(), &n.into());

    let mut plaintext = data.to_vec().clone();

    cipher.apply_keystream(&mut plaintext);

    for byte in &mut plaintext {
        *byte = byte.reverse_bits();
    }

    return plaintext.into();
}

#[napi]
fn bucket_terrace(shifter: Buffer, mut data: Buffer, magic: JsNumber) -> Buffer {
    for (i, byte) in shifter.iter().enumerate() {
        data[i] ^= byte ^ (magic.get_uint32().unwrap() as u8);
    }

    return data;
}
