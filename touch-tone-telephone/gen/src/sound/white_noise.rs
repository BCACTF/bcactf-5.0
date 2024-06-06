use crate::rand::PcgRng;
use super::meta::{SampleData, SampleMetadata};

pub fn get_white_noise_sample(
    sample: SampleMetadata,
    amplitude: f64,
) -> SampleData {
    let mut rng = PcgRng::seeded(sample.audio.sample_rate as u64)
        .further_seeded(sample.sample_number as u64)
        .further_seeded(sample.channel as u64);

    let sample = rng.advance() as f64 / u32::MAX as f64;

    SampleData((sample * 2.0 - 1.0) * amplitude)
}

