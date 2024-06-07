use crate::fourier;

const ROW_0_FREQ: f64 = 697.0;
const ROW_1_FREQ: f64 = 770.0;
const ROW_2_FREQ: f64 = 852.0;
const ROW_3_FREQ: f64 = 941.0;

const COL_0_FREQ: f64 = 1209.0;
const COL_1_FREQ: f64 = 1336.0;
const COL_2_FREQ: f64 = 1477.0;
const COL_3_FREQ: f64 = 1633.0;


pub fn decode_key(samples: &[f64], rate: f64) -> char {
    let r0 = fourier::get_alignment(samples.iter().cloned(), rate, ROW_0_FREQ);
    let r1 = fourier::get_alignment(samples.iter().cloned(), rate, ROW_1_FREQ);
    let r2 = fourier::get_alignment(samples.iter().cloned(), rate, ROW_2_FREQ);
    let r3 = fourier::get_alignment(samples.iter().cloned(), rate, ROW_3_FREQ);

    let c0 = fourier::get_alignment(samples.iter().cloned(), rate, COL_0_FREQ);
    let c1 = fourier::get_alignment(samples.iter().cloned(), rate, COL_1_FREQ);
    let c2 = fourier::get_alignment(samples.iter().cloned(), rate, COL_2_FREQ);
    let c3 = fourier::get_alignment(samples.iter().cloned(), rate, COL_3_FREQ);

    let (idx, _) = (0..16)
        .map(|n| (n / 4, n % 4))
        .map(|(r, c)| [r0, r1, r2, r3][r] + [c0, c1, c2, c3][c])
        .enumerate()
        // .inspect(|a| println!("{a:?}"))
        .max_by(|(_, a), (_, b)| a.total_cmp(b))
        .unwrap();

    let lookup = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D'],
    ];
    lookup[idx / 4][idx % 4]
}


pub fn get_key_by_key(mut samples: &[f64], rate: f64) -> Vec<char> {
    use crate::times::*;

    let mut keys = vec![];
    while !samples.is_empty() {
        let on_count = find_on_sample_len(samples, rate) as usize;
        let off_count = find_off_sample_len(&samples[on_count..], rate) as usize;

        let total_key_len = on_count + off_count;

        let these_samples = &samples[0..on_count];
        samples = &samples[total_key_len..];

        keys.push(decode_key(these_samples, rate));
    }

    keys
}

pub fn keys_to_char(hi: char, lo: char) -> Option<char> {
    fn get_nybble(c: char) -> Option<u8> {
        let row: u8 = match c {
            '1' | '2' | '3' | 'A' => 0,
            '4' | '5' | '6' | 'B' => 1,
            '7' | '8' | '9' | 'C' => 2,
            '*' | '0' | '#' | 'D' => 3,
            _ => return None,
        };
    
        
        let col: u8 = match c {
            '1' | '4' | '7' | '*' => 0,
            '2' | '5' | '8' | '0' => 1,
            '3' | '6' | '9' | '#' => 2,
            'A' | 'B' | 'C' | 'D' => 3,
            _ => return None,
        };
    
        Some(row * 4 + col)
    }

    let val = get_nybble(hi)? * 16 + get_nybble(lo)?;
    Some(val as char)
}

pub fn key_chars_to_string(mut chars: impl Iterator<Item = char>) -> Option<String> {
    let mut curr_str = String::new();

    while let (Some(hi), Some(lo)) = (chars.next(), chars.next()) {
        curr_str.push(keys_to_char(hi, lo)?);
    }

    Some(curr_str)
}
