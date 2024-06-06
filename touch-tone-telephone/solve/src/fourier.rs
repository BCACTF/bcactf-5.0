
pub fn get_alignment(samples: impl Iterator<Item = f64>, rate: f64, freq: f64) -> f64 {
    let mut real = 0.0;
    let mut imag = 0.0;

    let rad_per_sample = std::f64::consts::TAU * freq / rate;

    for (i, sample) in samples.enumerate() {
        let phase = rad_per_sample * i as f64;
        real += sample * phase.cos();
        imag += sample * phase.sin();
    }

    (real * real + imag * imag).sqrt()
}
