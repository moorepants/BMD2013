These are the instructions for generating the tables and plots.

$ mkvirtualenv bicycle

Start by installing stuff from the SciPy stack (make sure you have all of the
dependencies to build the packages)::

   (bicycle)$ pip install numpy
   (bicycle)$ pip install scipy
   (bicycle)$ pip install "numexpr<2.0"
   (bicycle)$ pip install "tables<3.0"

Be sure to do this after installing NumPy because matplotlibi is not very pip
friendly::

   (bicycle)$ pip install matplotlib

Get the latest yeadon (I could probably just pip install this one). Don't worry
about yeadon's optional dependencies because I'm only using the API::

   (bicycle)$ git clone git@github.com:chrisdembia/yeadon.git
   (bicycle)$ cd /yeadon
   (bicycle)$ python setup.py develop
   (bicycle)$ cd ..

pip install yeadon==1.0.2

Maybe add tags to my packages to correspond to this study.

Get the lasted DynamicistToolKit::

   (bicycle)$ git clone git@github.com:moorepants/DynamicistToolKit.git
   (bicycle)$ cd DynamicistToolKit
   (bicycle)$ python setup.py develop
   (bicycle)$ cd ..

Get the latest DynamicistToolKit::

   (bicycle)$ git clone git@github.com:moorepants/BicycleParameters.git
   (bicycle)$ cd BicycleParameters
   (bicycle)$ python setup.py develop
   (bicycle)$ cd ..

Get the lasted AutolevToolKit::

   (bicycle)$ git clone git@github.com:moorepants/AutolevToolKit.git
   (bicycle)$ cd AutolevToolKit
   (bicycle)$ python setup.py develop

Get the lasted BicycleDataProcessor::

   (bicycle)$ git clone git@github.com:moorepants/BicycleDataProcessor.git
   (bicycle)$ cd ~/src/BicycleDataProcessor
   (bicycle)$ python setup.py develop

Get the lasted CanonicalBicycleID::

   (bicycle)$ git clone git@github.com:moorepants/CanonicalBicycleID.git
   (bicycle)$ cd ~/src/CanonicalBicycleID
   (bicycle)$ python setup.py develop

Your environment should be::

   $ pip freeze
   -e git+git@github.com:moorepants/BicycleDataProcessor.git@cf37d7633b2e64a3d02d63a43ab193ec736796bc#egg=BicycleDataProcessor-dev
   -e git+git@github.com:moorepants/BicycleParameters.git@526b7314e42c161a4f60a9bf2718ff3dbad89007#egg=BicycleParameters-dev
   -e git+git@github.com:moorepants/CanonicalBicycleID.git@d0eaf45a279d52173a46934faeee30585d88ae43#egg=CanonicalBicycleID-dev
   Cython==0.19.1
   -e git+git@github.com:moorepants/DynamicistToolKit.git@78892454c4783698ae20fa619330d97cc5661135#egg=DynamicistToolKit-dev
   PyYAML==3.10
   argparse==1.2.1
   matplotlib==1.3.0
   nose==1.3.0
   numexpr==2.2.1
   numpy==1.7.1
   pyparsing==2.0.1
   python-dateutil==2.1
   scipy==0.12.0
   six==1.4.1
   tables==2.4.0
   tornado==3.1.1
   uncertainties==1.9.1
   wsgiref==0.1.2
   -e git+git@github.com:fitze/yeadon.git@8db10fbc1704711464ab08d8ee02d8821b9cc4e2#egg=yeadon-dev

Get the data!
TODO : add data instructions

Get the source::

   (bicycle)$ git clone git@github.com:moorepants/BMD2013.git
   (bicycle)$ cd whipple-id/paper/src
   (bicycle)$ python identify.py

This will generate three files in the data directory.
