#!/bin/bash
# Γιώργος Κουτσουραδής — πλήρες build (cloud container paths)
set -e
K=/home/claude/k; A=$K/advon; R=$K/repo
python3 $K/src/site.py | tail -1
python3 -W ignore $A/privacy/privacy_fix.py apply $R >/dev/null
sed -i 's/μέσω αυτής της ιστοσελίδας είναι Γιώργος Κουτσουραδής/μέσω αυτής της ιστοσελίδας είναι ο Γιώργος Κουτσουραδής/' $R/privacy.html
(cd $R && python3 -W ignore $A/favicon.py make $R assets/img/giorgos-koutsouradis-logo-icon.svg --tile "#F7F3EC" | tail -1)
python3 -W ignore $A/seo_live.py fix $R gkoutsouradis.gr | tail -1
python3 -W ignore $A/ai_seo.py fix $R gkoutsouradis.gr | tail -1
python3 $K/src/post.py
python3 -W ignore $A/seo_live.py schema $R | tail -1
python3 -W ignore $A/seo_rank.py check $R gkoutsouradis.gr | tail -1
(cd $R && python3 -W ignore $A/favicon.py check $R | tail -1)
python3 -W ignore $A/privacy/privacy_fix.py check $R | tail -1
