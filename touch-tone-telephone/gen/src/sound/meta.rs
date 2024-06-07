#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AudioMetadata {
    pub sample_rate: u32,
    pub channels: u16,
    pub bit_type: BitType,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SampleMetadata {
    pub audio: AudioMetadata,
    pub channel: u16,
    pub sample_number: usize,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SampleData(pub f64);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BitType {
    I08,
    I16,
    I24,
    I32,
    I64,
    F16,
    F32,
    F64,
}