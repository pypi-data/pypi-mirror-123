# Wallpaper Changing Daemon (wcd)
Wallpaper Changing Daemon reminds me of mpd, but it manages wallpapers instead of music.

## Overview
* It comes with wcc too, which is a CLI client app, used to interact with the Daemon.
* It works on python 3.9 (and, probably, on 3.7 and 3.8 too, not sure about lower versions though).
* It only depends on `PyYAML` and `coloredlogs`, but you don't have to worry about installing them manually, pip's got you covered.
* It copies it's default config file into `~/.config/wcd/`, or to wherever you point it to, via `$WCD_CFG`.
* I only code as a hobby, but I'd say I made a good job to make this very readable and, thus, feel very welcomed to check how things are implemented, to get a better understanding of what this program does, its capabilities, etc...
* You need to have a program which will do the wallpaper switching (such as `xwallpaper`, `feh` or `nitrogen`) installed on your machine.

## Why shouldn't I just use a shell script instead
Lots of people use shell scripts in which they have shell scripts like this:

    while true; do
        for file in "$(find /usr/share/backgrounds/ -type f | shuf)"; do
            xwallpaper --zoom "$file"
        done
    done

And that's fine, but I don't like that approach because it's too limiting. What if, actually, you don't like a wallpaper that has been presented to you? Well, then, you'd have to manually change it. With wcd and wcc, you can interact with the daemon as it presents wallpapers to you, going back and forward in a history buffer, choosing to start or to stop randomizing wallpapers, or just getting the next one presented to you if you don't like the current one anymore, all with a single keypress (see "sxhkd keybindings for wcc" below).

## Installation
1. Install the package with [pipx](https://github.com/pypa/pipx): `pipx install wcd` or clone this repo and run `setup.py`
    * If you use Arch based distros, you can install pipx as such: `sudo pacman -S python-pipx`
2. Run the package once, to generate config files. If you want to, you can point to where you want your config to be stored in by exporting an evironment variable named `WCD_CFG`, like this:
    * `export WCD_CFG="path/to/config" # be sure to add this line to your ~/.profile or ~/.bashrc or whatever shell you use`
    * `wcd`
3. Load the config file (defaults to `~/.config/wcd/cfg.yml`) on your text editor and change the `wallpaper_cmd` entry to whatever suits you best.
4. Kill the previous running instance if you haven't already and, then, restart the program.
5. You're all set, enjoy.

### Installing and Running as systemd Service
1. Clone this repo: `git clone https://github.com/brunofauth/wcd.git`
2. cd into it: `cd wcd`
3. edit `wcd.service` to include whatever you get when you run `which wcd`
4. Copy the unit file to your systemd config folder: `cp wcd.service ~/.config/systemd/user/wcd.service`
5. To enable starting wcd on login, run: `systemctl enable --user wcd.service`
6. To immediatly start wcd, run: `systemctl start --user wcd.service`

## Communicating with the wcd
* Run: `wcc --help`, it stands for Wallpaper Changing Client and comes bundled with `wcd`

## sxhkd keybindings for wcc (append to your sxhkdrc)
    shift + XF86Audio{Play,Next,Prev}
        wcc {toggle_cycle,next,prev}

## TODO
* aur package

