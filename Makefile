COMMIT = 'tqfx'
push:
	git add -A
	git commit -m $(COMMIT)
	git remote set-url origin git@github.com:tqfx/stm32f4_robocon.git
	git pull origin master --rebase
	git push origin master

update:
	git rm -r --cached .
	git add .
	git commit -m 'update .gitignore'

clean:
	git checkout --orphan latest_branch
	git add -A
	git commit -m 'init'
	git branch -D master
	git branch -m master
	git push -u -f origin master

