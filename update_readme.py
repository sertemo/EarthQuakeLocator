"""Actualiza en el README la versión"""

import toml


def update_readme():
    # Leer la configuración del proyecto
    with open("pyproject.toml", "r") as file:
        data = toml.load(file)
        project_version = data["tool"]["poetry"]["version"]

    # Leer el contenido actual de README.md y actualizar
    with open("README.md", "r") as file:
        readme_contents = file.readlines()

    # La versión está en la segunda fila
    readme_contents[1] = f"### Version: {project_version}\n"

    # Escribir el contenido actualizado de nuevo a README.md
    with open("README.md", "w") as file:
        file.writelines(readme_contents)


if __name__ == "__main__":
    update_readme()
