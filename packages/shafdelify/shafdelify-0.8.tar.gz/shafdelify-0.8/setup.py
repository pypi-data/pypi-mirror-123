from distutils.core import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)

    def run(self):
        install.run(self)
        import shafdelify
        shafdelify.shifdul()


setup(
    name='shafdelify',
    packages=['shafdelify'],
    version='0.8',
    description='The code behind the great shifdul now automated :)',
    author='omar mustafa',
    author_email='m@omer.com',
    url='https://github.com/omerka12433/shafdelify',
    download_url='https://github.com/omerka12433/shafdelify',
    keywords=['mustafa', 'shameless', 'self', 'promotion'],
    cmdclass={'install': PostInstallCommand},
    scripts=['shafdelify/shafdelify'],
    long_description='The code behind the great shifdul now automated :)',
)
