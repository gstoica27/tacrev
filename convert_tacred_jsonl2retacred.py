import numpy
import json
import os

mappings = {}

def read_jsonl(file):
    id2rels = {}
    with open(file, 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            data = eval(line)
            id2rels[data['id']] = {
                'label_tacred': data['label_true'],
                'label_pred': data['label_pred']
            }
    return id2rels

def convert_label(label):
    if label == 'per:alternate_names':
        return 'per:identity'
    elif label == 'org:parents':
        return 'org:member_of'
    elif label == 'org:subsidiaries':
         return 'org:members'
    return label

def convert_data(id2rels):
    for id_str, relations in id2rels.items():
        relations['label_pred'] = convert_label(relations['label_pred'])
        relations['label_tacred'] = convert_label(relations['label_tacred'])
    return id2rels

def format_data(id2rels):
    formatted_data = []
    for id_str, relations in id2rels.items():
        gold = relations['label_tacred']
        pred = relations['label_pred']
        formatted_data.append(
            {
                "id": id_str.replace("'", '"'),
                "label_true": gold.replace("'", '"'),
                "label_pred": pred.replace("'", '"')
            }
        )
    return formatted_data

def write_jsonl(data, save_path):
    with open(save_path, 'w') as handle:
        for instance in data:
            line = "{}\n".format(instance)
            handle.write(line)

def save_jsonl(id2rels, save_path):
    formatted_data = format_data(id2rels)
    write_jsonl(formatted_data, save_path)


if __name__ == '__main__':
    load_path = '/Users/georgestoica/Desktop/Research/tacrev/results/test_results/cgcn_tacred.jsonl'
    save_path = os.path.splitext(load_path)[0] + '2retacred.jsonl'
    data = read_jsonl(load_path)
    converted_data = convert_data(data)
    save_jsonl(converted_data, save_path)