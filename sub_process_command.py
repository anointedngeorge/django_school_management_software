import subprocess

def create_tenant(schema_name, school_name, school_phone, school_address):
    command = "python3 manage.py create_tenant"
    try:
        # Open a subprocess with stdin/stdout pipes
        with subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as proc:
            # Provide input to the subprocess
            input_data = f"{schema_name}\n {school_name}\n{school_phone}\n{school_address}"
            stdout, _ = proc.communicate(input=input_data)

            # Check if the command executed successfully
            if proc.returncode == 0:
                print("Tenant created successfully.")
            else:
                print("Failed to create tenant.")

            # Print any output from the command
            print(stdout)

    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        print("Error:", e)

# Example usage
schema_name = input("Schema name: ")
school_name  = input("School name: ")
school_phone  = input("School phone: ")
school_address  = input("School Address: ")
create_tenant(schema_name, school_name,school_phone, school_address)