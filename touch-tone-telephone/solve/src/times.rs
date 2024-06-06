pub fn avg_amp(samples: &[f64]) -> f64 {
    let sum = samples
        .iter()
        .fold(0.0, |a, b| a + b.abs());
    sum / samples.len() as f64
}
pub fn find_on_sample_len(samples: &[f64], rate: f64) -> f64 {
    let mut idx = 0;
    let mut search_size = (rate as usize / 100).min(samples.len()); // assumes pulses are longer that 1 100th of a second

    let on_amp = 0.5;
    while search_size as f64 > rate / 500.0 {
        while avg_amp(&samples[idx..idx + search_size]) > on_amp * 0.25 {
            idx += search_size;
            if samples.len() <= idx + search_size {
                return idx as f64;
            }
        }

        if idx >= search_size {
            idx -= search_size;
        }
        search_size /= 2;
    }

    idx += search_size * 2;
    idx as f64
}

pub fn find_off_sample_len(samples: &[f64], rate: f64) -> f64 {
    let mut idx = 0;
    let mut search_size = (rate as usize / 100).min(samples.len()); // assumes off times are longer that 1/100th of a second

    
    let on_amp = 0.5;
    while search_size as f64 > rate / 500.0 {
        while avg_amp(&samples[idx..idx + search_size]) < on_amp * 0.25 {
            idx += search_size;
            if samples.len() <= idx + search_size {
                return idx as f64;
            }
        }

        if idx >= search_size {
            idx -= search_size;
        }
        search_size /= 2;
    }

    idx += search_size * 2;
    idx as f64
}
