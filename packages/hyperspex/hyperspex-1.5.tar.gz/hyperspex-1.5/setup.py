from setuptools import setup
import os
svg_files = ["hyperspex/gui/style/qdark/svg/"+file for file in list(os.walk("/Users/adrien/Documents/Software/hyperspex/hyperspex/gui/style/qdark/svg/"))[0][2]]
png_files = ["hyperspex/gui/style/qdark/"+file for file in list(os.walk("/Users/adrien/Documents/Software/hyperspex/hyperspex/gui/style/qdark/"))[0][2]]

setup(
    name='hyperspex',
    version='1.5',
    description='A Python package to help 3D hyperspectral data exploration through a Graphical User Interface.',
    url='https://github.com/AdrienR09/hyperspex',
    download_url='https://github.com/AdrienR09/hyperspex/archive/v_11.tar.gz',
    author='Adrien Rousseau',
    author_email='adrien.rousseau@umontpellier.fr',
    license='BSD 2-clause',
    packages=["hyperspex", "hyperspex.gui.style", "hyperspex.gui.colorbar", "hyperspex.gui.scientific_spinbox"],
    data_files=[('ui', ['hyperspex/gui/ui_spectrum_window.ui', 'hyperspex/gui/ui_image_window.ui',
                        'hyperspex/gui/colorbar/ui_colorbar.ui']),
                ('qss', ['hyperspex/gui/style/dracula.qss', 'hyperspex/gui/style/qdark.qss',
                        'hyperspex/gui/style/qtdark.qss']),
                ('png', png_files),
                ('svg', svg_files),
                ],
    include_package_data=True,
    install_requires=['mpi4py>=2.0',
                    'lmfit',
                    'scipy',
                    'despike',
                    'numpy',
                    'qtpy',
                    'pyqtgraph',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)