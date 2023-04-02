# python3
# 3.10
from typing import Optional, TypeVar

class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == 'add':
            self.name = query[2]


Contact = tuple[int, str]
oContact = Optional[Contact]
ContactNode = TypeVar("Self", bound="ContactNode")
oContactNode = Optional[ContactNode]
class ContactNode:
    def __init__(self, value: Contact):
        self.prev: oContactNode = None
        self.next: oContactNode = None
        self.value: Contact = value


class Bucket:
    def __init__(self):
        self.head: oContactNode = None
        self.tail: oContactNode = None

    def add(self, contact: Contact) -> None:
        if (self.head is None):
            self.head = ContactNode(contact)
            self.tail = self.head
        else:
            n = self.head
            while True:
                if n.value[0] == contact[0]:
                    n.value = contact
                    return
                if n.next is None:
                    n.next = ContactNode(contact)
                    self.tail = n.next
                    return
                n = n.next

    def getName(self, number: int) -> str:
        n = self.head
        while True:
            if n.value[0] == number:
                return n.value[1]
            if n.next is None:
                return "not found" 
            n = n.next

    def remove(self, number: int) -> None:
        n = self.head
        while True:
            if n.value[0] == number:
                if n is self.head:
                    self.head = n.next
                    return
                elif n is self.tail:
                    n.prev = None
                    return
                else:
                    n.prev.next, n.next.prev= n.next, n.prev
                    return
            if n.next is None:
                return
            n = n.next


class PhoneBook:
    def __init__(self, m: int):
        self.buckets: list[Bucket] = [Bucket()] * m
        self.m: int = m

    def hashNumber(self, number: int) -> int:
        return ((518396941*number+86950909)%374219533)%self.m

    def add(self, contact: Contact):
        self.buckets[self.hashNumber(contact[0])].add(contact)

    def find(self, number: int) -> str:
        return self.buckets[self.hashNumber(number)].getName(number)

    def delete(self, number: int) -> None:
        self.buckets[self.hashNumber(number)].remove(number)


def read_queries():
    n = int(input())
    return [Query(input().split()) for i in range(n)]


def write_responses(result):
    print('\n'.join(result))


# add - add(key, value)
# del - remove(key)
# find - get(key)
def process_queries(queries):
    result = []
    # Keep list of all existing (i.e. not deleted yet) contacts.
    contacts = PhoneBook(50)
    for cur_query in queries:
        if cur_query.type == 'add':
            # if we already have contact with such number,
            # we should rewrite contact's name
            contacts.add((cur_query.number, cur_query.name))
        elif cur_query.type == 'del':
            contacts.delete(cur_query.number)
        else:
            result.append(contacts.find(cur_query.number))
    return result

if __name__ == '__main__':
    write_responses(process_queries(read_queries()))

