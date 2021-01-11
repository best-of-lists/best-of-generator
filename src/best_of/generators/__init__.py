from typing import List, Optional

from best_of import utils
from best_of.generators import base_generator, markdown_list

AVAILABLE_GENERATORS: List[base_generator.BaseGenerator] = [
    markdown_list.MarkdownListGenerator()
]


def get_generator(name: str) -> Optional[base_generator.BaseGenerator]:

    generator_dict = {
        utils.simplify_str(generator.name): generator
        for generator in AVAILABLE_GENERATORS
    }

    if utils.simplify_str(name) in generator_dict:
        return generator_dict[utils.simplify_str(name)]

    return None
