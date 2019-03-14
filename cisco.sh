#!/usr/bin/expect -f
set examined_host "192.168.1.1"
set username "my_username"
set password "my_password"

set timeout 4
log_user 0

set arg1 [lindex $argv 0];
set arg2 [lindex $argv 1];

if {$examined_host != ""} {
    send_user "$examined_host: "

    spawn telnet $examined_host
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
        send "$username\n"
        send_user "Username sent, "
    }

    expect -re ".*assword:.*" {
        send "$password\n"
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
