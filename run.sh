#!/bin/sh --

# This script runs puzzle solvers.
#
# One advantage of having a shell script to run solvers, rather than just
# running `run.py` directly, is that this script can decide on the fly which
# Python implementation to use.

set -o nounset


BLUE='\033[34;1m'
END_COLOR='\033[0m'

if [ -t 1 ]; then
    HEADING="$BLUE"
    END_HEADING="$END_COLOR"
else
    HEADING=''
    END_HEADING=''
fi


# Print a usage message to stderr.
print_usage() {
    printf "Usage: %s [-t|--time] [year [day]]\n" "$0" >&2
}

# Print a string indicating which command to use for timings.
time_mode() {
    if env time --format="(%es)" true >/dev/null 2>&1; then
        echo 'env-time'
    elif (time -p true) >/dev/null 2>&1; then
        echo 'time-p'
    else
        echo 'time'
    fi
}

# Return 0 (success) if a faster Python interpreter should be used.
use_fast_python() {
    # $1: year
    # $2: day
    [ "$1" -eq 2019 ] && [ "$2" -eq 9 ]
}

# Print the name of the fastest known suitable installed Python interpreter.
fast_python() {
    if can_use_pypy; then
        echo 'pypy3'
    else
        echo 'python3'
    fi
}

# Return 0 (success) if a suitable version of PyPy is installed.
can_use_pypy() { (
    if ! type pypy3 >/dev/null 2>&1; then
        return 1
    fi

    i=0
    for word in $(pypy3 --version); do
        if [ $i = 1 ]; then
            break
        fi
        if [ "$word" != 'Python' ]; then
            return 1
        fi
        i=1
    done

    IFS="."
    i=0
    for part in ${word-}; do
        if [ $i = 1 ]; then
            break
        fi
        if [ "$part" -ne 3 ] 2>/dev/null; then
            return 1
        fi
        i=1
    done

    [ "${part-}" -ge 6 ] 2>/dev/null
); }

# Print a heading and the solution to a puzzle.
run_day() {
    # $1: time mode
    # $2: fast Python
    # $3: program path

    if [ ! -e "$3" ]; then
        echo "Error: no programs found" >&2
        return 1
    fi

    year_dir_="${3%/*}"
    year_="${year_dir_#advent}"
    day_="${3#*/d}"
    day_="${day_#0}"
    day_="${day_%%_*}"

    if use_fast_python "$year_" "$day_"; then
        python_="$2"
    else
        python_='python3'
    fi

    printf "${HEADING}# %d, day %d #${END_HEADING}\n" "$year_" "$day_"
    solve "$1" "$python_" "$year_" "$day_"
    ret=$?
    echo
    return "$ret"
}

# Print the solution to a puzzle.
solve() {
    # $1: time mode
    # $2: Python command
    # $3: year
    # $4: day

    if [ "$1" = 'env-time' ]; then
        env time --format="(%es)" "$2" run.py "$3" "$4"
    elif [ "$1" = 'time-p' ]; then
        time -p "$2" run.py "$3" "$4"
    elif [ "$1" = 'time' ]; then
        time "$2" run.py "$3" "$4"
    else
        "$2" run.py "$3" "$4"
    fi
}

# Solve the puzzle or puzzles specified by the arguments.
#
# If '--time' is given as an argument, print timings.
#
main() {
    real_path="$(readlink -f -- "$0" 2>/dev/null)" || real_path="$0"
    base_path="$(dirname -- "$real_path")" || return
    cd -- "$base_path" || return

    # Parse command-line arguments.
    year=''
    day=''
    mode=''
    for arg in "$@"; do
        case "$arg" in
        -*)
            if [ "$arg" = '-t' ] || [ "$arg" = '--time' ]; then
                if [ -z "$mode" ]; then
                    mode="$(time_mode)"
                fi
            else
                print_usage
                return 1
            fi
            ;;
        *)
            if [ -z "$year" ]; then
                year="$arg"
                # Using `[0123456789]` to try to avoid matching other Unicode
                # digits.
                if ! [ "$(expr "$year" : '[0123456789]\{4\}$')" -gt 0 ]; then
                    print_usage
                    printf "Error: invalid year '%s'\n" "$arg" >&2
                    return 1
                fi
            elif [ -z "$day" ]; then
                day="$arg"
                if ! [ "$(expr "$day" : '[0123456789]\{1,2\}$')" -gt 0 ]; then
                    print_usage
                    printf "Error: invalid day '%s'\n" "$arg" >&2
                    return 1
                fi
            else
                print_usage
                return 1
            fi
            ;;
        esac
    done

    if [ "$day" ]; then
        if use_fast_python "$year" "$day"; then
            python="$(fast_python)"
        else
            python='python3'
        fi
        solve "$mode" "$python" "$year" "$day"
        return
    fi

    fast="$(fast_python)"

    if [ "$year" ]; then
        year_dir="advent${year}"
        for program in "$year_dir"/d??*.py; do
            run_day "$mode" "$fast" "$program" || return
        done
    else
        for program in advent????/d??*.py; do
            run_day "$mode" "$fast" "$program" || return
        done
    fi
}

main "$@"
