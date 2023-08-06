import sys

from importlib_metadata import distributions

class Dist:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def get_installed_distributions():
    return(
        [Dist(project_name=it.metadata["Name"], version=it.version, check_version_conflict=(lambda: None))
            for it in distributions()
        ]
    )

def gather_libraries(*args, **kwargs):
    pkgs = get_installed_distributions()

    return (
        True, {
            'libraries': {
                x.project_name: {
                    'version': x.version,
                    'conflicts': x.check_version_conflict()
                } for x in pkgs
            }
        }
    )


def gather_python(*args, **kwargs):
    return (True, {
        'python': sys.version_info
    })


if __name__ == '__main__':
    import json

    print(json.dumps(gather_libraries(), indent=4))
