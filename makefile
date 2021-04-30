all : py git pip

py :
	python increaseVersionSetup.py
	rm -rf build dist
	python setup.py sdist bdist_wheel
	python -m twine upload  dist/*

git :
	git commit -am 'update pypi package'
	git push origin master

pip :
	pip install --upgrade OarLauncher
	echo "run 'pip install --upgrade OarLauncher'"
