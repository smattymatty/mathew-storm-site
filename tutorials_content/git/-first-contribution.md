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

## Getting Started with Git & GitHub for Beginners 🚀

This guide helps new contributors learn about open source, Git, and GitHub, so you can make your first contribution.

{~ alert type="success" ~}
**Welcome to your First Contribution Guide!**
This guide will help you get started with Git and GitHub, and make your first contribution to open source projects.

We specifically cover the EduLite project, which is a great example of a project that welcomes new contributors.

You can use this information to learn more about Git and GitHub, and to contribute to open source projects in general.

If you choose to contribute to EduLite, you'll be making your first contribution to a real-world project and your work will be recognized and appreciated by the community.
{~~}

---

### What you need to get started (Requirements)

* A GitHub account (if you don't already have one)
* A text editor or IDE (preferably VS Code for this tutorial)
* The technical skills to install Git on your operating system

{~ alert type="info" ~}
**Note:** This tutorial is designed for beginners who are new to Git and GitHub.
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
* **Standard GitHub steps:**
    1.  **Fork:** Make a personal copy of a project on GitHub.
    2.  **Clone:** Download your forked project to your computer.
    3.  **Branch:** Create a new branch for your changes (e.g., a new feature or bug fix).
    4.  **Push:** Upload your changes from your computer to your fork on GitHub.
    5.  **Pull Request (PR):** Propose your changes to the original project.
* **Benefits:** This process allows for clear discussion, code review, and organized contributions, especially for remote teams.

---

### Making Your First Pull Request (PR) 🎉

* **What a Pull Request is:** Your formal way to ask the project owners to include your improvements.
* **Why it's a big deal:** It shows you can use Git and GitHub and is your first step into open source.
* **What you'll learn here:** How to find suitable tasks (like "good first issues"), make your changes, and confidently submit your first contribution to projects like EduLite.

---

# Why Learn Git & GitHub?

* **Essential skill for all developers:**
    * In today's software development landscape, proficiency in Git and GitHub is as fundamental as knowing a programming language. It's the bedrock for managing code changes efficiently, whether you're working on a small personal project or as part of a large distributed team.
    * Understanding version control with Git allows you to experiment fearlessly, track your project's evolution, and pinpoint when and where changes were made, saving you countless hours and potential headaches.
    * Many modern development practices and tools, such as Continuous Integration/Continuous Deployment (CI/CD) pipelines, are built around Git workflows.

* **Industry standard for version control:**
    * Git has overwhelmingly become the standard for version control across the tech industry, replacing older systems. Its distributed nature, powerful branching and merging capabilities, speed, and strong community support have led to its widespread adoption.
    * This means that regardless of the company size, programming language, or type of project, you'll almost certainly encounter Git and a platform like GitHub. Knowing it makes you instantly more adaptable and employable.

* **Required for collaborative projects:**
    * Git and GitHub are designed for teamwork. They provide the mechanisms for multiple developers to work on the same project simultaneously without stepping on each other's toes. Features like branches allow for isolated development of new features or fixes, while Pull Requests on GitHub facilitate code reviews and discussions before changes are merged into the main codebase.
    * Without robust version control, collaborative efforts can quickly descend into chaos with conflicting file versions, overwritten work, and a lack of clear history, making platforms like GitHub indispensable for projects like EduLite that rely on community contributions.

* **Helps build your developer portfolio:**
    * Your GitHub profile acts as a dynamic, living resume and portfolio. By hosting your projects (even small ones or course assignments) on GitHub and making contributions to other open source projects, you create a tangible record of your coding skills, your learning journey, and your ability to work with version control.
    * Potential employers and collaborators can see not just the final product, but also the process, the quality of your commits, and how you interact within a development environment.

* **Shows your code to potential employers:**
    * Many recruiters and hiring managers actively use GitHub to find and assess candidates. A public GitHub profile gives them direct insight into your practical coding abilities, problem-solving skills, and attention to detail in a way that a traditional resume cannot.
    * Well-commented code, clear commit messages, thoughtful Pull Request descriptions, and contributions to existing projects (like EduLite!) can significantly strengthen your profile and demonstrate your passion for development and collaboration.

---

# What We'll Cover

* **Setting up Git on your computer:**
    * This is the essential first step. Once you have git installed on your operating system, you will be ready for this course. We will share links and commands for installation.
    * You'll also learn how to perform initial configurations, such as setting your `user.name` and `user.email`, which are important for identifying your contributions.
    * We'll touch upon using Git via the command line and briefly introduce how it integrates with popular code editors like VS Code.

* **Understanding key Git concepts:**
    * Beyond just commands, we'll help you build a solid mental model of how Git works. This understanding is crucial for using Git effectively and troubleshooting any issues.
    * We'll cover fundamental ideas like what a repository (repo) is, the difference between your working directory and the staging area (index), the significance of commits as snapshots in time, the power of branches for parallel work, what HEAD signifies, and how local and remote repositories interact in a distributed system.

* **Forking and cloning repositories:**
    * Learn the concept of "**forking**" – creating your own server-side copy of a project (like EduLite on GitHub). This gives you a space to experiment and prepare your changes without affecting the original project directly.
    * We'll then cover "**cloning**," which is how you bring that forked repository (or any remote repository) down to your local machine so you can work on the files. You'll get comfortable with the `git clone` command.

* **Creating branches for your work:**
    * Discover the power of **branches** as independent lines of development within your repository.
    * Understand why it's a best practice to **create a new branch** for every new feature, bug fix, or piece of work. This keeps your changes organized, isolates them from the main codebase (often called `main` or `master`), and makes collaboration much smoother.
    * We’ll practice creating, switching between, and managing branches using commands like `git branch` and `git checkout` (or `git switch`).

* **Making commits with good messages:**
    * A "commit" is how you save your work in Git, creating a snapshot of your project at a specific point. We'll cover the two-step process: staging changes with `git add` and then committing them with `git commit`.
    * Crucially, we'll emphasize the art of writing clear, concise, and informative commit messages. Good messages are vital for understanding the project's history, helping collaborators (and your future self!), and making debugging easier.

* **Creating pull requests:**
    * Once you've pushed your committed changes to your fork on GitHub, the next step for contributing to a project like EduLite is creating a Pull Request (PR).
    * A PR is a formal proposal to merge the changes from your branch into the original project's main branch. It's the central hub for discussion, code review, and automated checks before your contributions are integrated. We'll show you how to initiate and describe your PRs effectively on GitHub.

* **Responding to code reviews:**
    * After submitting a Pull Request, project maintainers or other contributors will likely review your code. This is a valuable part of the open source process, designed to improve code quality, catch potential issues, share knowledge, and ensure consistency.
    * We'll discuss how to receive feedback constructively, ask for clarifications if needed, and make further changes to your PR by adding new commits and pushing them to the same branch.

* **Contributing to real projects:**
    * This is where all the pieces come together! We'll guide you on how to apply this entire workflow to make actual contributions, using EduLite as our primary example.
    * You'll learn how to find beginner-friendly tasks (like those often labeled "good first issue"), make your changes, and go through the full cycle of submitting a contribution, empowering you to participate in any open source project.

---

# About Our Example Project: EduLite

* Student-first learning platform
* Built for areas with weak internet
* 100% volunteer-driven open source project
* Perfect for your first contribution
* Includes both frontend and backend opportunities

---

# Getting Started with Git

* **Git is a distributed version control system:**
    * A Version Control System (VCS) is a tool that helps you manage and track changes to your project's files over time. Think of it as a "save" button for your entire project, but with the ability to go back to previous saves, see who changed what, and work on different versions simultaneously.
    * The "distributed" part is key: unlike older centralized systems where the entire project history is stored on a single server, Git gives every developer a full, independent copy of the project's history on their local machine. This means more flexibility, speed, and resilience, as you're not always reliant on a central server.

* **Tracks changes to files over time:**
    * Git meticulously records every modification you make to your project's files – whether you're adding new code, changing existing lines, or deleting something. It does this by taking snapshots of your entire project at points you define (called "commits").
    * This tracking is incredibly beneficial because it allows you to look back at the history, see exactly what changed between versions, revert to a previous stable state if something goes wrong, and understand how your project has evolved. It's primarily optimized for text files like source code but can manage other file types too.

* **Allows multiple people to work together:**
    * Git is designed from the ground up for collaboration. It provides powerful tools like "branching," which lets developers work on different features or fixes in isolation without interfering with each other or the main codebase.
    * Once individual work is complete, Git offers mechanisms for "merging" these different lines of development back together. It even helps identify and resolve "merge conflicts" that can occur if different people have modified the same part of a file. This is essential for team projects and open-source contributions like those for EduLite.

* **Maintains history of all changes:**
    * Every time you save a snapshot of your work (a "commit"), Git stores it along with important metadata: who made the change, when it was made, and, crucially, a message describing *why* the change was made.
    * This comprehensive history is invaluable. It allows you to understand past decisions, pinpoint when bugs were introduced (using tools like `git bisect`), audit changes, and confidently revert to any previous version of your project if needed. This entire history is typically stored in a hidden `.git` directory within your project.

* **Works offline (most operations are local):**
    * Because Git is distributed and you have a full copy of the repository history on your computer, most of the operations you'll perform—like creating branches, making commits, viewing your project's history, or comparing versions—are done locally and are incredibly fast.
    * This means you can be fully productive even without an internet connection, which is a huge advantage for developers on the go or in environments with unreliable connectivity (a consideration relevant to EduLite's mission). You only need an internet connection when you're ready to share your changes with others (by "pushing" to a remote repository like GitHub) or get the latest updates from them ("pulling").

---

# Git Across Different Operating Systems

* **Git installation varies by OS:**
    * Getting Git onto your computer is the first hands-on step, and the method differs slightly based on your operating system. We'll guide you through the most common ways:
    * **Windows:** The most straightforward method is typically to download the official installer directly from the [Git SCM website (https://git-scm.com/downloads/win)](https://git-scm.com/downloads/win). This installer often includes "Git Bash," a terminal environment that provides a Linux-like command-line experience for using Git on Windows.
    * **Mac:** If you use Homebrew (a popular package manager for macOS), installing Git can be as simple as running the command `brew install git`. Alternatively, installers are also available, sometimes bundled with Xcode developer tools or directly from the [Git SCM website (https://git-scm.com/downloads/mac)](https://git-scm.com/downloads/mac).
    * **Linux:** Installation is typically handled through your distribution's built-in package manager. For example:
        * On **Ubuntu/Debian** based systems, you'll use `sudo apt install git`.
        * On **Fedora**, the command is `sudo dnf install git`.
        * On **Arch Linux**, you would use `sudo pacman -S git`.

* **Good news: Once installed, Git commands are identical across all platforms:**
    * This is a fantastic aspect of Git! While the initial setup might differ, the core Git commands you will learn and use (`git commit`, `git branch`, `git checkout`, `git push`, `git pull`, etc.) are exactly the same whether you're on Windows, macOS, or any Linux distribution.
    * This universality means the skills you develop are highly transferable, and you can collaborate seamlessly with others who might be using different operating systems.

* **All terminal commands in this course work the same on Windows, Mac, and Linux:**
    * To ensure a consistent learning experience, this course will focus on these universal Git commands as executed in a terminal or command-line interface.
    * While the terminal application itself might have a different name or appearance (e.g., Git Bash or PowerShell on Windows, Terminal on macOS, various terminal emulators on Linux), the underlying Git commands you type and their behavior will be consistent with what's taught.

* **GUI clients available for all platforms if preferred:**
    * If you're not entirely comfortable with the command line, or if you prefer a more visual way to interact with Git, there's good news: numerous Graphical User Interface (GUI) clients are available for all major operating systems. These tools provide a visual interface for Git operations.
    * While these GUI clients can be helpful, especially for visualizing branches and history, this course will primarily focus on the command-line interface to ensure you build a fundamental understanding of Git's operations, which are consistent everywhere.

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

---

# Configuring Git in VS Code

* **Set your identity (used in commits):**
    * Before you start making commits (saving your work), you need to tell Git who you are. This identity (your name and email address) will be embedded in every commit you create, making it clear who made which changes in the project's history.
    * You'll do this using the `git config` command with the `--global` flag, which means these settings will apply to all Git projects on your computer.
    * The commands are straightforward:
        ```
        git config --global user.name "Your Name"
        git config --global user.email "your.email@example.com"
        ```
    * Be sure to replace `"Your Name"` and `"your.email@example.com"` with your actual name and the email address you want associated with your commits (often the one linked to your GitHub account).

* **Verify your settings:**
    * After setting your identity, it's a good practice to verify that the configuration was applied correctly.
    * You can easily check your global Git settings by running:
        ```
        git config --global --list
        ```
    * This command will display all your global Git configurations, and you should see the `user.name` and `user.email` you just set, among other potential settings. This confirms Git knows who you are for future commits.

* **VS Code authentication benefits:**
    * Visual Studio Code (VS Code) has excellent built-in integration with Git and GitHub, which can significantly simplify how you authenticate with remote services like GitHub.
    * **Automatically prompts for GitHub login on first push:**
        * When you're ready to "push" (upload) your local commits to a remote repository on GitHub for the first time, VS Code can automatically detect this and prompt you to log in to GitHub. This often streamlines the initial authentication process, especially when using HTTPS.
    * **Securely stores credentials:**
        * Instead of you having to re-enter your username and password (or Personal Access Token) repeatedly, VS Code can securely store these credentials for you, typically by leveraging your operating system's keychain or other secure storage mechanisms.
    * **Handles token refresh automatically:**
        * Access tokens used for authentication (especially those obtained via OAuth through VS Code's GitHub extension) can expire. VS Code's integration can often handle the process of refreshing these tokens automatically in the background, ensuring you maintain uninterrupted access to your remote repositories.
    * **Supports multiple accounts:**
        * If you work with multiple GitHub accounts (for example, a personal account and a work or school account), VS Code's GitHub integration is designed to support this, allowing you to authenticate and switch between different accounts as needed for different projects or workspaces.

---

# VS Code's Git Integration Features

* Source Control tab (Ctrl+Shift+G)
* Status indicators in file explorer
* Built-in diff viewer
* Inline blame annotations with GitLens
* Commit staging with checkboxes
* Branch switching from status bar
* Conflict resolution helpers
* Terminal access for advanced commands

---
# Git Terminal vs. GUI Clients

* Terminal/Command Line:
  * Available on all platforms
  * Consistent across systems
  * Full access to all Git features
  * Preferred by many professionals

* GUI Clients (GitHub Desktop, GitKraken, etc.):
  * More visual interface
  * Easier for beginners
  * May hide some advanced features
  * This course focuses on terminal commands for consistency

---

# Configuring Git

* Set your identity (used in commits):
  ```
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

* Verify your settings:
  ```
  git config --global --list
  ```

---

# Recommended VS Code Extensions for Git

- Extensions enhance your Git workflow in VS Code
- Install from Extensions panel (Ctrl+Shift+X)
- These tools make Git more visual and intuitive
- Perfect for beginners learning Git concepts

---

# Extension: GitLens

* The most comprehensive Git extension
* Features:
  * Line-by-line blame annotations
  * Commit search and exploration
  * File and line history
  * Branch comparison
  * Revision navigation
  * Interactive rebase editor

* Why it's useful: Makes Git history and authorship visible within your code

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

# Cloning Your Fork (Updated)

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