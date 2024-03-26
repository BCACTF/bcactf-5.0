use super::{
    frequency::Frequency,
    meta::{ SampleData, SampleMetadata },
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Key {
    Num1, Num2, Num3, LetA,
    Num4, Num5, Num6, LetB,
    Num7, Num8, Num9, LetC,
    SAst, Num0, SPnd, LetD,
}

impl Key {
    pub fn from_char(c: char) -> Option<Self> {
        match c.to_ascii_lowercase() {
            '1' => Some(Self::Num1),
            '2' => Some(Self::Num2),
            '3' => Some(Self::Num3),
            '4' => Some(Self::Num4),
            '5' => Some(Self::Num5),
            '6' => Some(Self::Num6),
            '7' => Some(Self::Num7),
            '8' => Some(Self::Num8),
            '9' => Some(Self::Num9),
            '0' => Some(Self::Num0),
            'a' => Some(Self::LetA),
            'b' => Some(Self::LetB),
            'c' => Some(Self::LetC),
            'd' => Some(Self::LetD),
            '*' => Some(Self::SAst),
            '#' => Some(Self::SPnd),
            _ => None,
        }
    }

    const ROW_0_FREQ: Frequency = Frequency::new(1.0, 0.0, 697.0);
    const ROW_1_FREQ: Frequency = Frequency::new(1.0, 0.0, 770.0);
    const ROW_2_FREQ: Frequency = Frequency::new(1.0, 0.0, 852.0);
    const ROW_3_FREQ: Frequency = Frequency::new(1.0, 0.0, 941.0);

    const ROWS: [Frequency; 4] = [
        Self::ROW_0_FREQ,
        Self::ROW_1_FREQ,
        Self::ROW_2_FREQ,
        Self::ROW_3_FREQ,
    ];

    const COL_0_FREQ: Frequency = Frequency::new(1.0, 0.0, 1209.0);
    const COL_1_FREQ: Frequency = Frequency::new(1.0, 0.0, 1336.0);
    const COL_2_FREQ: Frequency = Frequency::new(1.0, 0.0, 1477.0);
    const COL_3_FREQ: Frequency = Frequency::new(1.0, 0.0, 1633.0);

    const COLS: [Frequency; 4] = [
        Self::COL_0_FREQ,
        Self::COL_1_FREQ,
        Self::COL_2_FREQ,
        Self::COL_3_FREQ,
    ];

    pub fn row(&self) -> u8 {
        use Key::*;
        match self {
            Num1 | Num2 | Num3 | LetA => 0,
            Num4 | Num5 | Num6 | LetB => 1,
            Num7 | Num8 | Num9 | LetC => 2,
            SAst | Num0 | SPnd | LetD => 3,
        }
    }

    pub fn col(&self) -> u8 {
        use Key::*;
        match self {
            Num1 | Num4 | Num7 | SAst => 0,
            Num2 | Num5 | Num8 | Num0 => 1,
            Num3 | Num6 | Num9 | SPnd => 2,
            LetA | LetB | LetC | LetD => 3,
        }
    }

    pub fn idx(&self) -> u8 {
        self.row() * 4 + self.col()
    }

    pub fn frequencies(&self) -> (Frequency, Frequency) {
        (Self::ROWS[self.row() as usize], Self::COLS[self.col() as usize])
    }

    pub fn get_val(
        &self,
        meta: SampleMetadata,
        amp: f64,
    ) -> SampleData {
        let (row, col) = self.frequencies();
        let row_val = row.get_val(meta);
        let col_val = col.get_val(meta);
        SampleData(amp * (row_val.0 + col_val.0) / 2.0)
    }
}
