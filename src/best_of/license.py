from typing import List, Optional

from addict import Dict

from best_of import utils

# Based on the most used open-source licenses:
# https://libraries.io/licenses
# https://spdx.org/licenses/
# https://tldrlegal.com/
# https://choosealicense.com/licenses/
# https://www.synopsys.com/blogs/software-security/top-open-source-licenses/
# https://opensource.org/licenses/alphabetical

# TODO add more
LICENSES: List[dict] = [
    {
        "name": "MIT",
        "spdx_id": "MIT",
        "keywords": ["mit-license"],
        "url": "http://bit.ly/34MBwT8",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "Apache-2",
        "spdx_id": "Apache-2.0",
        "keywords": ["apache-2", "apache-license-2.0"],
        "url": "http://bit.ly/3nYMfla",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "ISC",
        "spdx_id": "ISC",
        "url": "http://bit.ly/3hkKRql",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "BSD-3",
        "spdx_id": "BSD-3-Clause",
        "keywords": ["bsd-3", "bds-3-clause", "BSD-3.0-Clause"],
        "url": "http://bit.ly/3aKzpTv",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "GPL-3.0",
        "spdx_id": "GPL-3.0",
        "keywords": ["gpl-3", "gpl3", "gplv3", "gpl3.0"],
        "url": "http://bit.ly/2M0xdwT",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "GPL-2.0",
        "spdx_id": "GPL-2.0",
        "keywords": ["gpl-2"],
        "url": "http://bit.ly/2KucAZR",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "MPL-2.0",
        "spdx_id": "MPL-2.0",
        "keywords": ["mpl-2"],
        "url": "http://bit.ly/3postzC",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "BSD-2",
        "spdx_id": "BSD-2-Clause",
        "keywords": ["bsd-2", "freebsd", "bsd-2-Clause"],
        "url": "http://bit.ly/3rqEWVr",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "LGPL-3.0",
        "spdx_id": "LGPL-3.0",
        "keywords": ["lgpl-3"],
        "url": "http://bit.ly/37RvQcA",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "AGPL-3.0",
        "spdx_id": "AGPL-3.0",
        "keywords": ["agpl-3"],
        "url": "http://bit.ly/3pwmjO5",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "Unlicense",
        "spdx_id": "Unlicense",
        "url": "http://bit.ly/3rvuUlR",
        "osi_approved": False,
        "warning": False,
    },
    {
        "name": "EPL-2.0",
        "spdx_id": "EPL-2.0",
        "keywords": ["epl-2"],
        "url": "http://bit.ly/2M0xmjV",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "CC-BY-SA-4.0",
        "spdx_id": "CC-BY-SA-4.0",
        "keywords": ["CC-BY-SA-4.0 License"],
        "url": "http://bit.ly/3mSooSG",
        "osi_approved": False,
        "warning": False,
    },
    {
        "name": "Python-2.0",
        "spdx_id": "PSF-2.0",
        "keywords": ["Python License 2.0", "PSF-2", "Python-2"],
        "url": "http://bit.ly/35wkF7y",
        "osi_approved": False,
        "warning": False,
    },
]


def get_license(query: str) -> Optional[Dict]:
    licenses_map = {}
    for license in LICENSES:
        licenses_map[utils.simplify_str(license["name"])] = license
        licenses_map[utils.simplify_str(license["spdx_id"])] = license
        if "keywords" in license:
            for keyword in license["keywords"]:
                licenses_map[utils.simplify_str(keyword)] = license
    query = utils.simplify_str(query)
    if query not in licenses_map:
        return None

    return Dict(licenses_map[query])
