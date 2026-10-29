# Environment setup

1. Install rbenv and ruby-build. rbenv manages and switches between Ruby
versions. ruby-build downloads and compiles the actual Ruby source code
from the internet so it can be installed on your machine.

```bash
brew install rbenv ruby-build
```

2. Initialize rbenv in your shell configuration file (e.g., ~/.zshrc).
The `rbenv init -` command adds shims to PATH. It injects rbenv's shim
directory (a folder of wrapper scripts) into your system PATH. When you
run a command like ruby or gem, your shell hits the rbenv shim first
instead of a global system Ruby.

```bash
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(rbenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

3. Install and Set a Specific Ruby Version, and verify your active Ruby path

```bash
rbenv install 3.1.6
rbenv global 3.1.6
which ruby
```

4. Install Jekyll and Bundler and verify that Jekyll is running from the correct rbenv shim.
Jekyll is a static site generator which takes plain text files written in Markdown, and
transforms them into a complete, ready-to-serve static website. Bundler is a Ruby dependency
manager that manages Ruby packages (or "gems") for your project: A Gemfile defines your
project dependencies and general version constraints, while the Gemfile.lock records the
exact versions of those dependencies that were actually installed.

```bash
gem install jekyll bundler
jekyll --version
```

5. Navigate to your repo folder, install the dependencies locally into the project,
iand launch the local development server.

```bash
bundle install
bundle exec jekyll serve
```

6. Open your browser and navigate to `http://localhost:4000/tsvd` to view and test your
GitHub Pages blog live

