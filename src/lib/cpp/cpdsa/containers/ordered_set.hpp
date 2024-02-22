// Ordered set implementation -*- C++ -*-

#ifndef CPDSA_ORDERED_SET
#define CPDSA_ORDERED_SET

#ifndef INT_MIN
#define INT_MIN (-INT_MAX - 1)
#endif

#ifndef INT_MAX
#define INT_MAX __INT_MAX__
#endif
/**
 * @brief A container allowing for operations on discrete values in logarithmic
 * time.
 *
 *
 * @tparam _Tp Type of element. Must be discrete.
 * @tparam _LB The smallest value allowed to be added.
 * @tparam _RB One past the largest value allowed to be added.
 *
 * @note An implementation of a dynamic segment tree. Operations
 * have time complexity ```O(log(_RB - _LB))```. @c _LB and @c _RB should be
 * changed to suit specific needs (i.e. if @c _Tp is long long).
 */
template <typename _Tp, _Tp _LB = INT_MIN, _Tp _RB = INT_MAX>
class ordered_set {
   private:
    /**
     * @brief Node implementation for ordered_set.
     */
    struct node {
        int __cnt = 0;  // the amount of elements currently in the node ...
        _Tp __sum = 0;  // ... and their sum
        _Tp __lo = _RB,
            __hi = _LB;   // lowest and highest values currently in the node;
                          // placeholder values can be seen
        node *__l, *__r;  // left and right child

        node() = default;
        ~node() = default;
    };

    node* root = new node();

    /**
     * @brief Creates a new node and attaches it to the parent node in the given
     * direction.
     *
     * @param __par The parent node.
     * @param __dir The direction in which to attach the new node (0 for left
     * child, 1 for right child).
     */
    void create_node(node* __par, bool __dir) {
        if (__dir == 0)
            __par->__l = new node();
        else
            __par->__r = new node();
    }

    /**
     * @brief Wrapper function for __cnt.
     */
    _Tp get_cnt(node* id) { return id == nullptr ? 0 : id->__cnt; }

    /**
     * @brief Wrapper function for __sum.
     */
    _Tp get_sum(node* id) { return id == nullptr ? 0 : id->__sum; }

    /**
     * @brief Wrapper function for __lo.
     */
    _Tp get_lo(node* id) { return id == nullptr ? _RB : id->__lo; }

    /**
     * @brief Wrapper function for __hi.
     */
    _Tp get_hi(node* id) { return id == nullptr ? _LB : id->__hi; }

    /**
     * @brief Update the state of a value in the container.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param val Value being updated.
     * @param hs The change in count for said value (either 1 or -1, or -2 if
     * every occurences of the value is to be removed).
     */
    void update(node* id, _Tp l, _Tp r, _Tp val, int hs) {
        if (l == r) {
            if (id->__cnt == 0 && hs < 0)
                return;
            if (hs == -2)
                hs = id->__cnt;
            id->__cnt += hs;
            id->__sum += val * hs;
            id->__lo = id->__cnt ? val : _RB;
            id->__hi = id->__cnt ? val : _LB;
            return;
        }
        _Tp mid = midpoint(l, r);
        if (val <= mid) {
            if (id->__l == nullptr)
                create_node(id, 0);
            update(id->__l, l, mid, val, hs);
        } else {
            if (id->__r == nullptr)
                create_node(id, 1);
            update(id->__r, mid + 1, r, val, hs);
        }

        id->__cnt = get_cnt(id->__l) + get_cnt(id->__r);
        id->__sum = get_sum(id->__l) + get_sum(id->__r);
        id->__lo = std::min(get_lo(id->__l), get_lo(id->__r));
        id->__hi = std::max(get_hi(id->__l), get_hi(id->__r));
    }

    /**
     * @brief Returns the sum of values stored in the range of a given node.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param u Left boundary of the query range.
     * @param v Right boundary of the query range.
     */
    _Tp get(node* id, _Tp l, _Tp r, _Tp u, _Tp v) {
        if (id == nullptr || id->__hi < u || v < id->__lo)
            return 0;
        if (u <= id->__lo && id->__hi <= v)
            return id->__cnt;
        _Tp mid = midpoint(l, r);
        return get(id->__l, l, mid, u, v) + get(id->__r, mid + 1, r, u, v);
    }

