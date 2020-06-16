
def get_only_fields(args):
    """

    :param args:
    :type args:
    :return:
    :rtype:
    """
    only_fields = set()
    if args.get('fields'):
        for field in args.get('fields').split(','):
            only_fields.add(field.strip())

    return only_fields
