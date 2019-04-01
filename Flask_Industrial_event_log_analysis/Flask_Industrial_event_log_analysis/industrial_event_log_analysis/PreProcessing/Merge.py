import pandas as pd

""" Merge DataFrame objects by performing a database-style join operation by
columns or indexes.

If joining columns on columns, the DataFrame indexes *will be
ignored*. Otherwise if joining indexes on indexes or indexes on a column or
columns, the index will be passed on.

Parameters
----------
left : DataFrame
right : DataFrame
how : {'left', 'right', 'outer', 'inner'}, default 'inner'
* left: use only keys from left frame, similar to a SQL left outer join;
preserve key order
* right: use only keys from right frame, similar to a SQL right outer join;
preserve key order
* outer: use union of keys from both frames, similar to a SQL full outer
join; sort keys lexicographically
* inner: use intersection of keys from both frames, similar to a SQL inner
join; preserve the order of the left keys
on : label or list
Column or index level names to join on. These must be found in both
DataFrames. If `on` is None and not merging on indexes then this defaults
to the intersection of the columns in both DataFrames.
left_on : label or list, or array-like
Column or index level names to join on in the left DataFrame. Can also
be an array or list of arrays of the length of the left DataFrame.
These arrays are treated as if they are columns.
right_on : label or list, or array-like
Column or index level names to join on in the right DataFrame. Can also
be an array or list of arrays of the length of the right DataFrame.
These arrays are treated as if they are columns.
left_index : boolean, default False
Use the index from the left DataFrame as the join key(s). If it is a
MultiIndex, the number of keys in the other DataFrame (either the index
or a number of columns) must match the number of levels
right_index : boolean, default False
Use the index from the right DataFrame as the join key. Same caveats as
left_index
sort : boolean, default False
Sort the join keys lexicographically in the result DataFrame. If False,
the order of the join keys depends on the join type (how keyword)
suffixes : 2-length sequence (tuple, list, ...)
Suffix to apply to overlapping column names in the left and right
side, respectively
copy : boolean, default True
If False, do not copy data unnecessarily
indicator : boolean or string, default False
If True, adds a column to output DataFrame called "_merge" with
information on the source of each row.
If string, column with information on source of each row will be added to
output DataFrame, and column will be named value of string.
Information column is Categorical-type and takes on a value of "left_only"
for observations whose merge key only appears in 'left' DataFrame,
"right_only" for observations whose merge key only appears in 'right'
DataFrame, and "both" if the observation's merge key is found in both.

validate : string, default None
If specified, checks if merge is of specified type.

* "one_to_one" or "1:1": check if merge keys are unique in both
left and right datasets.
* "one_to_many" or "1:m": check if merge keys are unique in left
dataset.
* "many_to_one" or "m:1": check if merge keys are unique in right
dataset.
* "many_to_many" or "m:m": allowed, but does not result in checks.

.. versionadded:: 0.21.0

Notes
-----
Support for specifying index levels as the `on`, `left_on`, and
`right_on` parameters was added in version 0.23.0

Examples
--------

>>> A              >>> B
lkey value         rkey value
0   foo  1         0   foo  5
1   bar  2         1   bar  6
2   baz  3         2   qux  7
3   foo  4         3   bar  8

>>> A.merge(B, left_on='lkey', right_on='rkey', how='outer')
lkey  value_x  rkey  value_y
0  foo   1        foo   5
1  foo   4        foo   5
2  bar   2        bar   6
3  bar   2        bar   8
4  baz   3        NaN   NaN
5  NaN   NaN      qux   7

Returns
-------
merged : DataFrame
The output type will the be same as 'left', if it is a subclass
of DataFrame. """
