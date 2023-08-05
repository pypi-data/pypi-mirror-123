py setup.py sdist
twine upload dist/*
twine upload dist/* --skip-existing  --config-file .pypirc


pipreqs ./ --encoding=utf8 --force

pip install -r requirements.txt
