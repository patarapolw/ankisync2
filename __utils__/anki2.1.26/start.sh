#!/bin/sh

x11docker \
    --xpra --clipboard --pulseaudio --no-entrypoint --home=$PWD/home \
    -- \
    -- patarapolw/anki2.1.26 anki
