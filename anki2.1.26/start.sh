#!/bin/sh

x11docker \
    --hostdisplay --clipboard --pulseaudio --no-entrypoint --home=$PWD/home \
    -- \
    -- patarapolw/anki2.1.26 anki
