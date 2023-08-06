# -*- coding: utf-8 -*-

"""
@date: 2020/10/19 上午10:03
@file: base_evaluator.py
@author: zj
@description: 
"""

from abc import ABCMeta, abstractmethod
import torch

from zcls.config.key_word import KEY_OUTPUT
from zcls.util.metrics import topk_accuracy


class BaseEvaluator(metaclass=ABCMeta):

    def __init__(self, classes, top_k=(1,)):
        super(BaseEvaluator, self).__init__()
        self.classes = classes
        self.device = torch.device('cpu')

        self.top_k = top_k
        self._init()

    def _init(self):
        # self.topk_list = list()
        # self.cate_acc_dict = dict()
        # self.cate_num_dict = dict()

        self.total_outputs_list = list()
        self.total_targets_list = list()

        self.cate_outputs_dict = dict()
        self.cate_targets_dict = dict()
        for i in range(len(self.classes)):
            key = str(i)
            self.cate_outputs_dict[key] = list()
            self.cate_targets_dict[key] = list()

    def evaluate_train(self, output_dict: dict, targets: torch.Tensor):
        assert isinstance(output_dict, dict) and KEY_OUTPUT in output_dict.keys()

        probs = output_dict[KEY_OUTPUT]
        res = topk_accuracy(probs, targets, top_k=self.top_k)

        acc_dict = dict()
        for i in range(len(self.top_k)):
            acc_dict[f'tok{self.top_k[i]}'] = res[i]
        return acc_dict

    def evaluate_test(self, output_dict: dict, targets: torch.Tensor):
        assert isinstance(output_dict, dict) and KEY_OUTPUT in output_dict.keys()
        probs = output_dict[KEY_OUTPUT]
        outputs = probs.to(device=self.device)
        targets = targets.to(device=self.device)

        self.total_outputs_list.extend(outputs)
        self.total_targets_list.extend(targets)

        for i, target in enumerate(targets):
            key = str(target.item())
            self.cate_outputs_dict[key].append(outputs[i])
            self.cate_targets_dict[key].append(targets[i])

        # res = topk_accuracy(outputs, targets, top_k=self.top_k)
        # self.topk_list.append(torch.stack(res))
        # preds = torch.argmax(outputs, dim=1)
        # for target, pred in zip(targets.numpy(), preds.numpy()):
        #     self.cate_num_dict.update({
        #         str(target):
        #             self.cate_num_dict.get(str(target), 0) + 1
        #     })
        #     self.cate_acc_dict.update({
        #         str(target):
        #             self.cate_acc_dict.get(str(target), 0) + int(target == pred)
        #     })

    def get(self):
        assert len(self.total_targets_list) == len(self.total_outputs_list)
        if len(self.total_targets_list) == 0:
            return None, None

        result_str = '\ntotal -'
        topk_list = topk_accuracy(torch.stack(self.total_outputs_list), torch.stack(self.total_targets_list),
                                  top_k=self.top_k)
        acc_dict = dict()
        for i in range(len(self.top_k)):
            acc_dict[f"top{self.top_k[i]}"] = topk_list[i]
            result_str += '  {} acc: {:.3f}'.format(f"top{self.top_k[i]}", topk_list[i])

        for idx in range(len(self.classes)):
            class_name = self.classes[idx].strip()

            key = str(idx)
            cate_outputs = self.cate_outputs_dict[key]
            result_str += '\n{:<3} - {:<20}'.format(idx, class_name)
            if len(cate_outputs) == 0:
                for i in range(len(self.top_k)):
                    acc_dict[f"top{self.top_k[i]}"] = 0.
                    result_str += '  {:<3}: {:<5}'.format(f"top{self.top_k[i]}", "{:.2f}".format(0.))
            else:
                cate_outputs = torch.stack(self.cate_outputs_dict[key])
                cate_targets = torch.stack(self.cate_targets_dict[key])

                topk_list = topk_accuracy(cate_outputs, cate_targets, top_k=self.top_k)

                for i in range(len(self.top_k)):
                    acc_dict[f"top{self.top_k[i]}"] = topk_list[i]
                    result_str += '  {:<3}: {:<5}'.format(f"top{self.top_k[i]}", "{:.2f}".format(topk_list[i]))
        result_str += '\n'

        # if len(self.topk_list) == 0:
        #     return None, None
        #
        # cate_topk_dict = dict()
        # for class_name in self.classes:
        #     cate_topk_dict[class_name] = 0.0
        # for key in self.cate_num_dict.keys():
        #     total_num = self.cate_num_dict[key]
        #     acc_num = self.cate_acc_dict[key]
        #     class_name = self.classes[int(key)]
        #
        #     cate_topk_dict[class_name] = 1.0 * acc_num / total_num if total_num != 0 else 0.0
        #
        # result_str = '\ntotal -'
        # acc_dict = dict()
        # topk_list = torch.mean(torch.stack(self.topk_list), dim=0)
        # for i in range(len(self.top_k)):
        #     acc_dict[f"top{self.top_k[i]}"] = topk_list[i]
        #     result_str += ' {} acc: {:.3f}'.format(f"top{self.top_k[i]}", topk_list[i])
        # result_str += '\n'
        #
        # for idx in range(len(self.classes)):
        #     class_name = self.classes[idx]
        #     cate_acc = cate_topk_dict[class_name]
        #
        #     if cate_acc != 0:
        #         result_str += '{:<3} - {:<20} - acc: {:.2f}\n'.format(idx, class_name, cate_acc * 100)
        #     else:
        #         result_str += '{:<3} - {:<20} - acc: 0.0\n'.format(idx, class_name)

        return result_str, acc_dict

    def clean(self):
        self._init()
