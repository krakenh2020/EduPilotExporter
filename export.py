import json
import os

import click


def get_credentials(creds_path, cred_type):
    # Open directory and recursively yield json decoded content of all json files.
    # Return an error if content is not json decodable.
    for root, dirs, files in os.walk(creds_path):
        if cred_type not in root:
            continue
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file)) as f:
                    try:
                        yield json.load(f)
                    except json.decoder.JSONDecodeError:
                        click.echo(f"Error: {file} is not valid json.")


# Get all keys of a dict and return them as list.
def get_keys(cred):
    for key in cred.keys():
        yield key
        if isinstance(cred[key], dict):
            yield from get_keys(cred[key])


def get_fields_for_credential_type(cred_type):
    if cred_type == "course-grades":
        return ['id', 'name', 'grade']
    if cred_type == "diploma":
        return ['id', 'academicDegree', 'name']
    raise Exception(f"Unknown credential type: {cred_type}")


def get_line(cred, cred_fields):
    return [str(cred.get(field, "")) for field in cred_fields]


def write_to_csv(fields, data, output):
    # Write data to csv file.
    with open(output, "w") as f:
        f.write(", ".join(fields) + "\n")
        for line in data:
            f.write(", ".join(line) + "\n")


@click.command()
@click.option('--path', default='instance/uploads', help='Path to directory with credentials')
@click.option('--cred_type', default='course-grades', help='course-grades or diplomas')
@click.option('--output', default='data.csv', help='Path to output file')
def main(path, cred_type, output):
    fields = get_fields_for_credential_type(cred_type)
    lines = []
    for cred in get_credentials(path, cred_type):
        line = get_line(cred['credentialSubject'], fields)
        lines.append(line)
    write_to_csv(fields, lines, output)


if __name__ == '__main__':
    main()
