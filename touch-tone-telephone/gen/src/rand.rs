#[derive(Debug, Clone)]
pub struct PcgRng {
    state: u64,
}

impl PcgRng {
    pub fn seeded(seed: u64) -> Self {
        let mut rng = Self {
            state: seed,
        };
        rng.advance();
        rng
    }

    pub fn further_seeded(self, seed: u64) -> Self {
        let mut rng = self;
        rng.advance();
        rng.state ^= seed;
        rng.advance();
        rng
    }

    const MULTIPLIER: u64 = 6364136223846793005;
    const INCREMENT: u64  = 1442695040888963407;

    pub fn advance(&mut self) -> u32 {
        let old_state = self.state;
        let rot = (old_state >> 59) as u16;

        let new_state = old_state.wrapping_mul(Self::MULTIPLIER).wrapping_add(Self::INCREMENT);
        let pre_scramble = (new_state ^ (new_state >> 18)) as u32;

        let low_scrambled = pre_scramble >> rot;
        let high_scrambled = pre_scramble << (31 & (!rot).wrapping_add(1));
        
        self.state = new_state;
        low_scrambled | high_scrambled
    }

    pub fn into_seed(self) -> u64 {
        self.state
    }
}
