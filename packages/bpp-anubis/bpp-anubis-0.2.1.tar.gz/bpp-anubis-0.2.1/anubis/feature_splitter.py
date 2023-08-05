import os


def get_features(args, accounts) -> list:
    """
    Split the features as evenly as possible
    :param args:
    :param accounts:
    :return:
    """
    all_features = []

    for thing in os.walk(args.dir):
        for file in thing[2]:
            if file.endswith('.feature'):
                # all_features.append(os.path.join(thing[0], file))
                all_features.append(f'@section.{file.split()[0]}')

    # old way of parsing files
    # feature_data = [
    #     f'section.{f.split()[0]}' for f in
    #     os.listdir(os.path.join(args.dir)) if f.endswith('.feature')
    # ]
    # inc = -(-len(feature_data) // args.processes)  # weird, yucky
    # features = [feature_data[i:i + inc] for i in range(0, len(feature_data), inc)]

    inc = -(-len(all_features) // args.processes)  # weird, yucky
    features = [all_features[i:i + inc] for i in range(0, len(all_features), inc)]
    return list(zip(accounts, features))
