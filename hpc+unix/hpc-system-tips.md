# A nicer `squeue`

```
squeue --format="%.18i %.18P %.30j %.8u %.8T %.10M %.9l %.6D %.20S %R" --me
```

# Using `except` to log in faster and easier (with 1password)

Usage of script: ./ssh_shortcut horeka/uc2

```sh
#!/usr/bin/expect 

set system [lindex $argv 0];

if { $system == "horeka"} {

        send_user "Logging into Horeka\n"
        # set OTP variable from password manager
        set otp [exec op item get KIT --otp]
        # set pw as password from passwork manager
        set pw [exec op item get KIT --fields=horeka]
        # requires having set up ssh config to be able to call 'ssh horeka'
        spawn ssh horeka
        expect "*OTP: "
        send "$otp\r"
        expect "*Password: "
        send "$pw\r"
        interact

} elseif { $system == "uc2" } {

        send_user "Logging into UC2\n"
        set otp [exec op item get KIT --otp]
        set pw [exec op item get KIT --fields=uc2]
        spawn ssh uc2
        expect "*OTP: "
        send "$otp\r"
        expect "*Password: "
        send "$pw\r"
        interact

} else {

        send_user "System not found"

}
```
