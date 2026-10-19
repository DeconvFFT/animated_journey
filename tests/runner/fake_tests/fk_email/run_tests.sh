#!/usr/bin/env bash
# Fake area whose output holds PLANTED identifying-looking strings, built at run time from fragments so that this
# file itself holds none of them. The runner must mask them everywhere it stores or prints them. Exits 0.
set -u
mail="$(printf '%s%s%s%s' 'zz.planted' '@' 'nowhere-co' '.org')"
home="$(printf '%s%s%s' '/ho' 'me/' 'alice-fake/notes.txt')"
echo "fk_email: mode=${1#--}"
echo "contact $mail was seen in this output"
echo "log written to $home today"
echo "RESULT PASS fk_email :: planted contact $mail printed"
exit 0