    /**
     * @brief Find the k-th largest element in the given node
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param k The position to find.
     *
     * @return Either said value or _RB if no such value exists.
     */
    _Tp k_largest(node* id, _Tp l, _Tp r, int k) {
        if (id == nullptr)
            return _RB;
        if (l == r)
            return id->__cnt ? id->__lo : _RB;

        _Tp mid = midpoint(l, r);
        return get_cnt(id->__l) >= k
                   ? k_largest(id->__l, l, mid, k)
                   : k_largest(id->__r, mid + 1, r, k - get_cnt(id->__l));
    }

    /**
     * @brief Find the smallest value in a node not less than @c val.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param val Value to compare against.
     *
     * @return Either said value or _RB if no such value exists.
     */
    _Tp lower_bound(node* id, _Tp l, _Tp r, _Tp val) {
        if (id == nullptr)
            return _RB;
        if (l == r)
            return id->__cnt ? id->__lo : _RB;
        _Tp mid = midpoint(l, r);
        return id->__l != nullptr && get_hi(id->__l) >= val
                   ? lower_bound(id->__l, l, mid, val)
                   : lower_bound(id->__r, mid + 1, r, val);
    }

    /**
     * @brief Find the largest value in a node not more than @c val.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param val Value to compare against.
     *
     * @return Either said value or _RB if no such value exists.
     */
    _Tp upper_bound(node* id, _Tp l, _Tp r, _Tp val) {
        if (id == nullptr)
            return _RB;
        if (l == r)
            return id->__cnt ? id->__lo : _RB;

        _Tp mid = midpoint(l, r);
        return id->__r != nullptr && get_lo(id->__r) <= val
                   ? upper_bound(id->__r, mid + 1, r, val)
                   : upper_bound(id->__l, l, mid, val);
    }

    /**
     * @brief Clear a node and its children.
     *
     * @param id The node to be cleared.
     */
    void clear(node* id) {
        if (id == nullptr)
            return;
        clear(id->__l);
        clear(id->__r);
        delete id;
        id = nullptr;
    }

   public:
    /**
     * @brief Create an ordered_set with no elements.
     */
    ordered_set() {}

    /**
     * @brief Returns one past the largest number allowed to be added.
     */
    _Tp end() { return _RB; }

    /**
     * @brief Returns the number of elements in the container.
     */
    int size() { return root->__cnt; }

    /**
     * @brief Returns true if the container is empty.
     */
    bool empty() { return !size(); }

    /**
     * @brief Add a new element into the container.
     *
     * @param val Value to be added.
     */
    void insert(const _Tp& val) { update(root, _LB, _RB, val, 1); }

    /**
     * @brief Remove an element (i.e. one occurence of a value) from the
     * container.
     *
     * @param val Value of the element to be removed.
     */
    void erase(const _Tp& val) { update(root, _LB, _RB, val, -1); }

    /**
     * @brief Remove all occurences of a value from the container.
     *
     * @param val Value to be removed.
     */
    void erase_all(const _Tp& val) { update(root, _LB, _RB, val, -2); }

    /**
     * @brief Remove all elements from the container.
     */
    void clear() {
        clear(root->__l);
        clear(root->__r);
        root = new node();
    }

    /**
     * @brief Returns the number of elements in the specified range.
     *
     * @param l Left boundary of the range.
     * @param r Right boundary of the range.
     */
    int count(_Tp l, _Tp r) { return get(root, _LB, _RB, l, r); }

    /**
     * @brief Returns the number of elements less than or equal to @c val.
     *
     * @param val Value to compare against.
     */
    int order_of_key(const _Tp& val) { return get(root, _LB, _RB, _LB, val); }

    /**
     * @brief Returns the k-th largest element in the container.
     *
     * @param k The position of the element to find.
     *
     * @return Either said value or _RB if no such value exists.
     */
    _Tp find_by_order(const int& k) {
        return size() >= k ? k_largest(root, _LB, _RB, k) : _RB;
    }

    /**
     * @brief Returns the smallest value in the container no less than @c val.
     *
     * @param val Value to compare against.
     *
     * @return Either said value or _RB if no such value exists.
     */
    _Tp lower_bound(const _Tp& val) { return lower_bound(root, _LB, _RB, val); }

    /**
     * @brief Returns the largest value in the container no more than @c val.
     *
     * @param val Value to compare against.
     *
     * @return Either said value or _RB if no such value exists.
     */
    _Tp upper_bound(const _Tp& val) { return upper_bound(root, _LB, _RB, val); }
};

#endif /* CPDSA_ORDERED_SET */