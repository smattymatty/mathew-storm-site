---
title: 01 - Your First Contribution
created: 2025-05-22
tags:
  - git
  - github
  - contributing
  - open source
  - education
  - tutorials
  - edulite
  - beginners
---

{~ hero layout="text_left_image_right" image_src="https://1000logos.net/wp-content/uploads/2021/05/GitHub-logo.png" image_alt="GitHub Desktop logo" text_bg_color="primary-25" text_color="black-75" ~}

## Getting Started with Git & GitHub for Beginners 🚀

This guide helps new contributors learn about open source, Git, and GitHub, so you can make your first contribution.

We specifically cover the **EduLite** project, which is a great example of a project that welcomes new contributors.

You can use this information to learn more about Git and GitHub, and to contribute to open source projects in general.


{~~}

{~ alert type="success" ~}
**Welcome to your First Contribution Guide!**
If you choose to contribute to EduLite, you'll be making your first contribution to a real-world project and your work will be recognized and appreciated by the community.
{~~}

---

### What you need to get started (Requirements)

* A GitHub account (if you don't already have one)
* A text editor or IDE (preferably VS Code for this tutorial)
* The technical skills to install Git on your operating system

{~ alert type="info" ~}
**Note:** This tutorial is designed for beginners who are new to Git and GitHub, but we expect you to have some familiarity with the command line and basic programming concepts.
If these requirements are too steep, perhaps I can create a '0' level tutorial for you.
{~~}


---

### Understanding Git Basics 🛠️

* **What Git is:** A tool that tracks changes to your project, lets you go back to earlier versions, and allows multiple people to work on different parts at once.

{~ card title="Key terms" footer="Learning these terms will help you understand the fundamentals of Git." ~}

* **`Repository (Repo)`:** Where your project and its history are stored.
* **`Commit`:** A saved snapshot of your changes.
* **`Branch`:** A separate line of development within a project.
* **`Merge`:** Combining changes from different branches.
* **`Remote`:** A connection to a repository hosted elsewhere (like on GitHub).
{~~}

* **Why it's important:** Essential for managing your own projects and working effectively in a team.

---

### Using the GitHub Workflow 🔄

* **What GitHub adds:** A website that uses Git and adds features for better teamwork, like tracking issues, managing projects, and **Pull Requests**.
  
{~ card title="Standard GitHub steps" footer="These are the steps you'll follow when contributing to any project on GitHub." ~}

1. **`Fork`:** Make a personal copy of a project on GitHub.
2. **`Clone`:** Download your forked project to your computer.
3. **`Branch`:** Create a new branch for your changes (e.g., a new feature or bug fix).
4. **`Push`:** Upload your changes from your computer to your fork on GitHub.
5. **`Pull Request (PR)`:** Propose your changes to the original project.
{~~}

* **Benefits:** This process allows for clear discussion, code review, and organized contributions, especially for remote teams.

---

### Making Your First Pull Request (PR) 🎉

* **What a Pull Request is:** Your formal way to ask the project owners to include your improvements.

{~ card title="Why it's a big deal"  footer="This process provides a clear discussion, code review, and organized contributions, especially for remote teams." ~}
It shows you can use Git and GitHub and is your first step into open source.
{~~}

* **What you'll learn here:** How to find suitable tasks (like "good first issues"), make your changes, and confidently submit your first contribution to projects like EduLite.

---

## Why Learn Git & GitHub?

Understanding Git and GitHub is crucial for anyone involved in software development. Here's why:

* **A Must-Have Skill for Developers:**
    * Git and GitHub are as important as knowing a programming language for managing code.
    * Git lets you track changes, experiment safely, and see your project's history.
    * Many modern development tools (like CI/CD for automatic testing and deployment) rely on Git.

* **The Go-To for Version Control:**
    * Most companies and projects use Git to manage different versions of their code.
    * Knowing Git makes you more valuable to employers because it's used almost everywhere.

* **Key for Teamwork:**
    * Git and GitHub are built for teams to work together on the same project smoothly.
    * **Branches** let developers work on new things separately without causing problems.
    * **Pull Requests** on GitHub allow for code reviews and discussions before changes are combined. This avoids confusion and lost work.

* **Builds Your Coding Portfolio:**
    * Your GitHub profile is like a live resume that shows off your projects and skills.
    * It displays your coding abilities, how you learn, and that you can use version control.

* **Shows Your Skills to Employers:**
    * Employers often look at GitHub profiles to see a candidate's actual coding work.
    * Good code, clear notes (commit messages), and contributions to projects demonstrate your skills and passion.

---

## What You'll Learn

Here’s a summary of the topics we will go through:

* **Setting Up Git:**
    * Install Git on your computer (we'll provide links/commands).
    * Configure your Git user name and email.
    * Briefly see how to use Git with the command line and code editors (like VS Code).

{~ card title="Core Git Concepts" footer="Understand how Git works" ~}

* **`Working directory vs. staging area`:** Your current files vs. files ready to be saved.
* **`Commits`:** Snapshots of your project at a specific time.
* **`Branches`:** Parallel lines of work within your project.
* **`HEAD`:** What Git considers your current position.
* **`Local & remote repos`:** Your computer's copy vs. a copy on a server (like GitHub).
{~~}

* **Forking & Cloning Repositories:**
    * **Forking:** Creating your own server-side copy of a project (e.g., EduLite on GitHub) to work on.
    * **Cloning:** Downloading a repository (like your fork) to your computer using `git clone`.

* **Using Branches for Your Work:**
    * Learn why branches are useful for keeping new features or fixes separate and organized.
    * Practice creating and switching between branches (e.g., `git branch`, `git checkout`).

* **Making Good Commits:**
    * Save your changes by "committing" them:
        1.  Stage changes with `git add`.
        2.  Commit with `git commit`.
    * Learn to write clear and helpful commit messages.

* **Creating Pull Requests (PRs):**
    * After pushing changes to your fork on GitHub, learn to create a Pull Request.
    * A PR is how you ask for your changes to be added to the main project. It's where discussions and code reviews happen.

* **Handling Code Reviews:**
    * Understand that project maintainers will review your PR to improve code quality.
    * Learn how to take feedback, ask questions, and update your PR with more changes.

* **Contributing to Real Projects (like EduLite):**
    * Put everything together to make real contributions.
    * Learn to find beginner-friendly tasks (e.g., "good first issue") and submit your work.

---

# About Our Example Project: EduLite

* Student-first learning platform
* Built for areas with weak internet
* 100% volunteer-driven open source project
* Perfect for your first contribution
* Includes both frontend and backend opportunities

{~ alert type="success" ~}
While the **EduLite** community appreciates any contributions, the material in this tutorial can be used as a foundation for any projects.
{~~}

---

# Git: A Distributed Version Control System

Git is a powerful version control tool. Its key functions include:

* **Distributed VCS:** Tracks all file changes, supporting parallel work. Full local copies offer speed and offline use.
* **Change Tracking:** Saves all modifications as **commits** (project snapshots) for easy history review and rollbacks.
* **Team Collaboration:** Employs **branching** for isolated development and **merging** to integrate changes, managing conflicts.
* **Comprehensive History:** Logs detailed information for every commit (who, when, why), vital for audits and debugging.
* **Offline Functionality:** Most operations are performed **locally and quickly**; internet is only needed to share or fetch updates (push/pull).

---

# Git Across Different Operating Systems

{~ alert type="warning" ~}
**Git installation varies by OS:**
Getting Git onto your computer is the first hands-on step, and the method differs slightly based on your operating system. Here's a brief rundown of the most common ways:
{~~}

* **Windows:** The most straightforward method is typically to download the official installer directly from the [Git SCM website (https://git-scm.com/downloads/win)](https://git-scm.com/downloads/win). This installer often includes "Git Bash," a terminal environment that provides a Linux-like command-line experience for using Git on Windows.
* **Mac:** If you use Homebrew (a popular package manager for macOS), installing Git can be as simple as running the command `brew install git`. Alternatively, installers are also available, sometimes bundled with Xcode developer tools or directly from the [Git SCM website (https://git-scm.com/downloads/mac)](https://git-scm.com/downloads/mac).
* **Linux:** Installation is typically handled through your distribution's built-in package manager. For example:
    * On **Ubuntu/Debian** based systems, you'll use `sudo apt install git`.
    * On **Fedora**, the command is `sudo dnf install git`.
    * On **Arch Linux**, you would use `sudo pacman -S git`.

{~ alert type="success" ~}
**Good news: Once installed, Git commands are identical across all platforms:**

This is a fantastic aspect of Git! While the initial setup might differ, the core Git commands you will learn and use (`git commit`, `git branch`, `git checkout`, `git push`, `git pull`, etc.) are exactly the same whether you're on Windows, macOS, or any Linux distribution.

This universality means the skills you develop are highly transferable, and you can collaborate seamlessly with others who might be using different operating systems.
{~~}

* **All terminal commands in this course work the same on Windows, Mac, and Linux:**
    * To ensure a consistent learning experience, this course will focus on these universal Git commands as executed in a terminal or command-line interface.
    * While the terminal application itself might have a different name or appearance (e.g., Git Bash or PowerShell on Windows, Terminal on macOS, various terminal emulators on Linux), the underlying Git commands you type and their behavior will be consistent with what's taught.

{~ alert type="info" ~}
**GUI clients available for all platforms if preferred:**

If you're not entirely comfortable with the command line, or if you prefer a more visual way to interact with Git, there's good news: numerous Graphical User Interface (GUI) clients are available for all major operating systems. These tools provide a visual interface for Git operations.

While these GUI clients can be helpful, especially for visualizing branches and history, this course will primarily focus on the command-line interface to ensure you build a fundamental understanding of Git's operations, which are consistent everywhere.
{~~}

---

# Why We Use VS Code for This Tutorial

* Combines code editor and terminal in one interface
* Built-in Git integration saves time
* Visual diff tool makes changes clear
* Widely used in industry (familiar to most teams)
* Works consistently across Windows, Mac, and Linux
* Extensions enhance Git workflow
* Free and open source
* Lightweight enough for beginners

{~ alert type="danger" ~}
**Important Consideration:** While VS Code's built-in Git tools are convenient for this tutorial, make sure you also grasp the fundamental Git commands. Over-reliance on GUI features alone can sometimes hinder a deeper understanding of Git's core operations and troubleshooting.
{~~}

---

## Configuring Git in VS Code 🛠️

Before you start committing, it's essential to tell Git who you are and understand how VS Code helps with GitHub.

{~ card title="1. Set Your Git Identity 🧑‍💻" footer="This info appears on all your commits." ~}
Git needs your name and email to correctly attribute your work. These settings apply globally to all your Git projects.

Open your terminal and run:
`git config --global user.name "Your Name"`
{~~}

{~ alert type="warning" ~}
Make sure to replate `"Your Name"` and `"your.email@example.com"` with your actual name and the email address you want associated with your commits (often the one linked to your GitHub account).
{~~}

{~ card title="2. Verify Your Settings ✅" footer="This confirms your Git identity was saved correctly." ~}
Double-check that your Git identity was saved correctly:
`git config --global --list`
{~~}

{~ alert type="success" ~}
You should see your `user.name` and `user.email` in the output list. This confirms Git knows who you are for future commits!
{~~}

{~ card title="3. VS Code's GitHub Authentication Perks 🚀" footer="Without VS Code, Git would require you to re-enter your username and password." ~}
VS Code has excellent built-in features to simplify how you connect and authenticate with GitHub:

* **Easy Login:** Automatically prompts for GitHub login on your first push, especially with HTTPS.
* **Secure Credential Storage:** Safely remembers your login details (using your OS keychain or similar), so you don't have to re-enter them.
* **Automatic Token Refresh:** Handles refreshing access tokens in the background, ensuring continuous access.
* **Multiple Account Support:** Lets you manage and switch between different GitHub accounts for various projects.
{~~}

---
# VS Code's Git Integration Features

{~ card title="Key VS Code Git Features at Your Fingertips" footer="These tools streamline your Git workflow directly within the editor." ~}
Visual Studio Code offers powerful built-in Git integration and is further enhanced by extensions like GitLens. Here are some key features:

* **Source Control Tab (Ctrl+Shift+G):** Your main hub for viewing changes, staging files, committing, and managing branches.
* **Status Indicators in File Explorer:** Easily see which files are modified, added, or untracked with visual cues next to filenames.
* **Built-in Diff Viewer:** Visually compare versions of your files to see exactly what has changed.
* **Inline Blame Annotations (with GitLens):** See who last modified a line of code and when, directly in the editor (GitLens extension feature).
* **Commit Staging with Checkboxes:** Simply check boxes to select which changes or parts of files you want to include in your next commit.
* **Branch Switching from Status Bar:** Quickly view your current branch and switch to others directly from the bottom status bar.
* **Conflict Resolution Helpers:** Provides visual tools to help you resolve merge conflicts when they occur.
* **Integrated Terminal Access:** Open a terminal within VS Code to use Git command-line for any advanced operations.
{~~}

---

# Git Terminal vs. GUI Clients: Which to Use?

{~ alert type="info" title="Our Tutorial's Approach to Git Tools" ~}
In this guide, we often use VS Code, which includes excellent visual Git integration (giving you a bit of a hybrid experience!). However, to ensure you build a strong and versatile understanding of Git, we primarily focus on teaching the **terminal/command line** operations. Mastering the core commands empowers you with a deep knowledge of how Git works, allowing you to use any Git tool—whether CLI or GUI—more effectively.
{~~}

{~ card title="Comparing Git Interfaces: Terminal (CLI) vs. Graphical (GUI)" footer="Both have their strengths; understanding core Git is key!" ~}
You have two main ways to interact with Git:

**1. Terminal / Command Line (CLI):**

* **Universally Available:** Works on all major operating systems (Windows, macOS, Linux).
* **Consistent Commands:** The Git commands you learn are the same everywhere.
* **Full Power & Control:** Provides access to all of Git's features and is great for scripting complex workflows.
* **Often Preferred by Pros:** Many experienced developers favor the CLI for its speed, precision, and efficiency.

**2. Graphical User Interface (GUI) Clients:**
  *(Examples: GitHub Desktop, Sourcetree, GitKraken, VS Code's integrated Git panel)*

* **Visual Interaction:** Offers a graphical way to see your repository's history, branches, and changes.
* **Potentially Easier for Beginners:** The visual nature can make initial Git concepts less intimidating for some.
* **Varying Feature Access:** While user-friendly, some GUIs might not expose all of Git's advanced commands or options directly.
* **Behind the Scenes:** GUI tools are essentially user-friendly interfaces that execute standard Git commands for you.
{~~}

---

# Recommended VS Code Extensions for Git

- Extensions enhance your Git workflow in VS Code
- Install from Extensions panel (Ctrl+Shift+X)
- These tools make Git more visual and intuitive
- Perfect for beginners learning Git concepts

{~ card title="Extension: GitLens" footer="A must-have VS Code extension for deeper Git insights!" ~}
GitLens is widely recognized as one of the most powerful and comprehensive Git extensions for Visual Studio Code. It dramatically enhances your ability to visualize, understand, and navigate your project's Git history.

**Key Features Include:**

* **Line-by-line Blame Annotations:** Instantly see who wrote or last changed any line of code and when, right in the editor.
* **Commit Search & Exploration:** Easily search, filter, and explore the commit history in various insightful ways.
* **File and Line History:** View the detailed evolution of any file or even specific lines of code over time.
* **Branch Comparison Tools:** Visually compare branches to understand differences and track changes effectively.
* **Revision Navigation:** Effortlessly jump between different versions (commits) of your files.
* **Interactive Rebase Editor:** Provides a powerful UI for more advanced operations like reordering, squashing, or editing commits (use with understanding, as it rewrites history!).

**Why It's So Useful:**
GitLens makes your Git repository's history and authorship incredibly transparent and accessible, all without leaving your code editor. This significantly boosts productivity and deepens your understanding of how your project has evolved.
{~~}

{~ card title="Extension: Git Graph" footer="See your branches and merges come to life!" ~}
Another invaluable VS Code extension for Git users is **Git Graph**. This tool excels at providing a clear, visual representation of your repository's commit history, branches, and merges.

**Key Features & Benefits:**

* **Graphical Git Log:** Transforms the often complex Git log into an easy-to-understand, interactive graph.
* **Clear Branch Visualization:** Instantly see how branches diverge, where they merge, and the overall structure of your development lines.
* **Tag Display:** Clearly indicates where tags are placed within your commit history.
* **Enhanced Understanding:** Makes it much simpler to grasp the flow of changes and the relationship between different commits, especially in projects with multiple contributors or complex branching strategies.
* **Repository Overview:** Provides a great bird's-eye view of your project's evolution.
* **Contextual Git Actions:** (For more advanced users) Allows performing some common Git actions directly from the graph.

**Why It's a Great Addition:**
Git Graph is particularly helpful for beginners and visual learners as it makes the abstract concepts of branches and merges much more tangible. It complements tools like GitLens by focusing on the graphical layout of your Git history.
{~~}

---

# Understanding GitHub

* Web-based platform built around Git
* Hosts repositories (projects)
* Adds collaboration features:
  * Issues and discussions
  * Pull requests
  * Project management tools
  * Code reviews
  * Actions (CI/CD)

---

# The Contribution Workflow

1. Find a project you want to contribute to
2. Fork the repository to your account
3. Clone your fork to your computer
4. Create a branch for your changes
5. Make and commit your changes
6. Push your branch to your fork
7. Create a pull request
8. Respond to feedback

---

# Authenticating with GitHub

* Git config only sets commit identity, not GitHub authentication
* When pushing/pulling, you'll need to authenticate:

* Option 1: HTTPS with Personal Access Token (PAT)
  * Generate token on GitHub (Settings → Developer settings → PAT)
  * First push will prompt for username and token
  * Can save credentials with:
    ```
    git config --global credential.helper store
    ```

* Option 2: SSH Keys (recommended)
  * Generate SSH key: `ssh-keygen -t ed25519 -C "your.email@example.com"`
  * Add to GitHub (Settings → SSH Keys)
  * Clone using SSH URL: `git clone git@github.com:YOUR_USERNAME/EduLite.git`

* Option 3: GitHub CLI
  * Install GitHub CLI and run: `gh auth login`

---

# Cloning Your Fork

* HTTPS method (requires PAT):
  ```
  git clone https://github.com/YOUR_USERNAME/EduLite.git
  ```

* SSH method (requires SSH key setup):
  ```
  git clone git@github.com:YOUR_USERNAME/EduLite.git
  ```

* After cloning, connect to original repo:
  ```
  cd EduLite
  git remote add upstream https://github.com/ibrahim-sisar/EduLite.git
  # or with SSH:
  git remote add upstream git@github.com:ibrahim-sisar/EduLite.git
  ```

---

# Working with Branches

* Branches isolate your changes from main code
* Never work directly on main/master branch
* Create a descriptive branch name:
  ```
  git checkout -b feature/login-page
  git checkout -b fix/broken-link
  git checkout -b docs/update-readme
  ```

* Check current branch:
  ```
  git branch
  ```

---

# Making Changes

* Edit files in your favorite code editor
* Create new files as needed
* Check which files you've changed:
  ```
  git status
  ```

* See specific changes:
  ```
  git diff
  ```

---

# Staging Changes

* Git requires a two-step commit process
* First "stage" the files you want to commit:
  ```
  git add filename.js          # Add specific file
  git add directory/           # Add all files in directory
  git add .                    # Add all changed files
  ```

* Check what's staged:
  ```
  git status
  ```

---

# Creating Commits

* Commits are snapshots of your changes
* Include a clear message explaining what changed
* Command:
  ```
  git commit -m "Add login form validation"
  ```

* Good commit messages:
  * Start with a verb (Add, Fix, Update)
  * Be specific but concise
  * Focus on "what" and "why", not "how"

---

# Commit Best Practices

* Make small, focused commits
* Each commit should do one logical change
* Write meaningful commit messages
* Make sure code works before committing
* Follow project commit guidelines if they exist

---

# Pushing Changes

* Upload your commits to GitHub
* First time pushing a branch:
  ```
  git push -u origin your-branch-name
  ```

* Subsequent pushes:
  ```
  git push
  ```

---

# Creating a Pull Request

* Formally requests project maintainers to review and merge your changes
* Steps:
  * Go to original repository on GitHub
  * Click "Pull requests" tab
  * Click "New pull request"
  * Select "compare across forks"
  * Select your fork and branch
  * Click "Create pull request"
  * Fill out the form with details

---

# Writing a Good PR Description

* Clearly explain what your changes do
* Reference any related issues: "Fixes #42"
* Include screenshots for UI changes
* Explain how to test your changes
* List any potential concerns or questions
* Thank maintainers for their time

---

# The Code Review Process

* Maintainers will review your code
* They may request changes
* Be responsive and open to feedback
* Make requested changes by:
  * Making new commits on your branch
  * Pushing them to your fork
  * PR updates automatically

---

# Updating Your PR

* If changes are requested:
  ```
  # Make your changes
  git add .
  git commit -m "Address review feedback"
  git push
  ```

* If main branch has changed:
  ```
  git fetch upstream
  git rebase upstream/main
  git push -f
  ```

---

# Handling Merge Conflicts

* Occur when two people change the same code
* Resolve locally before pushing:
  ```
  git fetch upstream
  git rebase upstream/main
  # Fix conflicts in your editor
  git add .
  git rebase --continue
  git push -f
  ```

---

# Git Command Cheat Sheet

* Setup: `git clone`, `git config`
* Check status: `git status`, `git log`, `git diff`
* Branches: `git branch`, `git checkout -b`, `git checkout`
* Changes: `git add`, `git commit`, `git push`
* Updates: `git fetch`, `git pull`, `git rebase`
* Problems: `git stash`, `git reset`, `git revert`

---

# GitHub Features for Contributors

* Issues: Find tasks to work on
* Projects: Track progress
* Discussions: Ask questions
* Actions: Automated testing
* Wiki: Project documentation
* Notifications: Stay updated
* Profile: Showcase your contributions

---

# Practical Exercise

* Fork the EduLite repository
* Clone your fork locally
* Create a branch for a simple change
* Make a small improvement (fix typo, update docs)
* Commit and push your changes
* Create your first pull request
* Experience the review process

---

# Contributing to EduLite

* Check the CONTRIBUTING.md file
* Look for issues labeled "good first issue"
* Join the Discord server for help
* Setup development environment per README
* Follow coding standards of the project
* Ask questions in GitHub Discussions

---

# Beyond Your First PR

* Keep your fork updated
* Tackle more complex issues
* Review other people's PRs
* Help with documentation
* Participate in discussions
* Share your experience with others

---

# Resources for Learning More

* Pro Git book (free online)
* GitHub Learning Lab
* Git documentation
* Stack Overflow
* YouTube tutorials
* Interactive learning: try.github.io
* Git Visualization tools

---

# Thank You!

* You're now ready to start contributing
* Remember: everyone was a beginner once
* The open source community welcomes you
* Your contributions matter
* Let's build something great together!