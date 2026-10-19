#!/usr/bin/env bash
# fake_df_2000.sh: a stand-in for 'df -BM -P /' that reports 2000 MB available, so the guard accepts the tiny stand-in stages of tests/sp1.
printf 'Filesystem     1M-blocks  Used Available Use%% Mounted on\n'
printf 'fake           258020M 256020M     2000M  100%% /\n'
