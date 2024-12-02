DATE := $(shell date +%Y-%m-%d)
VENV_PATH := .venv

define COMMIT_TYPES
feat:     A new feature
fix:      A bug fix
docs:     Documentation only changes
style:    Changes that do not affect the meaning of the code
refactor: A code change that neither fixes a bug nor adds a feature
perf:     A code change that improves performance
test:     Adding missing tests or correcting existing tests
build:    Changes that affect the build system or external dependencies
ci:       Changes to CI configuration files and scripts
chore:    Other changes that don't modify src or test files
revert:   Reverts a previous commit
endef
export COMMIT_TYPES

# Local development commands
.PHONY: dev ruff-watch dev-kill

dev:
	@if [ -z "$$TMUX" ]; then \
		tmux new-session -d -s herding-cats; \
		tmux send-keys 'cd $(shell pwd)' C-m; \
		tmux split-window -v -p 15; \
		tmux send-keys 'cd $(shell pwd) && source .venv/bin/activate && make ruff-watch' C-m; \
		tmux select-pane -t 0; \
		tmux send-keys 'source .venv/bin/activate' C-m; \
		tmux attach-session -t herding-cats; \
	else \
		tmux split-window -v -p 15 'source .venv/bin/activate && make ruff-watch'; \
		tmux select-pane -t 0; \
	fi

ruff-watch:
	@echo "Starting Ruff in watch mode..."
	@ruff check --watch .

dev-kill:
	@echo "Killing HerdingCats dev session"s
	tmux kill-session -t herding-cats

# Git commands
update: git-add git-commit git-push

git-add:
	git add .

git-commit:
	@echo "Available commit types:"
	@echo "$$COMMIT_TYPES" | sed 's/^/  /'
	@echo
	@read -p "Enter commit type: " type; \
	if echo "$$COMMIT_TYPES" | grep -q "^$$type:"; then \
		read -p "Enter commit scope (optional, press enter to skip): " scope; \
		read -p "Is this a breaking change? (y/N): " breaking; \
		read -p "Enter commit message: " msg; \
		if [ "$$breaking" = "y" ] || [ "$$breaking" = "Y" ]; then \
			if [ -n "$$scope" ]; then \
				git commit -m "$$type!($$scope): $$msg [$(DATE)]" -m "BREAKING CHANGE: $$msg"; \
			else \
				git commit -m "$$type!: $$msg [$(DATE)]" -m "BREAKING CHANGE: $$msg"; \
			fi; \
		else \
			if [ -n "$$scope" ]; then \
				git commit -m "$$type($$scope): $$msg [$(DATE)]"; \
			else \
				git commit -m "$$type: $$msg [$(DATE)]"; \
			fi; \
		fi; \
	else \
		echo "Invalid commit type. Please use one of the available types."; \
		exit 1; \
	fi

git-push:
	git push
