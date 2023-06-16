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

# Sharing a Workspace
It is recommended to use ACLs via `setfacl` not `chmod` to grant other users access to a workspace.  
To grant user `ab1234` access to the workspace `my_workspace` use:

For **read only** access:
```
setfacl -Rm u:ab1234:rX,d:u:ab1234:rX $(ws_find my_workspace)
```

For **read and write** access:
```
setfacl -Rm u:ab1234:rwX,d:u:ab1234:rwX $(ws_find my_workspace)
```
When granting individual write access, it might be necessary to **set ACLs for your own user first** to be able to access the files of your co-workers.

For more information, see also: https://wiki.bwhpc.de/e/Workspace#Sharing_Workspace_Data_within_your_Workgroup
