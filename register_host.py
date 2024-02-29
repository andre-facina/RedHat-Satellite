#!/usr/bin/env python3
# This script registers a host to the satellite. Tested in satellite version 6.14
import argparse
import subprocess

def generate_registration_command(hostname, user, token, activation_key):
    curl_command = f'curl -X POST https://{hostname}/api/registration_commands --user {user}:{token} -H \'Content-Type: application/json\' -d \'{{ "registration_command": {{ "activation_keys": ["{activation_key}"] }} }}\' -k'

    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    
    response_json = result.stdout.strip()
    registration_command = eval(response_json)['registration_command']

    registration_command = registration_command.replace('| bash', '-k | bash')

    return registration_command

def main():
    parser = argparse.ArgumentParser(description='Generate and execute registration command.')
    parser.add_argument('--hostname', required=True, help='Hostname of the API')
    parser.add_argument('--user', required=True, help='User for authentication')
    parser.add_argument('--token', required=True, help='Token for authentication')
    parser.add_argument('--ak', required=True, help='Activation key')
    args = parser.parse_args()

    registration_command = generate_registration_command(args.hostname, args.user, args.token, args.ak)
    print(f'Resulting registration command:\n{registration_command}')

    try:
        subprocess.run(registration_command, shell=True, timeout=60)
    except subprocess.TimeoutExpired:
        print("The registration continues in backgroud")

if __name__ == "__main__":
    main()

