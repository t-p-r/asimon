#include <bits/stdc++.h>
using namespace std;

// Ordered set implementation -*- C++ -*-
#include <climits>

#ifndef CPDSA_ORDERED_SET
#define CPDSA_ORDERED_SET

namespace cpdsa {
/**
 * @brief A container allowing for operations on discrete elements
 * and ranges of values in logarithmic time.
 *
 * @ingroup sequences
 *
 * @tparam _Tp Type of element. Must be discrete (i.e. ```is_integral<_Tp>```
 * must holds true).
 * @tparam LB The smallest value allowed to be added.
 * @tparam RB One past the largest value allowed to be added.
 *
 * @note An implementation of a dynamic segment tree. Operations
 * have time complexity O(log(RB - LB)). @c LB and @c RB should be changed
 * to suit specific needs (i.e. if @c _Tp is long long).
 */
template <typename _Tp, _Tp LB = INT_MIN, _Tp RB = INT_MAX>
class ordered_set {
   private:
    static const int NULL_NODE_COUNT = 0;
    static const int NULL_NODE_SUM = 0;
    static const int NULL_NODE_MAX = LB;
    static const int NULL_NODE_MIN = RB;

    /**
     * @brief Node implementation for ordered_set.
     */
    struct node {
        int cnt;            // the amount of elements currently in the node ...
        _Tp sum;            // ... and their sum.
        _Tp lowest_value;   // Value bounds for the node.
        _Tp highest_value;  // An uninstantiated or null node has
                            // lowest_value = RB and highest_value = LB.
        node *left_child, *right_child;  // left and right child

        node()
            : cnt(NULL_NODE_COUNT),
              sum(NULL_NODE_SUM),
              lowest_value(NULL_NODE_MIN),
              highest_value(NULL_NODE_MAX) {}

        ~node() {
            ~(left_child);
            ~(right_child);
            delete this;
        };

        /**
         * @brief Returns whether the current node doesn't overlap with the
         * range
         * ```[u,v]```
         */
        bool out_of_bound(_Tp u, _Tp v) const noexcept {
            return (highest_value < u || v < lowest_value);
        }

        /**
         * @brief Returns whether the current node is completely within the
         * range
         * ```[u,v]```
         */
        bool contained_by(_Tp u, _Tp v) const noexcept {
            return (u <= lowest_value && lowest_value <= v);
        }
    };

#define NULL_NODE nullptr

    enum NODE_UPDATE_ACTIONS { ADD_ONCE, REMOVE_ONCE, REMOVE_ALL };
    enum NODE_DIRECTIONS { LEFT, RIGHT };

    node* root;
    /**
     * @brief Creates a new node and attaches it to the parent node in the given
     * direction.
     *
     * @param __par The parent node.
     * @param __dir The direction in which to attach the new node (0 for left
     * child, 1 for right child).
     */
    constexpr void create_node(node* par, bool dir) {
        if (dir == NODE_DIRECTIONS::LEFT)
            par->left_child = new node();
        else
            par->right_child = new node();
    }

    /**
     * @brief Wrapper function for cnt
     */
    [[nodiscard]] constexpr _Tp get_cnt(node* id) const noexcept {
        return id == NULL_NODE ? NULL_NODE_COUNT : id->cnt;
    }

    /**
     * @brief Wrapper function for sum.
     */
    [[nodiscard]] constexpr _Tp get_sum(node* id) const noexcept {
        return id == NULL_NODE ? NULL_NODE_SUM : id->sum;
    }

    /**
     * @brief Wrapper function for lowest_value.
     */
    [[nodiscard]] constexpr _Tp get_lowest(node* id) const noexcept {
        return id == NULL_NODE ? RB : id->lowest_value;
    }

    /**
     * @brief Wrapper function for highest_value.
     */
    [[nodiscard]] constexpr _Tp get_highest(node* id) const noexcept {
        return id == NULL_NODE ? LB : id->highest_value;
    }

    /**
     * @brief Update the state of a leaf value/node in the container.
     *
     * @param leaf The current node.
     * @param val Value being updated.
     * @param action Action specified (see @c NODE_UPDATE_ACTIONS)
     */
    constexpr void update_leaf(node* leaf, _Tp val, int action) {
        if (leaf->cnt == 0 && (action == NODE_UPDATE_ACTIONS::REMOVE_ONCE ||
                               action == NODE_UPDATE_ACTIONS::REMOVE_ALL))
            return;

        switch (action) {
            case NODE_UPDATE_ACTIONS::ADD_ONCE:
                leaf->cnt++;
                leaf->sum += val;
                break;
            case NODE_UPDATE_ACTIONS::REMOVE_ONCE:
                leaf->cnt--;
                leaf->sum -= val;
                break;
            case NODE_UPDATE_ACTIONS::REMOVE_ALL:
                leaf->cnt = leaf->sum = 0;
                break;
            default:
                break;
        }

        leaf->lowest_value = leaf->cnt ? val : RB;
        leaf->highest_value = leaf->cnt ? val : LB;
    }

