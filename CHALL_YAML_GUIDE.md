# chall.yaml Documentation

This is a guide on what the `chall.yaml` file is, how to create one, and how the different fields are used.

## General Information

### What is a chall.yaml file?

A `chall.yaml` file contains information about a specific challenge. Each challenge is **required** to have a `chall.yaml` file in the root of the challenge directory.

ARCS uses the information in the `chall.yaml` file to display the challenge's description, points, author, showing file attachments, etc. on the CTF website. It will also host service challenges (if specified) and will automatically add a link to the challenge's service on the CTF website.

See [the example challenge's chall.yaml file](/example/chall.yaml) for an example of a complete and basic `chall.yaml` file.

## Fields

### `name`

- **Type:** String
- **Required:** Yes
- **Description:** The name of the challenge. This is what will be displayed on the competition website.
- **Example:**
    ```yaml
    name: "Hello World"
    ```


### `categories`

- **Type:** List of Strings
- **Required:** Yes
- **Description:** The categories that the challenge falls under. Categories MUST be `misc`, `binex`, `crypto`, `foren`, `rev`, `webex`.
- **Example:** 
    ```yaml
    categories:
        - misc
        - crypto
    ```

### `tags`
- **Type:** List of Strings
- **Required:** No
- **Description:** Tags for the challenge. These are used to filter challenges on the competition website. Can not contain duplicates from the `categories` field.
- **Example:**
    ```yaml
    tags:
        - "Hello"
        - "World"
    ```

### `value`
- **Type:** Integer
- **Required:** Yes
- **Description:** The point value of the challenge. Usually a multiple of 25.
- **Example:**
    ```yaml
    value: 100
    ```

### `flag`
- **Type:** String or Path
- **Required:** Yes
- **Description:** The correct flag for the challenge. Make sure the flag is following the format of its specific CTF. **NOTE:** This can either be the string itself or a path to a file containing the flag. The path must be relative to the root of the challenge directory.
- **Example:**
    ```yaml
    flag: flag{this_is_a_flag}
    ```
    OR
    ```yaml
    flag:
        file: ./flag.txt
    ```
    where `/<challenge_dir>/flag.txt` contains the flag.

### `description`
- **Type:** String
- **Required:** Yes
- **Description:** The description of the challenge. This is what will be displayed on the competition website. You can use markdown and multiple lines in this field. Try to use proper grammar and spelling.
- **Example:**
    ```yaml
    description: |
        This is a challenge about saying hello to the world. This is **very** important because I put it in bold.

        And this is a new paragraph!
        
        aaaaaaaaaaaaa  
    ```

### `hints`
- **Type:** List of Strings
- **Required:** Yes
- **Description:** Hints for the challenge.
- **Example:**
    ```yaml
    hints:
        - "This is a hint!"
        - "This is another hint!"
    ```

### `deploy`
- **Type:** Dictionary
- **Required:** No
- **Description:** Information about how to deploy the challenge. This is only required for service challenges (e.g. webex or binex with netcat). Note a Dockerfile is required.
- **Example:**
    - Web Example:
        ```yaml
        deploy:
            web: # Name of the container
                build: . # Directory relative to the challenge directory's root containing the Dockerfile.
                expose: 1337/tcp # port/<tcp or udp>
        ```
    - netcat Binex Example:
        ```yaml
        deploy:
            nc: # Name of the container
                build: . # Directory relative to the challenge directory's root containing the Dockerfile.
                expose: 1337/tcp # port/<tcp or udp>
        ```

### `authors`
- **Type:** List of Strings
- **Required:** Yes
- **Description:** The authors of the challenge. This is how your name will be displayed on the competition website, so use a nickname if you want.
- **Example:**
    ```yaml
    authors:
        - John Doe
        - Jane Doe
    ```

### `files`
- **Type:** List of Paths
- **Required:** No
- **Description:** A list of files that will be displayed on the challenge's page to be downloaded. The paths must be relative to the root of the challenge directory. File names can be changed using the `dest` attribute. Note that files from a container can also be added here; see the example below.
- **Example:**
    ```yaml
    files:
        - src: ./source.js # File named source.js will be displayed as source.js
        - src: ./hello.txt
          dest: bye.txt # File named hello.txt will be displayed bye.txt
        - src: /home/ctf/file_from_container.txt
          dest: file_from_container.txt
          container: nc # The container to copy the file from
    ```

### `visible`
- **Type:** Boolean
- **Required:** No
- **Description:** Whether or not the challenge should be visible on the competition website. Defaults to `true`.
- **Example:**
    ```yaml
    visible: false
    ```

## Notes
- Comments can be added to a `chall.yaml` file using the `#` character. Anything after the `#` on that line will be ignored.
- Looking at similar previous challenges is a good way to see how to format your `chall.yaml` file if you're confused.
- If you're still confused, ask an admin for help.
