use super::meta::{ SampleData, SampleMetadata };


#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Frequency {
    pub amplitude: f64,
    pub phase: f64,
    pub frequency: f64,
}

impl Frequency {
    pub const fn new(amplitude: f64, phase: f64, frequency: f64) -> Self {
        Self {
            amplitude,
            phase,
            frequency,
        }
    }

    pub const fn builder() -> FrequencyBuilder<Unset, Unset, Unset> {
        FrequencyBuilder::new()
    }

    pub fn get_val(&self, meta: SampleMetadata) -> SampleData {
        let seconds_offset = meta.sample_number as f64 / meta.audio.sample_rate as f64;
        let cycles = seconds_offset * self.frequency;
        let radians = cycles * (2.0 * std::f64::consts::PI) + self.phase;

        SampleData(self.amplitude * radians.sin())
    }
}


#[derive(Debug, Clone, Copy)]
pub struct Set;
#[derive(Debug, Clone, Copy)]
pub struct Unset;



#[derive(Debug, Clone, Copy, PartialEq)]
pub struct FrequencyBuilder<Amp: Copy, Pha: Copy, Frq: Copy> {
    amplitude: f64,
    phase: f64,
    frequency: Option<f64>,
    phantoms: std::marker::PhantomData<(Amp, Pha, Frq)>,
}

impl FrequencyBuilder<Unset, Unset, Unset> {
    pub const fn new() -> Self {
        Self {
            amplitude: 1.0,
            phase: 0.0,
            frequency: None,
            phantoms: std::marker::PhantomData,
        }
    }
}
impl Default for FrequencyBuilder<Unset, Unset, Unset> {
    fn default() -> Self {
        Self::new()
    }
}

impl<Pha: Copy, Frq: Copy> FrequencyBuilder<Unset, Pha, Frq> {
    pub const fn with_amplitude(self, amplitude: f64) -> FrequencyBuilder<Set, Pha, Frq> {
        FrequencyBuilder {
            amplitude,
            phase: self.phase,
            frequency: self.frequency,
            phantoms: std::marker::PhantomData,
        }
    }
}
impl<Amp: Copy, Frq: Copy> FrequencyBuilder<Amp, Unset, Frq> {
    pub const fn with_phase(self, phase: f64) -> FrequencyBuilder<Amp, Set, Frq> {
        FrequencyBuilder {
            amplitude: self.amplitude,
            phase,
            frequency: self.frequency,
            phantoms: std::marker::PhantomData,
        }
    }
}

impl<Amp: Copy, Pha: Copy> FrequencyBuilder<Amp, Pha, Unset> {
    pub const fn with_frequency(self, frequency: f64) -> FrequencyBuilder<Amp, Pha, Set> {
        FrequencyBuilder {
            amplitude: self.amplitude,
            phase: self.phase,
            frequency: Some(frequency),
            phantoms: std::marker::PhantomData,
        }
    }
}

impl<Amp: Copy, Pha: Copy> FrequencyBuilder<Amp, Pha, Set> {
    pub const fn build(self) -> Frequency {
        Frequency {
            amplitude: self.amplitude,
            phase: self.phase,
            frequency: match self.frequency {
                Some(f) => f,
                None => panic!("FrequencyBuilder::build called without frequency set!"),
            },
        }
    }
}

