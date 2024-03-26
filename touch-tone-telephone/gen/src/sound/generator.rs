use super::{
    keys::Key,
    meta::{AudioMetadata, SampleData, SampleMetadata},
};

pub fn from_keys(
    keys: impl Iterator<Item = Key>,
    key_duration: f64,
    pause_duration: f64,
    amplitude: f64,

    sample_offset: usize, 
    meta: AudioMetadata,
    channel: u16,
) -> impl Iterator<Item = SampleData> {
    let key_samples = (key_duration * meta.sample_rate as f64) as usize;
    let pause_samples = (pause_duration * meta.sample_rate as f64) as usize;

    let time_between_starts = key_samples + pause_samples;

    keys.enumerate().flat_map(move |(i, key)| {
        let initial_offset = i * time_between_starts + sample_offset;

        (0..time_between_starts).map(
            move |i| if i <= key_samples {
                let actual_sample_idx = initial_offset + i;

                key.get_val(
                    SampleMetadata {
                        audio: meta,
                        channel,
                        sample_number: actual_sample_idx,
                    },
                    amplitude,
                )
            } else {
                SampleData(0.0)
            }
        )
    })
}
