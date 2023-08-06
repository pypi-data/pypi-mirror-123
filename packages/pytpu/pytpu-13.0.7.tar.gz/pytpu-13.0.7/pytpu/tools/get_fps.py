# pylint: disable=E0611,C0103,R0914,W1514,R1735,R1734,C0206

import asyncio
from typing import Dict, List
from time import time
from zipfile import ZipFile
import tempfile
import json
import os
import shutil

import numpy as np
from ..pytpu import TPUDevice, TPUProgram, TPUInference, TPUProgramInfo  # type: ignore
from ..tools.helpers import to_raw

# tpu_program_path = '/auto/pytpu_tests/tpu_programs/tpu_framework_3.0.0'
# tpu_program = 'resnet50.tpu'

__all__ = [
    'get_fps',
]


async def run_inference(name: int, device: TPUDevice, inference: TPUInference,
                        data_list: List[Dict[str, np.ndarray]], silent: bool = True) -> None:

    for ii, data in enumerate(data_list):
        inference.load(data)
        if not silent:
            print(f'Process {name}: Load tensors {ii} done')
        status = await device.load_inference(inference)
        assert status.is_success
        if not silent:
            print(f'Process {name}: Run {ii} done')
        inference.get(as_dict=True)
        if not silent:
            print(f'Process {name}: Get tensors {ii} done')

        if (ii + 1) % 100 == 0:
            print(f'Process {name}: finish {ii + 1} iteration')


def get_fps(program_path: str, raw: bool = False, n_queries: int = 100, n_proc: int = 4) -> float:

    print(f'Start measure performance for program: {program_path}')
    print(f'Configuration: RAW = {raw}; queries = {n_queries}; processes = {n_proc}')

    with tempfile.TemporaryDirectory() as tempdir:
        with ZipFile(program_path, 'r') as zip_obj:
            zip_obj.extractall(tempdir)

        with open(os.path.join(tempdir, 'metadata.json'), 'r') as metadata_file:
            metadata = json.load(metadata_file)

        if raw is True:
            with open(os.path.join(tempdir, 'metadata.json'), 'w') as metadata_file:
                metadata = to_raw(metadata)
                json.dump(metadata, metadata_file)

            program_path = os.path.join(tempdir, 'program_raw.tpu')
            shutil.make_archive(program_path, 'zip', tempdir)
            os.rename(program_path + '.zip', program_path)
            print(f'Raw program saved to {program_path}')

        layers_param = dict()
        for _, region in metadata['inputs'].items():
            for name, inp in region.items():
                layers_param[inp['anchor']] = inp

        data_list = list()
        for _ in range(n_queries):
            for name in layers_param:
                # print(layers_param[name]['user_shape'])
                generated_data = (np.random.rand(*layers_param[name]['user_shape']) * 2 - 1) * 100
                # print(layers_param[name]['user_dtype'])
                generated_data = generated_data.astype(layers_param[name]['user_dtype'])
                generated_data_dict = {name: generated_data}
                data_list.append(generated_data_dict)

        batch = max([layers_param[name]['user_shape'][0] for name in layers_param])

        device = TPUDevice()
        tpu_program = TPUProgram(program_path, TPUProgramInfo())
        device.load_program(tpu_program)
        inferences = [TPUInference(tpu_program) for _ in range(n_proc)]
        inference_processes = [run_inference(ii, device, inferences[ii], data_list[ii:len(data_list):n_proc])
                               for ii in range(n_proc)]

        start_time = time()
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*inference_processes))
        total_inference_time = time() - start_time

        fps = n_queries * batch / total_inference_time

        print(f'Estimated FPS = {fps}')

    return fps
