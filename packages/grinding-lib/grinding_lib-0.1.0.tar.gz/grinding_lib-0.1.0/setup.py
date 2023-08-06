from setuptools import setup, find_packages

setup(
    name='grinding_lib',
    version='0.1.0',
    description='Demo Python Library for Siemens Grinding project',
    long_description=" In-house Python Library built to be used for Siemens Grinding project",
    long_description_content_type="text/markdown",
    author='Me',
    license='DPA',
    packages=["grinding_lib"],
    include_package_data=True,
    install_requires=["time",
                      "numpy", "pandas", "sklearn", "h5py", "tqdm", "os", "tensorflow", "matplotlib", "keras",
                      "librosa", "scipy", "gc", "joblib", "re", "seaborn", "pyAudioAnalysis", "statistics",
                      "soundfile", "shutil", "sound_waves", "sys", "warnings"]
)


