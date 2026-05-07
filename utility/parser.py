import re
from datetime import datetime
from enum import StrEnum
from typing import Generator, Iterable

from objects.guild import Guild


class FormatType(StrEnum):
    # fmt: off
    ID                  = "id"  # "123"
    NAME                = "name"  # "Name"
    DESCRIPTION         = "description"  # "This is a guild"
    ICON                = "icon"  # "https://images.com/icon/123"
    BANNER              = "banner"  # "https://images.com/banner/123"
    SPLASH              = "splash"  # "https://images.com/banner/123"
    DISCOVERY_SPLASH    = "discovery_splash"  # "https://images.com/banner/123"
    MFA_LEVEL           = "mfa_level"  # "<emoji>|mfa_level"
    VERIFICATION_LEVEL  = "verification_level"  # "<emoji>|verification_level"
    PREMIUM_LEVEL       = "premium_level"  # "<emoji>|premium_level"
    NSFW_LEVEL          = "nsfw_level"  # "<emoji>|nsfw_level"
    FEATURES            = "features"  # "[<features-1>]"
    APPROX_MEMBER       = "approx_member"  # "10"
    APPROX_PRESENCE     = "approx_presence"  # "12"
    ROLES               = "roles"  # "2"
    EMOJIS              = "emojis"  # "1"
    STICKERS            = "stickers"  # "12"
    CHANNELS            = "channels"  # "12"
    O_NAME              = "o_name"  # "IAmOwner"
    O_ID                = "o_id"  # "149"
    O_PRO               = "o_pro"  # "male|female"
    O_AVATAR            = "o_avatar"  # "https://images.com/avatar"
    O_BANNER            = "o_banner"  # "https://images.com/banner"
    O_BIO               = "o_bio"  # "MyselfOwnerPro"
    NOW                 = "now"  # "strftime(%Y-%m-%d %H:%M:%S%p)"
    # fmt: on


def make_values(guild: Guild) -> dict[FormatType, str]:
    # fmt: off
    values = {
        FormatType.NAME: guild.name,
        FormatType.ID: guild.id,
        FormatType.DESCRIPTION: guild.description,
        FormatType.ICON: str(guild.icon),
        FormatType.SPLASH: str(guild.splash),
        FormatType.DISCOVERY_SPLASH: str(guild.discovery_splash),
        FormatType.BANNER: str(guild.banner),

        FormatType.O_NAME: guild.owner.display_name,
        FormatType.O_ID: guild.owner.id,
        FormatType.O_PRO: guild.owner.pronoun,
        FormatType.O_AVATAR: str(guild.owner.avatar),
        FormatType.O_BANNER: str(guild.owner.banner),
        FormatType.O_BIO: guild.owner.bio,

        FormatType.APPROX_MEMBER: guild.approximate_member_count,
        FormatType.APPROX_PRESENCE: guild.approximate_presence_count,

        FormatType.EMOJIS: len(guild.emojis),
        FormatType.STICKERS: len(guild.stickers),

        FormatType.ROLES: len(guild.roles),
        FormatType.CHANNELS: len(guild.channels),

        FormatType.NSFW_LEVEL: str(guild.nsfw_level),
        FormatType.MFA_LEVEL: str(guild.mfa_level),
        FormatType.PREMIUM_LEVEL: str(guild.premium_level),
        FormatType.VERIFICATION_LEVEL: str(guild.verification_level),

        FormatType.FEATURES: guild.features,

        FormatType.NOW: datetime.now().strftime("%Y-%m-%d %H:%M:%S%p"),
    }
    # fmt: on

    return dict(map(lambda item: (item[0], str(item[1])), values.items()))


def parse_text(
    text: str,
) -> Generator[
    tuple[int, int, FormatType], None, Iterable[tuple[int, int, FormatType]]
]:
    # parse: %(FormatType.Attr.value)s
    pattern = re.compile(r"%\(([a-zA-Z_][a-zA-Z0-9_]*)\)s")
    matches: Iterable[tuple[int, int, FormatType]] = []

    for match in pattern.finditer(text):
        try:
            fmt = FormatType(match.group(1))
        except ValueError:
            continue

        result = (match.start(), match.end(), fmt)
        yield result

        matches.append(result)

    return matches
