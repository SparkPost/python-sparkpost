from distutils.version import StrictVersion

from django import get_version


def at_least_version(version):
    return StrictVersion(get_version()) > StrictVersion(version)
