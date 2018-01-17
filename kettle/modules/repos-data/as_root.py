import sys

from kettle.ket import Kettle
from kettle.modules.repos import Repos

kettle = Kettle(sys.argv[1])
repo = Repos(kettle)
repos = repo.get_ppas()
repo.install_repos(repos)

