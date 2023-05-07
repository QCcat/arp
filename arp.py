import sys
import os

def default(alias_file):
    #2023 Ubuntu

    bashrc = r"""
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

    """
    f = open(alias_file, 'w')
    f.write(bashrc)
    f.close()

    os.system('. ~/.bashrc')




def add_alias(alias_name, alias_command, alias_file):
    alias = f"alias {alias_name}='{alias_command}'\n"

    try:
        with open(alias_file, "a") as f:
            f.write(alias)
            os.system(". ~/.bashrc")
    except IOError:
        print("Write error")


def list_aliases(alias_file):
    print("------------------------")

    try:
        with open(alias_file, "r") as f:
            for line in f:
                if "alias" in line and "=" in line:
                    print(line[:-1])
    except IOError:
        print("Read error")

    print("------------------------")


def remove_alias(alias_name, alias_file):
    try:
        # alias_file = ('f.txt')
        with open(alias_file, "r") as f:
            aliases = f.readlines()

        with open(alias_file, "w") as f:
            for alias in aliases:
                if alias_name not in alias:
                    f.write(f'{alias}\n')    

        os.system('. ~/.bashrc')
    except:
        print("Read error")


def show_help():
    print(
        """
    [ arp - alias redactor ]
    ------------------------------------------
    new     -- create new alias [ new <alias name> <command> ]
       Important! if the alias contains more than one command,
       then the quotation marks are required:
       [ new <alias name> <'command command ...'> ]

       ( It is highly discouraged to create aliases 
       with less than 3 letters )
    
    remove  -- remove alias [ remove <alias name> ]
    list    -- alias list [ list ]
    default -- default alias file [ default ]
       Also possible manually:
       [ /bin/cp /etc/skel/.bashrc ~/ ]
    __________________________________________
        """
    )


def run():
    user = os.getlogin()
    alias_file = f"/home/{user}/.bashrc"

    if len(sys.argv) > 1:
        if sys.argv[1] == "new":
            if len(sys.argv) == 4:
                add_alias(sys.argv[2], sys.argv[3], alias_file)
            else:
                print("Usage: new <alias name> <alias command>")

        elif sys.argv[1] == "list":
            list_aliases(alias_file)

        elif sys.argv[1] == "remove":
            if len(sys.argv) == 3:
                remove_alias(sys.argv[2], alias_file)
            else:
                print("Usage: remove <alias name>")
        
        elif sys.argv[1] == "default":
            default(alias_file)

        elif sys.argv[1] in ["help", "h"]:
            show_help()

        else:
            print("Error: Invalid command")

    else:
        print("arp: no command specified")


if __name__ == "__main__":
    run()
