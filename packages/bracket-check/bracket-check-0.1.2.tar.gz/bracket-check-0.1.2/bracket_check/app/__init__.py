from .handler import StaplesDataObject, DataExtractor


def bracket_checker(*args, **kwargs):
    return StaplesDataObject(DataExtractor.get_data(*args, **kwargs)).run()
