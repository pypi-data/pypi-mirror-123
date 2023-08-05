"""
# 介绍
我们提供了一个可快速处理大量数据的多进程数据处理模块
此模块可以处理list、numpy、pandas等数据，并且可以以tuple的形式输入，以tuple的形式输出
中间的处理过程可以让用户来决定，只要传入一个自定义函数即可
可设置进程数
----------------------------
# 作者
连晓磊 lian222@foxmail.com
王岳   wangyue29@tal.com
----------------------------
# 样例
样例1：分词
```
def seg(x):
    result = []
    for i in tqdm_notebook(x):
        result.append(list(jieba.cut(i)))
    return result

data = process_data(data, seg, num_workers=16)
```
-------------
样例2：text2ids
```
def convert_example(x, f_token, max_seq_len, return_raw_data=False, mask_rate=0, x1=None, avg_split=False):
    input_ids_list = []
    input_mask_list = []
    segment_ids_list = []
    input_ids_gt_list = []
    contents = []

    if x1 is not None:
        if "JPY_PARENT_PID" in os.environ:
            bar = tqdm_notebook(zip(x, x1))
        else:
            bar = tqdm(zip(x, x1))
    else:
        if "JPY_PARENT_PID" in os.environ:
            bar = tqdm_notebook(x)
        else:
            bar = tqdm(x)

    for line in bar:
        if x1 is not None:
            line, line1 = line[0], line[1]
        else:
            line1 = ''
        if mask_rate <= 0:
            input_ids, input_mask, segment_ids = convert_single_example(max_seq_len, f_token, line, line1,
                                                                        avg_split=avg_split)
        else:
            input_ids, input_mask, segment_ids, input_ids_gt = convert_single_example_with_mlm(
                max_seq_len, f_token, line, line1, avg_split=avg_split)

        input_ids = np.array(input_ids)
        input_mask = np.array(input_mask)
        segment_ids = np.array(segment_ids)
        input_ids_list.append(input_ids)
        input_mask_list.append(input_mask)
        segment_ids_list.append(segment_ids)
        if mask_rate > 0:
            input_ids_gt = np.array(input_ids_gt)
            input_ids_gt_list.append(input_ids_gt)

        if return_raw_data:
            contents.append(list(line.replace('\n', '')))

    if mask_rate > 0:
        if return_raw_data:
            return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list), \
                   np.array(input_ids_gt_list), np.array(contents)
        return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list), \
               np.array(input_ids_gt_list)
    else:
        if return_raw_data:
            return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list), np.array(contents)
        return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list)

def _process(text, **kwargs):
    f_token = kwargs.get('f_token')
    max_seq_len = kwargs.get('max_seq_len', 128)
    return_raw_data = kwargs.get('return_raw_data', False)
    mask_rate = kwargs.get('mask_rate', 0)
    avg_split = kwargs.get('avg_split', False)
    if len(text.shape) > 1:
        text_a, text_b = text[:, 0], text[:, 1]
        return convert_example(text_a, f_token, max_seq_len, return_raw_data, mask_rate, text_b, avg_split=avg_split)
    else:
        return convert_example(text, f_token, max_seq_len, return_raw_data, mask_rate, avg_split=avg_split)

vocab_file = os.path.join(bert_model_dir, "vocab.txt")
f_token = FullTokenizer(vocab_file)

text = data[text_cols].values
func_kwargs = {'f_token': f_token, 'max_seq_len': max_seq_len, 'return_raw_data': return_raw_data,
               'mask_rate': mask_rate, 'avg_split': avg_split}

result = process_data(text, _process, num_workers=16, is_tuple_data=False, func_kwargs=func_kwargs)
input_ids = result[0]
input_mask = result[1]
segment_ids = result[2]
```

"""

import numpy as np
import math
import multiprocessing


def _process_data_subprocessing(idx, manager_dict, data, op_func, kwargs):
    manager_dict[idx] = op_func(data, **kwargs)


def process_data(data, op_func, num_workers=1, **kwargs):
    """
        多进程处理数据
    Args:
        data: 输入数据
        op_func: 处理函数
        num_workers: 进程数
        **kwargs: 其它参数

    Returns:
        处理完成的数据
    """

    def throw_error(e):
        raise e

    func_kwargs = kwargs.get('func_kwargs')
    is_tuple_data = kwargs.get('is_tuple_data')
    if func_kwargs is None:
        func_kwargs = {}
    if num_workers < 2:
        data = op_func(data, **func_kwargs)
    else:
        # 计算每个进程处理的数据量
        if is_tuple_data:
            data_len = len(data[0])
        else:
            data_len = len(data)

        batch_size = math.ceil(data_len / num_workers)
        # 按照单进程数据量对数据集进行切分，当数据量不能被进程数整除时，最后一个进程会和其它进程处理的数据量不同
        batch_idxs = [list(range(batch_size * idx, min(batch_size * (idx + 1), data_len))) for idx in
                      range(num_workers)]

        # 定义进程池
        pool = multiprocessing.Pool(num_workers)
        # 定义数据共享管理器
        manager = multiprocessing.Manager()
        manager_dict = manager.dict()

        # 向进程池分发任务
        for idx in range(len(batch_idxs)):
            # 分批将数据放入进程
            _ = pool.apply_async(_process_data_subprocessing,
                                 (idx, manager_dict,
                                  data[batch_idxs[idx]] if not is_tuple_data else [item[batch_idxs[idx]] for item in
                                                                                   data],
                                  op_func, func_kwargs), error_callback=throw_error)
        pool.close()
        pool.join()

        data = []
        seg_locale = [0]  # 当数据为tuple时，用于记录合并后再分割时的index
        subprocess_result = None
        for idx in range(len(batch_idxs)):
            subprocess_result = manager_dict.get(idx)
            # 判断自定义函数返回的数据是否为tuple，如果是tuple，则此函数也会返回多个值
            # 例如自定义函数最后是`return (input_ids_batch, segment_ids_batch, input_mask_batch)`，
            # 则此函数最终返回结果是(input_ids_all, segment_ids_all, input_mask_all)
            if isinstance(subprocess_result, tuple):
                if idx == 0:
                    for item in subprocess_result[:-1]:
                        seg_locale.append(item.shape[1] + seg_locale[-1])
                    seg_locale = seg_locale[1:]
                # 将tuple数据拼接成一个大ndarray
                tmp_data = np.concatenate(subprocess_result, axis=1)
            else:
                tmp_data = subprocess_result
            data.append(tmp_data)
        # 将最后一个batch的拼接起来
        data = np.concatenate(data, axis=0)

        if isinstance(subprocess_result, tuple):
            # 将拼接后的ndarray再拆分成tuple
            data = np.split(data, seg_locale, axis=1)
    return data
