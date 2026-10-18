Round 2 test of the LightCraft v0.9.1 TIFF strip limit (research/craft-visual.md, R12).
Not a Craft app: a 25-line harness around the Rust `tiff` crate 0.11.3 (the version in LightCraft v0.9.1's Cargo.lock),
with the same Limits that crates/codecs/src/tiff_codec.rs builds (max_pixels default 1<<30, so decoding_buffer_size = 32 GiB;
ifd_value_size 32 MiB; intermediate_buffer_size left at the crate default, 128 MiB).
  python3 -I make_fixtures.py OUTDIR      # writes ~1.2 GB of 8-bit gray TIFFs (needs numpy, Pillow); delete them afterwards
  cargo build --release && target/release/tifftest OUTDIR/*.tif
Result table: craft-visual.md, R12.
