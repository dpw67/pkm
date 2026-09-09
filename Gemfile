# Gems for building this site locally.
#
# GitHub Pages does not read this file -- the classic branch build resolves its
# own gem set -- so it exists only to reproduce that build here, where a mistake
# can still be caught. Pushing to `main` publishes, with nothing in between.
#
# The pins mirror what Pages actually runs, reported at
# https://pages.github.com/versions/: Ruby 3.3.4, Jekyll 3.10.0,
# github-pages 232, jekyll-theme-primer 0.6.0. Re-read that page before bumping.
source "https://rubygems.org"

# macOS ships Ruby 2.6, which cannot resolve this gem set. Declared so bundler
# says exactly that instead of failing somewhere deep in dependency resolution.
ruby "~> 3.3"

gem "github-pages", "~> 232"

# Arrives through github-pages, which pins it to 0.6.0. Named anyway, because
# _config.yml depends on it for the `default` layout -- the theme is a
# dependency of the site, not an implementation detail of the gem above.
gem "jekyll-theme-primer", "~> 0.6"

# Left the standard library in Ruby 3.0, and Jekyll 3.10's `serve` still expects
# it. Without this, `make serve` dies on a missing require.
gem "webrick", "~> 1.8"
