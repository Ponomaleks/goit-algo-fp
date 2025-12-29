from typing import Optional


class Node:
    def __init__(self, data=None) -> None:
        self.data = data
        self.next: Optional["Node"] = None


class LinkedList:
    def __init__(self) -> None:
        self.head = None

    def insert_at_beginning(self, data) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data) -> None:
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int) -> None:
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev: Optional["Node"] = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        if prev is not None:
            prev.next = cur.next
            cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self) -> None:
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def reverse(self) -> None:
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sort_by_merging(self) -> None:
        if self.head is None or self.head.next is None:
            return

        mid = self._get_middle(self.head)

        if mid is not None:
            next_to_mid = mid.next
            mid.next = None

        left = LinkedList()
        left.head = self.head
        right = LinkedList()
        right.head = next_to_mid

        left.sort_by_merging()
        right.sort_by_merging()

        self.head = self._sorted_merge(left.head, right.head)

    def _get_middle(self, head: Node) -> Node | None:
        if head is None:
            return head
        slow: Optional["Node"] = head
        fast: Optional["Node"] = head.next
        while fast and fast.next:
            if slow is not None:
                slow = slow.next
            fast = fast.next.next
        return slow

    def _sorted_merge(self, a: Node | None, b: Node | None) -> Node | None:
        if not a or a.data is None:
            return b
        if not b or b.data is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self._sorted_merge(a.next, b)
        else:
            result = b
            result.next = self._sorted_merge(a, b.next)
        return result


def merge_sorted_lists(list1: LinkedList, list2: LinkedList) -> LinkedList:
    merged_list = LinkedList()
    dummy = Node()
    tail = dummy

    a = list1.head
    b = list2.head

    while a and b:
        if a.data is None:
            tail.next = b
            break
        if b.data is None:
            tail.next = a
            break

        if a.data <= b.data:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a else b

    merged_list.head = dummy.next
    return merged_list


llist = LinkedList()

# Вставляємо вузли в початок
llist.insert_at_beginning(5)
llist.insert_at_beginning(10)
llist.insert_at_beginning(15)

# Вставляємо вузли в кінець
llist.insert_at_end(20)
llist.insert_at_end(25)

print("\nЗв'язний список до реверсування:")
llist.print_list()

llist.reverse()
print("\nЗв'язний список після реверсування:")
llist.print_list()

llist.sort_by_merging()
print("\nЗв'язний список після сортування:")
llist.print_list()

llist_2 = LinkedList()
llist_2.insert_at_beginning(17)
llist_2.insert_at_beginning(49)
llist_2.insert_at_beginning(30)
llist_2.insert_at_beginning(10)
llist_2.insert_at_beginning(2)
llist_2.sort_by_merging()
print("\nДругий зв'язний список після сортування:")
llist_2.print_list()
print("\nЗв'язний список після merge:")
merge_sorted_lists(llist, llist_2).print_list()
