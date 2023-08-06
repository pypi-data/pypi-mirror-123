from unittest import TestCase

from sotag.download.sotag_downloader import SOTagDownloader


# SOTagItemCollection类型定义了__add__方法，从而可以轻易地对多个.bin文件进行合并
# 依次运行以下三个测试 可以测试此合并过程

class TestSoTagItemDownloader(TestCase):

    def test_add_batch1(self):
        searcher = SOTagDownloader()
        searcher.init_all_synonyms()
        need_tag_1 = ['.net', 'html', 'javascript', 'css']
        for tag in need_tag_1:
            item = searcher.get_tag_item_for_one_tag(tag)
            searcher.so_tag_item_collection.add_so_tag_item(item)
        searcher.save("test_run_1.bin")

    def test_add_batch2(self):
        searcher = SOTagDownloader()
        searcher.init_all_synonyms()
        need_tag_1 = ['php', 'c', 'c#', 'c++']
        for tag in need_tag_1:
            item = searcher.get_tag_item_for_one_tag(tag)
            searcher.so_tag_item_collection.add_so_tag_item(item)
        searcher.save("test_run_2.bin")

    def test_add_batch3(self):
        searcher1 = SOTagDownloader("test_run_1.bin")
        searcher2 = SOTagDownloader("test_run_2.bin")
        searcher1.so_tag_item_collection = searcher1.so_tag_item_collection + searcher2.so_tag_item_collection
        searcher1.save("test_run_3.bin")
