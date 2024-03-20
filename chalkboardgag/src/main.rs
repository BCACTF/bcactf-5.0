use std::{fs::File, io::Write};

// this is just used for generating the file
// then the flag is manually dispersed throughout the characters of the file
fn main() {
    let mut file = File::create("chalkboardgag.txt");
    for i in 0..=100000 {
        file.as_mut()
            .unwrap()
            .write("I WILL NOT BE SNEAKY\n".as_bytes());
    }
    println!("Hello, world!");
}
