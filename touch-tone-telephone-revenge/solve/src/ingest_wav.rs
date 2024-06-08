use std::{fs::File, path::Path};

use wav::BitDepth;

pub fn wav_to_samples(path: &str) -> (Vec<f64>, f64) {
    let mut reader = File::open(Path::new(path)).unwrap();
    let (header, data) = wav::read(&mut reader).unwrap();

    let data: Vec<_> = match data {
        BitDepth::Empty => panic!("no data :("),
        BitDepth::Eight(data) => data.into_iter().map(|x| x as f64 / u8::MAX as f64 * 2.0 - 1.0).collect(),
        BitDepth::Sixteen(data) => data.into_iter().map(|x| x as f64 / i16::MAX as f64).collect(),
        BitDepth::TwentyFour(data) => data.into_iter().map(|x| x as f64 / i32::MAX as f64).collect(),
        BitDepth::ThirtyTwoFloat(data) => data.into_iter().map(|x| x as f64).collect(),
    };
    (
        data,
        header.sampling_rate as f64,
    )
}