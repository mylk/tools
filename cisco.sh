#!/usr/bin/expect -f

set CURRENT_DIRECTORY [file dirname $argv0]

source "${CURRENT_DIRECTORY}/secrets.tcl"

set timeout 4
log_user 0

set arg1 [lindex $argv 0];
set arg2 [lindex $argv 1];

if {$CISCO_HOST != ""} {
    send_user "$CISCO_HOST: "

    spawn telnet "$CISCO_HOST"
    match_max 100000

    expect {
        -re ".*Connection refused.*" {
            send_user "\nTelnet: Connection refused."
        }

        -re ".*but none set.*" {
            send_user "\nTelnet TTY disabled.\n"
            exit
        }

        -re ".*closed.*" {
            send_user "\nConnection closed by foreign host."
        }
    }

    expect -re ".*sername:.*" {
        send "$CISCO_USERNAME\n"
        send_user "Username sent, "
    }

    expect -re ".*assword:.*" {
        send "$CISCO_PASSWORD\n"
        send_user "Password sent, "
    }

    expect {
        -re ".*assword:.*" {
            send_user "Asked again for password (invalid)."
        }

        -re ".*Login invalid.*" {
            send_user "Login invalid."
        }

        timeout {
            send_user "Timed out. "
        }
    }

    if {$arg1 == "wifi"} {
        expect -re ".*#" {
            send_user "GOT IT!"
            send "config t\r"
        }

        if {$arg2 == "on"} {
            expect -re ".*\(config\).*" {
                send "int dot11Radio0\n"
            }

            expect -re ".*\(config\-if\).*" {
                send "no shut\n"
            }

            expect -re ".*\(config\-if\).*" {
                send "int dot11Radio0.1\n"
            }

            expect -re ".*\(config\-subif\).*" {
                send "no shut\n"
            }
        }

        if {$arg2 == "off"} {
            expect -re ".*\(config\).*" {
                send "int dot11Radio0\n"
            }

            expect -re ".*\(config\-if\).*" {
                send "shut\n"
            }

            expect -re ".*\(config\-if\).*" {
                send "int dot11Radio0.1\n"
            }

            expect -re ".*\(config\-subif\).*" {
                send "shut\n"
            }
        }
    }

    if {$arg1 == "restart"} {
        expect {
            -re ".*#" {
                send_user "GOT IT!"
                send "reload\r"
            }

            -re ".*>" {
                send_user "GOT IT!"
                send "reload\r"
            }
        }

        expect -re ".*System configuration has been modified.*" {
            send "no\r"
        }

        expect -re ".*confirm.*" {
            send "\r"
            send_user "\nReloading..."
            send "\r"
        }
    }
}

send_user "\n"
