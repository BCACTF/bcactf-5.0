def sanitize(letter):
    print("Checking for contraband...")
    return any([i in letter.lower() for i in BANNED_CHARS])

BANNED_CHARS = "gdvxftundmnt'~`@#$%^&*-/.{}"
flag = "bcactf{PyTH0n_pR0_03ed78292b89c}"

print("Welcome to the prison's mail center")
msg = input("Please enter your message: ")

if sanitize(msg): 
    print("Contraband letters found!\nMessage Deleted!")
    exit()

exec(msg)