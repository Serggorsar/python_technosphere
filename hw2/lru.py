from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int=10) -> None:
        self.lrucache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> str:
        if key in self.lrucache:
            self.lrucache.move_to_end(key, last=True)
            return self.lrucache[key]
        return ''

    def set(self, key: str, value: str) -> None:
        if len(self.lrucache) == self.capacity and key not in self.lrucache:
            self.lrucache.popitem(last=False)
        self.lrucache[key] = value
        self.lrucache.move_to_end(key, last=True)


    def delete(self, key: str) -> None:
        del self.lrucache[key]

if __name__ == "__main__":
    cache = LRUCache(100)
    cache.set('Jesse', 'Pinkman')
    cache.set('Walter', 'White')
    cache.set('Jesse', 'James')
    print(cache.get('Jesse') == 'James') # вернёт 'James'
    cache.delete('Walter')
    print(cache.get('Walter') == '') # вернёт ''
