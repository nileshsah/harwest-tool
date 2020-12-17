# 📦 Harwest ⛏

[![PyPI](https://img.shields.io/pypi/v/harwest.svg)](https://pypi.python.org/pypi/harwest)
[![Downloads](https://pepy.tech/badge/harwest)](https://pepy.tech/project/harwest)
[![PyPI](https://img.shields.io/pypi/l/harwest.svg)](https://github.com/nileshsah/harwest-tool/blob/master/LICENSE)

Your ultimate one-shot tool to har(w)est submissions from different platforms onto one single Git repository

**Harwest** takes away the hassle of managing your submission files on different online-judges by automating the entire process of collecting and organizing your code submissions in one single Git repository.

## Highlights
* Fully automated collection of your most recent submissions with minimal effort setup
* Simple and easy to use interface to get you started in minutes
* Extensive traceability for your submissions with reference to the problem, tags, submission date and more
* Single commit for each submission stamped with the original submission date for building rich and accurate contributions graph
* Automated git pushes to the remote repository with every update
* Requires little to no knowledge of operating Git (though would strongly recommend learning it)

## Platforms

Harwest currently has extensive support for the [Codeforces](https://codeforces.com/) platform 
while integration with various other platforms are still in the kitchen. Contributions are always welcomed.


## Installation

You would need `Python 3.5+` along with `pip3` in order to be able to install and use the tool. 
Refer to the documentation for installing `pip` on [windows](https://phoenixnap.com/kb/install-pip-windows), 
[ubuntu/linux](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) or
[mac](https://docs.python-guide.org/starting/install3/osx/) 

The package is available at <https://pypi.python.org/pypi/harwest> [![PyPI](https://img.shields.io/pypi/v/harwest.svg)](https://pypi.python.org/pypi/harwest)
Run the following command in the terminal to install the package:
```bash
$ pip3 install harwest
```


## Getting Started

After installing the package, run the command in the terminal:
```bash
$ harwest
```

In case you're using Harwest for the first time, you'd be greeted with a set of configuration steps
that you'll have to complete to set up the tool.

- **Step [1]** requires you to select a directory name where all your code submissions will be stored. 
  The directory will be created under the same path from where you executed the command. In case
  you'd like to set up the directory at some other location then press \<Ctrl\>+\<C\> to exit from
  the setup and execute the command again from your desired location.
- **Step [2]** is straight-forward and asks you to enter your full-name and email address which will be 
  used for setting up the git repository. **NOTE:** For the contributions to show up in the 
  contributions streak graph, the provided email address must be the same as the email address
  associated with your GitHub/BitBucket account 
  (refer: <https://dev.to/duhbhavesh/why-my-commits-aren-t-showing-up-on-github-contributions-graph-3a2h>)
- **Step [3]** though optional, takes away the effort of even pushing the changes to the Git repository
  from you. To take advantage of this feature, create an **empty** git repository in [GitHub](https://github.com/new) 
  or BitBucket _(without any README, .gitignore or license)_ and copy and paste the git remote url
  as input for this step. If you however don't want automated pushes for your repository then leave 
  the input as empty and press \<enter\>.   


```bash
nellex@HQ:~$ harwest

      __  __                              __
     / / / /___ _______      _____  _____/ /_
    / /_/ / __ `/ ___/ | /| / / _ \/ ___/ __/
   / __  / /_/ / /   | |/ |/ /  __(__  ) /_
  /_/ /_/\__,_/_/    |__/|__/\___/____/\__/

  =============================== by _nellex_

Hey there! 👋 Looks like you're using Harwest for the first time. Let's get you started 🚀

[1] We'll need to create a directory to store all your files
    The directory will be created as /home/nellex/<your-input>
> So, what would you like your directory to be called? accepted
👍 Alright, so you're directory will be created at /home/nellex/accepted

[2] Then let's build your author tag which will appear in your Git commits as:
    Author: Steve Jobs <steve.jobs@apple.com>
> So what would your beautiful (Author) Full Name be? Nilesh Sah
> And of course, your magical (Author) Email Address? niles*******@gmail.com

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
In case the scraping stops at any page due to some server error, you can restart scraping from the 
failed page by running the command (page 3 in this case)

```bash
$ harwest codeforces --start-page 3
```

## License

MIT License
