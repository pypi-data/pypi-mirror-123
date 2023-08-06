from LbPlatformUtils import requires
from LbPlatformUtils.architectures import ARCH_DEFS, get_supported_archs
from LbPlatformUtils.inspect import architecture


def archs():
    return list(get_supported_archs(ARCH_DEFS[architecture()]))


def required(platform):
    return requires(platform).split("-")[0]
