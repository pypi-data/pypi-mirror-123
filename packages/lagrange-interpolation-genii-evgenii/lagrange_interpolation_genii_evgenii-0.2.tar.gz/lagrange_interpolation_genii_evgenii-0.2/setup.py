# Импорт недавно установленного пакета setuptools.
import setuptools

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    name='lagrange_interpolation_genii_evgenii',
    version='0.2',
    author='Borodin Evgenii',
    author_email='j.borodin1@gmail.com',
    description='Lagrange interpolation package',
    url='https://www.instagram.com/eug_borodin/',
    long_description=long_description,
    packages=['lagrange_interpolation'],
    # Определяет тип контента, используемый в long_description.
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # Требуемая версия Python.
    python_requires='>=3.6'
)
