# gym-update1

# To install
- git clone https://github.com/claudia-viaro/gym-update1.git
- cd gym-update1
- !pip install gym-update1
- import gym
- import gym_update
- env =gym.make('update-v0')

# To change version
- change version to, e.g., 1.0.7 from setup.py file
- git clone https://github.com/claudia-viaro/gym-update1.git
- cd gym-update1
- python setup.py sdist bdist_wheel
- twine check dist/*
- twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
