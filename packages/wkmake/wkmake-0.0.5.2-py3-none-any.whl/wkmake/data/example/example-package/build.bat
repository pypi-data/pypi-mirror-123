rmdir /S /Q  dist build {{pkg_name}}.egg-info
python3 setup.py sdist bdist_wheel