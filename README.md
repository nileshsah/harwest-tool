# 📦 Harwest ⛏

[![PyPI](https://img.shields.io/pypi/v/harwest.svg)](https://pypi.python.org/pypi/harwest)
[![Downloads](https://pepy.tech/badge/harwest)](https://pepy.tech/project/harwest)
[![PyPI](https://img.shields.io/pypi/l/harwest.svg)](https://github.com/nileshsah/harwest-tool/blob/master/LICENSE)

**Harwest** takes away the hassle of managing your submission files on different online-judges by
automating the entire process of collecting and organizing your code submissions in one single Git repository.

## Highlights
* Fully automated collection of all yours submissions with minimal effort setup
* Simple and easy to use interface to get you started in minutes
* Extensive traceability for your submissions with reference to the problem, tags, submission date and more
* Single commit for each submission stamped with the original submission date for building rich and accurate contributions graph
* Automated git pushes to the remote repository with every update
* Requires little to no knowledge of operating Git (though would strongly recommend learning it)

## Platforms

Harwest currently has extensive support for the [Codeforces](https://codeforces.com/) platform 
while integration with various other OJs are still in the kitchen. Contributions are always welcomed.


## Installation

You will require `Python 3.5+` along with `pip3` in order to be able to install and use Harwest.
Refer to the documentation for installing `pip` on [windows](https://phoenixnap.com/kb/install-pip-windows), 
[ubuntu/linux](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) or
[macOS](https://docs.python-guide.org/starting/install3/osx/)

The package is available at <https://pypi.python.org/pypi/harwest> [![PyPI](https://img.shields.io/pypi/v/harwest.svg)](https://pypi.python.org/pypi/harwest)

Run the following command in the terminal to install the package:
```bash
$ pip3 install harwest
```


## Getting Started

After installing the package, run the following command in the terminal:
```bash
$ harwest
```

In case you're using Harwest for the first time, you'd be greeted with a set of configuration steps
that you'll have to complete to set up the tool.

- **Step [1]** requires you to select a directory name where all your code submissions will be stored. 
  The directory will be created under the same path from where you executed the command. 
  
  In case
  you'd like to set up the directory at some other location then press \<Ctrl\>+\<C\> to exit from
  the setup and execute the command again from your desired location.
- **Step [2]** is straight-forward and asks you to enter your full-name and email address which will be 
  used for setting up the git repository. 
  
  NOTE: For the contributions to show up in the contributions streak graph, the provided email 
  address must be the same as the email address associated with your GitHub/BitBucket account 
  
- **Step [3]** though optional, takes away the effort of even pushing the changes to the Git repository
  from you. To take advantage of this feature, create an **empty** git repository in [GitHub](https://github.com/new) 
  or BitBucket _(without any README, .gitignore or license)_ and copy and paste the git remote url
  as input for this step. 
  
  If you however don't want automated pushes for your repository then leave 
  the input as empty and press \<enter\>. You can always push the repository to remote manually.


```bash
nellex@HQ:~$ harwest

      __  __                              __
     / / / /___ _______      _____  _____/ /_
    / /_/ / __ `/ ___/ | /| / / _ \/ ___/ __/
   / __  / /_/ / /   | |/ |/ /  __(__  ) /_
  /_/ /_/\__,_/_/    |__/|__/\___/____/\__/

  ==========================================

Hey there! 👋 Looks like you're using Harwest for the first time. Let's get you started 🚀

[1] We'll need to create a directory to store all your files
    The directory will be created as /home/nellex/<your-input>
> So, what would you like your directory to be called? accepted
👍 Alright, so you're directory will be created at /home/nellex/accepted

[2] Then let's build your author tag which will appear in your Git commits as:
    Author: Steve Jobs <steve.jobs@apple.com>
> So what would your beautiful (Author) Full Name be? Nilesh Sah
> And of course, your magical (Author) Email Address? nilesh.sah13@gmail.com

[3] Guess what? We can automate the Git pushes for you too! 🎉
   In case you'd like that, then please specify the remote Git Url for an "empty" repository
   It would be somewhat like https://github.com/nileshsah/harwest-tool.git
   But it's optional, in case you'd like to skip then leave it empty and just hit <enter>
> (Optional) So, what would be the remote url for the repository again? https://github.com/nileshsah/accepted.git

 🥳 You rock! We're all good to go now
```

Once the initial set up is complete, you can then execute the command

```bash
$ harwest codeforces
```
to harvest your submissions from the Codeforces platform. If it's the first time you're running the 
command, you'll be prompted for providing your Codeforces handle name
```bash
> So what's your prestigious Codeforces Handle Name? nellex
```

Harwest will then start scraping all your submissions, starting from page 1 till the very end.

```bash
nellex@HQ:~$ harwest codeforces

      __  __                              __
     / / / /___ _______      _____  _____/ /_
    / /_/ / __ `/ ___/ | /| / / _ \/ ___/ __/
   / __  / /_/ / /   | |/ |/ /  __(__  ) /_
  /_/ /_/\__,_/_/    |__/|__/\___/____/\__/

  ==========================================

⛏ ️Harvesting Codeforces (nellex) Submissions to /home/nellex/accepted
⌛  Currently scanning page #1: (24/24) Phoenix and Beauty https://codeforces.com/contest/1348/problem/B
Username for 'https://github.com': nileshsah
Password for 'https://nileshsah@github.com':
👌 The updates were automatically pushed to the remote repository
✅ The repository was successfully updated!
```

In case scanning stops at any page due to some server side error, you can restart scraping from the
failed page by running the command

```bash
$ harwest codeforces --start-page 3 # the desired page number
```

## Reconfigure

Harwest settings can be reconfigured by running the following command which will then restart the
entire configuration steps.

```bash
$ harwest --init
```
Harwest provides the ability to re-use an existing directory previously created by this tool for 
further updates.

## License

MIT License
