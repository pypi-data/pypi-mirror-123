from .path import PathNode


fs2_data_layout = \
    PathNode('fs2_base', display='fs2-data', contents=[
        PathNode('common', contents=[
            PathNode('lexicons', contents=[
                PathNode('lexicon', display='librispeech-lexicon.txt')
            ])
        ]),
        PathNode('configs', contents=[
            PathNode('torchserve_config', display='torchserve-config.properties')
        ]),
        PathNode('data', contents=[
            PathNode('current_data', display='current_data_template', contents=[
                PathNode('aligned'),
                PathNode('before_align', display='before-align'),
                PathNode('preprocessed', contents=[
                    PathNode('duration'),
                    PathNode('energy'),
                    PathNode('mel'),
                    PathNode('pitch'),
                    PathNode('speakers', display='speakers.json'),
                    PathNode('stats', display='stats.json'),
                    PathNode('train_metadata', display='train.txt'),
                    PathNode('validate_metadata', display='val.txt'),
                ]),
                PathNode('raw_data', display='raw-data'),
                PathNode('train_output', display='saved-models', contents=[
                    PathNode('train_logs', display='logs'),
                    PathNode('train_checkpoints', display='models')
                ]),
                PathNode('checkpoint_status', display='checkpoint-status.json'),
                PathNode('train_eval_data_refs', display='data_refs.json'),
                PathNode('data_duplicated_relpaths', display='data-dupl-relpaths.json'),
                PathNode('data_relpaths', display='data-relpaths.json'),
                PathNode('optimal_checkpoint_status', display='optimal-checkpoint-status.json')
            ])
        ]),
        PathNode('metadata', contents=[
            PathNode('global_optimal_checkpoint_status', display='global-optimal-checkpoint-status.json')
        ]),
        PathNode('models', contents=[
            PathNode('archived_models', display='archived'),
            PathNode('deployed_models', display='model-store')
        ])
    ])
