from typing import Optional

import tensorflow as tf

def prepare_dataset(*data, batch_size:int=32, seed=None, drop_remainder=True, buffer_size:Optional[int]=None):
    """Create batched dataset with shuffling

        Arguments:
            *data: iterable of list/np.ndarray/tf.Tensor
                Iterable of data that make up the dataset.
            batchsize: int
                Number of consecutive elements of the dataset to combine in a single batch.
            seed: (Optional) int
                Random seed used in shuffling the dataset.
            drop_remainder: boolean, default=True
                Whether the last batch should be dropped in the case it has fewer than batch_size elements.
            buffer_size: (Optional) int
                Buffer size used in shuffling the dataset. If None, the sample size is used as the buffer size.
        Returns:
            tf.Dataset containing the shuffled dataset.
    """        
    data_list = []
    data_sizes = []
    for d in data:
        data_list.append(tf.data.Dataset.from_tensor_slices(d))
        if isinstance(d, tuple):
            data_sizes += [d_.shape[0] for d_ in d]
        else:
            data_sizes.append(d.shape[0])
    if len(set(data_sizes)) > 1:
        raise ValueError("input data have inconsistent sample sizes")
    if buffer_size is None:
        buffer_size = data_sizes[0]
    ds = tf.data.Dataset.zip(tuple(data_list))
    ds = ds.shuffle(buffer_size=buffer_size, seed=seed, reshuffle_each_iteration=True)
    ds = ds.batch(batch_size, drop_remainder=drop_remainder)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds