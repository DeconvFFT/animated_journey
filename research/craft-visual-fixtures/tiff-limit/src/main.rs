use std::io::BufReader;
use tiff::decoder::{Decoder, Limits};

// Same limit shape LightCraft v0.9.1 builds in crates/codecs/src/tiff_codec.rs::limits()
// (max_pixels default 1<<30): decoding_buffer_size = max_pixels*32, ifd_value_size = 32 MiB,
// intermediate_buffer_size left at the crate default (128 MiB).
fn main() {
    for path in std::env::args().skip(1) {
        let f = BufReader::new(std::fs::File::open(&path).unwrap());
        let mut limits = Limits::default();
        limits.decoding_buffer_size = ((1u64 << 30) * 32).min(usize::MAX as u64) as usize;
        limits.ifd_value_size = 32 << 20;
        let mut d = Decoder::new(f).unwrap().with_limits(limits);
        let dims = d.dimensions().unwrap();
        let res = d.read_image();
        match res {
            Ok(_) => println!("{path}: {dims:?} OK"),
            Err(e) => println!("{path}: {dims:?} ERR {e}"),
        }
    }
}
