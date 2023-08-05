import copy
from typing import Dict


def to_raw(metadata: Dict) -> Dict:
    raw_metadata = copy.copy(metadata)
    for idx, region in raw_metadata['inputs'].items():
        for name, _ in region.items():
            raw_metadata['inputs'][idx][name]['user_shape'] = raw_metadata['inputs'][idx][name]['tpu_shape']
            raw_metadata['inputs'][idx][name]['user_order'] = raw_metadata['inputs'][idx][name]['tpu_order']
            raw_metadata['inputs'][idx][name]['user_dtype'] = raw_metadata['inputs'][idx][name]['tpu_dtype']
            raw_metadata['inputs'][idx][name]['scales'] = [1.0, ]
            raw_metadata['inputs'][idx][name]['padding'] = \
                [[0, 0], ] * len(raw_metadata['inputs'][idx][name]['tpu_shape'])

    for idx, region in raw_metadata['outputs'].items():
        for name, _ in region.items():
            raw_metadata['outputs'][idx][name]['user_shape'] = raw_metadata['outputs'][idx][name]['tpu_shape']
            raw_metadata['outputs'][idx][name]['user_order'] = raw_metadata['outputs'][idx][name]['tpu_order']
            raw_metadata['outputs'][idx][name]['user_dtype'] = raw_metadata['outputs'][idx][name]['tpu_dtype']
            raw_metadata['outputs'][idx][name]['scales'] = [1.0, ]
            raw_metadata['outputs'][idx][name]['padding'] = \
                [[0, 0], ] * len(raw_metadata['outputs'][idx][name]['tpu_shape'])

    return raw_metadata
