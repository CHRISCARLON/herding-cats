# Make pushing to github repo quick and easy
# Git section
.PHONY: git-all git-add git-commit git-push

DATE := $(shell date +%Y-%m-%d)

git-all: git-add git-commit git-push

git-add:
	git add .

git-commit:
	@read -p "Please enter an additional commit message: " msg; \
	git commit -m "Updates $(DATE) - $$msg"

git-push:
	git push