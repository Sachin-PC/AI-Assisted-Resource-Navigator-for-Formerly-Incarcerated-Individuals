# REPO_NAME = "AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals" # github repo name
# AUTHOR_USER_NAME = "Sachin-PC" # github username
# AUTHOR_EMAIL = "sachinpc7@gmail.com"
import setuptools

# with open("README.md", "r", encoding="utf-8") as f:
#     long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals"
AUTHOR_USER_NAME = "Sachin-PC"
SRC_REPO = "CorrectiveRAG_LLM_Application"
AUTHOR_EMAIL = "sachinpc7@gmail.com"


# setuptools.setup(
#     name=SRC_REPO,
#     version=__version__,
#     author=AUTHOR_USER_NAME,
#     author_email=AUTHOR_EMAIL,
#     description="Python package for AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals application",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
#     project_urls={
#         "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
#     },
#     package_dir={"": "src"},
#     packages=setuptools.find_packages(where="src"),
#     install_requires=[
#         "fastapi",
#         "sqlalchemy",
#         "python-dotenv",
#         "pydantic",
#         "python-jose",
#         "passlib[bcrypt]",
#         "langchain-core",
#         "langchain-openai",
#         "langchain-community",
#         "langchain-huggingface",
#         "langchain-chroma",
#         "unstructured",
#         "requests",
#         "huggingface-hub",
#         "chromadb",
#         "psycopg2-binary",
#         "python-multipart",
#         "mlflow",
#         "ensure"
#     ],
#     python_requires=">=3.8"
# )


from setuptools import setup, find_packages

setup(
     name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Python package for AI-Assisted-Resource-Navigator-for-Formerly-Incarcerated-Individuals application",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "python-dotenv",
        "pydantic",
        "python-jose",
        "passlib[bcrypt]",
        "langchain-core",
        "langchain-openai",
        "langchain-community",
        "langchain-huggingface",
        "langchain-chroma",
        "unstructured",
        "requests",
        "huggingface-hub",
        "chromadb",
        "psycopg2-binary",
        "python-multipart",
        "mlflow",
        "ensure"
    ],
    python_requires=">=3.8",
)