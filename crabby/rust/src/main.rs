#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let shared_secret : &str = "null";
    let _private : &str = &gpwd();
    let url : &str = "http://localhost";
    let port : &str = "7787";
    let resp = reqwest::Client::new()
        .post(url.to_owned()+":"+port+"/flag")
        .header("Authorization", shared_secret)
        .send()
        .await?
        .text();
    println!("{:?}", resp.await?);
    Ok(())
}

fn gpwd() -> String {
    let vals = "99 50 57 116 90 86 57 122 100 88 66 108 99 108 57 122 90 87 78 121 90 88 82 102 97 50 86 53 88 51 82 108 101 72 82 102 97 71 86 121 90 81 61 61"
        .split(" ")
        .map(|x| x.parse::<u8>().unwrap());
    let mut res = String::new();
    for val in vals {
        res.push(val as char);
    }
    res
}