# Connor Constantino<br>UVM Cybersecurity Principles (CS166 / CS2660) Final Project
This project was created as a final project for the Cybersecurity Principles class I took while a student at UVM.

## Setup and Operation
No setup is required. All modules are from the Python standard library.

The program is run by running the menu.py module. When you run the module for the first time,
a credentials database will be created with the default values stored in logins.json. 

## Description and Features
This project is a text-based simulation of a cryptographically secure login system. It supports multiple users as 
well as the ability to add new users. Passwords are salted and hashed before being stored and are subjected to the
following requirements:
<ul>
    <li>Must be between 8 and 25 characters, inclusive</li>
    <li>Must have at least one of each of the following:
        <ul>
            <li>Uppercase characters</li>
            <li>Lowercase characters</li>
            <li>Special characters</li>
            <li>Punctuation</li>
        </ul>    
    </li>
</ul>
When creating a new user, passwords can be manually entered or automatically generated. Each user has an access level
which determines which departments they are able to access.

<hr>
The following sets of usernames, passwords, and access levels are built in as defaults and can be used to test.
Note, these do not follow the password requirements detailed above. This is so when testing the program, passwords are
quicker to type.
<table>
    <tr>
        <th>Username</th>
        <th>Password</th>
        <th>Access Level</th>
    </tr>
    <tr>
        <td>Dave</td>
        <td>Dave123</td>
        <td>2</td>
    </tr>
    <tr>
        <td>Aria</td>
        <td>123789</td>
        <td>3</td>
    </tr>
    <tr>
        <td>David</td>
        <td>passw0rd</td>
        <td>1</td>
    </tr>
    <tr>
        <td>Jane</td>
        <td>bAnAnAsPlIt</td>
        <td>2</td>
    </tr>
</table>

