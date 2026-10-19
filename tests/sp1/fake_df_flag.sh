#!/usr/bin/env bash
# fake_df_flag.sh: a stand-in for 'df -BM -P /' that reports 2000 MB available until the file named by LJ_FAKE_DF_FLAG exists, then 100 MB
# (below the 250 MB hard floor). The test creates the file a few seconds into a stage to show that the guard stops the stage and the stage cleans up.
if [ -n "${LJ_FAKE_DF_FLAG:-}" ] && [ -e "$LJ_FAKE_DF_FLAG" ]; then a=100; else a=2000; fi
printf 'Filesystem     1M-blocks  Used Available Use%% Mounted on\n'
printf 'fake           258020M 256020M %5sM  100%% /\n' "$a"
