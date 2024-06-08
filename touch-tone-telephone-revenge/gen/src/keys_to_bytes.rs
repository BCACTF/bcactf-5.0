use crate::sound::keys::Key;

fn get_from_nybble(nybble: u8) -> Key {
    use Key::*;
    const LOOKUP: [Key; 16] = [
        Num1, Num2, Num3, LetA,
        Num4, Num5, Num6, LetB,
        Num7, Num8, Num9, LetC,
        SAst, Num0, SPnd, LetD,
    ];

    LOOKUP[nybble as usize % LOOKUP.len()]
}

pub fn encode_bytes(bytes: impl Iterator<Item = u8>) -> impl Iterator<Item = Key> {
    bytes.flat_map(|byte| [
        get_from_nybble(byte >> 4),
        get_from_nybble(byte & 0xF)
    ])
}

pub fn decode_bytes(mut keys: impl Iterator<Item = Key>) -> impl Iterator<Item = u8> {
    std::iter::repeat(())
        .map_while(move |_| {
            let hi_nybble = keys.next()?;
            let lo_nybble = keys.next()?;
            let byte = (hi_nybble.idx() << 4) + lo_nybble.idx();

            Some(byte)
        })
}