    /**
     * @brief Update values of the current node by propagating from its childs.
     *
     * @param id The current node.
     */
    constexpr void update_from_childs(node* id) {
        id->cnt = get_cnt(id->left_child) + get_cnt(id->right_child);
        id->sum = get_sum(id->left_child) + get_sum(id->right_child);
        id->lowest_value =
            std::min(get_lowest(id->left_child), get_lowest(id->right_child));
        id->highest_value =
            std::max(get_highest(id->left_child), get_highest(id->right_child));
    }

    /**
     * @brief Recursively update the state of a node, and all its descendants
     * containing @c val in the container.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param val Value being updated.
     * @param action Action specified (see @c NODE_UPDATE_ACTIONS)
     *
     * @note In effect, the value of the leaf node containing @c val will have
     * its values modifies first, followed by its ancestor nodes through
     * ```update_from_childs```.
     *
     */
    void update(node* id, _Tp l, _Tp r, _Tp val, int action) {
        if (l == r) {
            update_leaf(id, val, action);
            return;
        }

        _Tp mid = midpoint(l, r);
        if (val <= mid) {
            if (id->left_child == NULL_NODE)
                create_node(id, NODE_DIRECTIONS::LEFT);
            update(id->left_child, l, mid, val, action);
        } else {
            if (id->right_child == NULL_NODE)
                create_node(id, NODE_DIRECTIONS::RIGHT);
            update(id->right_child, mid + 1, r, val, action);
        }

        update_from_childs(id);
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
    [[nodiscard]] _Tp get(node* id, _Tp l, _Tp r, _Tp u, _Tp v) const {
        if (id == NULL_NODE || id.out_of_bound(u, v))
            return NULL_NODE_SUM;
        if (id.contained_by(u, v))
            return get_cnt(id);
        _Tp mid = midpoint(l, r);
        return get(id->left_child, l, mid, u, v) +
               get(id->right_child, mid + 1, r, u, v);
    }

    /**
     * @brief Find the value of the k-th largest (1-based) element in the given
     * node
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param k The position to find.
     *
     * @return Either said value or RB if no such value exists.
     */
    [[nodiscard]] _Tp k_largest(node* id, _Tp l, _Tp r, int k) const {
        if (id == NULL_NODE)
            return RB;
        if (l == r)
            return id->cnt ? id->lowest_value : RB;

        _Tp mid = midpoint(l, r);

        if (get_cnt(id->left_child) >= k)
            return k_largest(id->left_child, l, mid, k);
        else
            return k_largest(id->right_child, mid + 1, r,
                             k - get_cnt(id->left_child));
    }

    /**
     * @brief Find the smallest value in a node not less than @c val.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param val Value to compare against.
     *
     * @return Either said value or RB if no such value exists.
     */
    [[nodiscard]] _Tp lower_bound(node* id, _Tp l, _Tp r, _Tp val) const {
        if (id == NULL_NODE)
            return RB;
        if (l == r)
            return id->cnt ? id->lowest_value : RB;
        _Tp mid = midpoint(l, r);

        if (id->left_child != NULL_NODE && get_highest(id->left_child) >= val)
            return lower_bound(id->left_child, l, mid, val);
        else
            return lower_bound(id->right_child, mid + 1, r, val);
    }

    /**
     * @brief Find the largest value in a node not more than @c val.
     *
     * @param id The current node.
     * @param l Left boundary of the node's range.
     * @param r Right boundary of the node's range.
     * @param val Value to compare against.
     *
     * @return Either said value or RB if no such value exists.
     */
    [[nodiscard]] _Tp upper_bound(node* id, _Tp l, _Tp r, _Tp val) const {
        if (id == NULL_NODE)
            return RB;
        if (l == r)
            return id->cnt ? id->lowest_value : RB;

        _Tp mid = midpoint(l, r);
        if (id->right_child != NULL_NODE && get_lowest(id->right_child) <= val)
            return upper_bound(id->right_child, mid + 1, r, val);
        else
            return upper_bound(id->left_child, l, mid, val);
    }

    /**
     * @brief Clear a node and its children.
     *
     * @param id The node to be cleared.
     */
    void clear(node* id) {
        ~id;
        id = NULL_NODE;
    }

#undef NULL_NODE

   public:
    /**
     * @brief Create an ordered_set with no elements.
     */
    ordered_set() {
        static_assert(std::is_integral<_Tp>());
        root = new node();
    }

    ~ordered_set() = default;

    /**
     * @brief Returns one past the largest number allowed to be added.
     */
    [[nodiscard]] constexpr _Tp end() const noexcept { return RB; }

    /**
     * @brief Returns the number of elements in the container.
     */
    [[nodiscard]] constexpr size_t size() const noexcept { return root->cnt; }

    /**
     * @brief Returns true if the container is empty.
     */
    [[nodiscard]] constexpr bool empty() const noexcept { return !size(); }

    /**
     * @brief Add a new element into the container.
     *
     * @param val Value to be added.
     */
    constexpr void insert(const _Tp& val) {
        update(root, LB, RB, val, NODE_UPDATE_ACTIONS::ADD_ONCE);
    }

    /**
     * @brief Remove an element (i.e. one occurence of a value) from the
     * container.
     *
     * @param val Value of the element to be removed.
     */
    constexpr void erase(const _Tp& val) {
        update(root, LB, RB, val, NODE_UPDATE_ACTIONS::REMOVE_ONCE);
    }

    /**
     * @brief Remove all occurences of a value from the container.
     *
     * @param val Value to be removed.
     */
    constexpr void erase_all(const _Tp& val) {
        update(root, LB, RB, val, NODE_UPDATE_ACTIONS::REMOVE_ALL);
    }

    /**
     * @brief Remove all elements from the container.
     */
    void clear() {
        clear(root->left_child);
        clear(root->right_child);
        root = new node();
    }

    /**
     * @brief Returns the number of elements in the range ```[l,r]```.
     *
     */
    [[nodiscard]] constexpr int count(_Tp l, _Tp r) const noexcept {
        return get(root, LB, RB, l, r);
    }

    /**
     * @brief Returns the number of elements less than or equal to @c val.
     */
    [[nodiscard]] constexpr int order_of_key(const _Tp& val) const noexcept {
        return get(root, LB, RB, LB, val);
    }

    /**
     * @brief Returns the k-th largest element in the container.
     *
     * @param k The position of the element to find.
     *
     * @return Either said value or RB if no such value exists.
     */
    [[nodiscard]] constexpr _Tp find_by_order(const int& k) const noexcept {
        assert(k >= 0);
        return size() >= k ? k_largest(root, LB, RB, k) : RB;
    }

    /**
     * @brief Returns the smallest value in the container no less than @c val.
     *
     * @return Either said value or RB if no such value exists.
     */
    [[nodiscard]] constexpr _Tp lower_bound(const _Tp& val) const noexcept {
        return lower_bound(root, LB, RB, val);
    }

    /**
     * @brief Returns the largest value in the container no more than @c val.
     *
     * @return Either said value or RB if no such value exists.
     */
    [[nodiscard]] constexpr _Tp upper_bound(const _Tp& val) const noexcept {
        return upper_bound(root, LB, RB, val);
    }
};
}  // namespace cpdsa

#endif /* CPDSA_ORDERED_SET */

cpdsa::ordered_set<int, (int)-1e9, (int)1e9 + 1> st;

int32_t main() {
    cin.tie(0)->sync_with_stdio(0);
#ifdef _TPR_
    freopen("./dump/input_dump.txt", "r", stdin);
    freopen("./dump/output_dump.txt", "w", stdout);
#endif
    int t;
    while (cin >> t) {
        // cerr << t << '\n';
        if (t == 1) {
            int x;
            cin >> x;
            st.insert(x);
        } else if (t == 2) {
            int x;
            cin >> x;
            st.erase(x);
        } else if (t == 3) {
            if (st.empty())
                cout << "empty\n";
            else
                cout << st.find_by_order(1) << '\n';
        } else if (t == 4) {
            if (st.empty())
                cout << "empty\n";
            else
                cout << st.find_by_order(st.size()) << '\n';
        } else if (t == 5) {
            int x;
            cin >> x;
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.lower_bound(x + 1);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        } else if (t == 6) {
            int x;
            cin >> x;
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.lower_bound(x);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        } else if (t == 7) {
            int x;
            cin >> x;
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.upper_bound(x - 1);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        } else if (t == 8) {
            int x;
            cin >> x;
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.upper_bound(x);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        }
    }
}