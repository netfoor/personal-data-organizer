from .script import get_extensions


print("Available file extensions:")
extensions = get_extensions()
print(extensions)

if __name__ == "__main__":
    get_extensions()
