from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='minuteinbox-py',
  version='0.4',
  description='Create temporary E-Mails & receive E-Mails with MinuteInbox through python',
  long_description=open('README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/Avnsx/MinuteInbox-Temporary-E-Mail',  
  author='Mika C',
  author_email='AvnDev@protonmail.com',
  py_modules=['minuteinbox'],
  license='MIT',
  classifiers=classifiers,
  keywords='email, minuteinbox, temporary, disposable, spam, mail, 10 minute, python email,', 
  packages=find_packages(),
  install_requires=['bs4','requests',] 
)
