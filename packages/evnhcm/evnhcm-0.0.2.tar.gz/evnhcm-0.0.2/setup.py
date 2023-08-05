from distutils.core import setup
setup(
    name = 'evnhcm',         # How you named your package folder (MyLib)
    packages = ['evnhcm'],   # Chose the same as "name"
    version = '0.0.2',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Lấy thông tin điện lực HCM',   # Give a short description about your library
    long_description= 'Lấy thông tin điện lực HCM dùng cho Hassio (Home Assistant)',
    author = 'Xuong Huynh',                   # Type in your name
    author_email = 'longxuongz@gmail.com',      # Type in your E-Mail
    keywords = ['evn', 'hcm', 'evnhcm'],   # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)