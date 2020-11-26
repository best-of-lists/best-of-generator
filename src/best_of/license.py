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
        "url": "https://tldrlegal.com/license/mit-license",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "Apache-2",
        "spdx_id": "Apache-2.0",
        "keywords": ["apache-2", "apache-license-2.0"],
        "url": "https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "ISC",
        "spdx_id": "ISC",
        "url": "https://tldrlegal.com/license/-isc-license",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "BSD-3",
        "spdx_id": "BSD-3-Clause",
        "keywords": ["bsd-3", "bds-3-clause"],
        "url": "https://tldrlegal.com/license/bsd-3-clause-license-(revised)",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "GPL-3.0",
        "spdx_id": "GPL-3.0",
        "keywords": ["gpl-3"],
        "url": "https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "GPL-2.0",
        "spdx_id": "GPL-2.0",
        "keywords": ["gpl-2"],
        "url": "https://tldrlegal.com/license/gnu-general-public-license-v2",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "MPL-2.0",
        "spdx_id": "MPL-2.0",
        "keywords": ["mpl-2"],
        "url": "https://tldrlegal.com/license/mozilla-public-license-2.0-(mpl-2)",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "BSD-2",
        "spdx_id": "BSD-2-Clause",
        "keywords": ["bsd-2", "freebsd", "bsd-2-Clause"],
        "url": "https://tldrlegal.com/license/bsd-2-clause-license-(freebsd)",
        "osi_approved": True,
        "warning": False,
    },
    {
        "name": "LGPL-3.0",
        "spdx_id": "LGPL-3.0",
        "keywords": ["lgpl-3"],
        "url": "https://tldrlegal.com/license/gnu-lesser-general-public-license-v3-(lgpl-3)",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "AGPL-3.0",
        "spdx_id": "AGPL-3.0",
        "keywords": ["agpl-3"],
        "url": "https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0)",
        "osi_approved": True,
        "warning": True,
    },
    {
        "name": "Unlicense",
        "spdx_id": "Unlicense",
        "url": "https://tldrlegal.com/license/unlicense",
        "osi_approved": False,
        "warning": False,
    },
    {
        "name": "EPL-2.0",
        "spdx_id": "EPL-2.0",
        "keywords": ["epl-2"],
        "url": "https://opensource.org/licenses/EPL-2.0",
        "osi_approved": True,
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
