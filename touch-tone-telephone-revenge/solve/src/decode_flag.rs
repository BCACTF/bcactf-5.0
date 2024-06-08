pub fn decode_flag(message: &str) -> Option<String> {
    let last_line = message.trim().split('\n').last()?;

    let indicies = message
        .split("get index 0x")
        .skip(1)
        .filter_map(|part| part.split_once('.').map(|(s, _)| s))
        .filter_map(|idx| usize::from_str_radix(idx, 16).ok())
        .map(|idx: usize| last_line.as_bytes()[idx])
        .fold(String::new(), |mut s, c| { s.push(c as char); s });

    Some(indicies)
}
