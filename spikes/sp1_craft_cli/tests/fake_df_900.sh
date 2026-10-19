#!/usr/bin/env bash
# fake_df_900.sh: a stand-in for 'df -BM -P /' that reports 900 MB available. Used with LJ_DF_CMD to test the disk rules
# of run_sp1.sh without filling the disk. It reads nothing and writes nothing.
printf 'Filesystem     1M-blocks  Used Available Use%% Mounted on\n'
printf 'fake           258020M 257120M      900M  100%% /\n'
