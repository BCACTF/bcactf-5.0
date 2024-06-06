use std::io::{Seek, Write};

use super::{
    keys::Key,
    meta::BitType,
};

pub trait SampleType where Self: Sized {
    fn get_from_float(f: f64) -> Self;
    fn bit_type() -> BitType;
    
    fn bits() -> u16;
    fn wrap(val: &[Self]) -> wav::BitDepth;
    fn audio_format() -> u16;
}

impl SampleType for i8 {
    fn get_from_float(f: f64) -> i8 {
        let max = i8::MAX as f64;
        let float_val = f * max;
        float_val as i8
    }
    fn bits() -> u16 { i8::BITS as u16 }
    fn bit_type() -> BitType { BitType::I08 }
    fn wrap(val: &[i8]) -> wav::BitDepth {
        wav::BitDepth::Eight(
            val.iter()
            .copied()
            // Convert -128, -127, ..., 127 to 0, 1, ..., 255
            .map(|v| v.wrapping_add(i8::MIN) as u8)
            .collect()
        )
    }
    fn audio_format() -> u16 { wav::WAV_FORMAT_PCM }
}

impl SampleType for i16 {
    fn get_from_float(f: f64) -> i16 {
        let max = i16::MAX as f64;
        let float_val = f * max;
        float_val as i16
    }
    fn bits() -> u16 { i16::BITS as u16 }
    fn bit_type() -> BitType { BitType::I16 }
    fn wrap(val: &[i16]) -> wav::BitDepth {
        wav::BitDepth::Sixteen(val.to_vec())
    }
    fn audio_format() -> u16 { wav::WAV_FORMAT_PCM }
}

impl SampleType for f32 {
    fn get_from_float(f: f64) -> f32 { f as f32 }
    fn bits() -> u16 { 32 }
    fn bit_type() -> BitType { BitType::F32 }
    fn wrap(val: &[f32]) -> wav::BitDepth {
        wav::BitDepth::ThirtyTwoFloat(val.to_vec())
    }
    fn audio_format() -> u16 { wav::WAV_FORMAT_PCM }
}

#[derive(Debug, Clone, Copy)]
pub struct Params {
    pub sample_rate: u32,

    pub on_duration: f64,
    pub off_duration: f64,
}

impl Params {
    pub fn generate_from_keys<T: SampleType>(
        &self,
        keys: impl Iterator<Item = Key>,
        output: &mut (impl Write + Seek),
    ) -> std::io::Result<()> {
        use wav::Header;
        use super::meta::AudioMetadata;
        use super::generator::from_keys;

        let header = Header::new(
            T::audio_format(),
            1,
            self.sample_rate,
            T::bits(),
        );
        let audio = AudioMetadata {
            sample_rate: self.sample_rate,
            channels: 1,
            bit_type: T::bit_type(),
        };

        let samples: Vec<_> = from_keys(
            keys,
            self.on_duration,
            self.off_duration,
            1.0,
            0,
            audio,
            0,
        )
            .map(|k| T::get_from_float(k.0))
            .collect();

        wav::write(
            header,
            &T::wrap(&samples),
            output,
        )
    }
}