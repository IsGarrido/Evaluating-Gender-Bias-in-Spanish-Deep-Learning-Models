from collections import defaultdict

class FunctionalHelper:

    @staticmethod
    def group_by(items, attribute):

        groups = defaultdict(list)
        for item in items:
            val = getattr(item, attribute)
            groups[val].append(item)
        return groups

    @staticmethod
    def group_by_two(items, attribute, attribute2):

        full_groups = defaultdict(dict)
        groups = FunctionalHelper.group_by(items, attribute)
        for key in groups:
            items = groups[key]
            subgroups = FunctionalHelper.group_by(items, attribute2)
            full_groups[key] = subgroups

        return full_groups

    @staticmethod
    def sum(items, attribute):

        total = 0
        for item in items:
            val = getattr(item, attribute)
            total = total + val
        return total
