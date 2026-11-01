# MySQL Table and SQL Design Examples

This reference explains the [main skill](../SKILL.md) by topic. Business assumptions in examples do not become constraints elsewhere. SQL uses InnoDB; `:name` illustrates driver-bound parameters, which must use the actual driver's supported syntax. Fragments show relevant fields only, omitting unrelated required fields, and are not complete executable table-creation scripts.

## Data modeling

### Entities, relationships, and field ownership

Corresponding rules: [entities, relationships, and field ownership](../SKILL.md#entities-relationships-and-field-ownership). Group names match the main document's rule entries.

#### Row grain

##### Customers, orders, items, and payment attempts

Assume each order belongs to one customer and allows payment retries.

| Table | One row represents | Responsibility and relationships |
| --- | --- | --- |
| `customer` | One customer | Current customer information; a customer can have zero or more orders |
| `sales_order` | One order | Order-wide information and confirmed shipping details; references `customer_id` |
| `order_item` | One item in an order | Quantity, transaction unit price, and product name at order time; belongs through `order_id`; the same product is not assumed unique within an order |
| `payment_attempt` | One payment attempt | Request and outcome; belongs through `order_id`; an order can have zero or more attempts |

An order with two items and three payment attempts has one order, two item rows, and three attempt rows. Do not mix payment-attempt-grain records into the order table.

#### Relationships and uniqueness

##### Cardinality and repetition on both sides

Assume each order requires one customer, customers need not have orders, drafts may lack items, and submitted orders require at least one item:

| Relationship | From one side | From the other side | Repetition rules |
| --- | --- | --- | --- |
| Customer/order | Customer has zero or more orders | Order belongs to exactly one customer | Multiple distinct orders per customer allowed |
| Order/item | Draft has zero or more items; submitted order at least one | Item belongs to exactly one order | Same product may recur, distinguished by item sequence |
| Order/payment attempt | Order has zero or more attempts | Attempt belongs to exactly one order | Retry creates a new attempt; replay of the same request follows idempotency rules |

Calling customer/order one-to-many does not establish whether orders can lack customers or customers must order. Define both cardinalities and conditions when they change with business state.

##### References and constraints for one-to-many and one-to-one

One-to-many: store `customer_id` in `sales_order`, not an order-ID list in customers. Make it `NOT NULL` if customer ownership is required, but not individually unique because a customer can have multiple orders.

One-to-one: assume at most one profile per customer and one owner per profile. Either design works:

| Structure | Profile-table constraints | Enforces |
| --- | --- | --- |
| Separate primary key | `id` primary key; `customer_id` nonnull and unique | At most one profile per customer |
| Reference as primary key | `customer_id` primary key | At most one profile per customer |

Both permit customers without profiles and neither alone proves customer existence. If customer creation must also create a profile, enforce existence through writes that commit together. Uniqueness or `NOT NULL` alone does not prove both records exist.

##### Relationship attributes and uniqueness scope: enrollment

Assume students can take multiple courses and courses have multiple students; a student can enroll in the same course only once per semester:

| Student ID | Course ID | Semester | Enrollment time | Grade |
| --- | --- | --- | --- | --- |
| S01 | C01 | Fall 2026 | 2026-09-01 09:00:00 | Not graded |
| S02 | C01 | Fall 2026 | 2026-09-01 10:00:00 | Not graded |
| S01 | C01 | Spring 2027 | 2027-02-20 09:00:00 | Not graded |

Store these in an enrollment junction table. Enrollment time and grade describe a student's course relationship in a semester, not the student or course itself.

Enforce uniqueness on student ID + course ID + semester, all required. Student/course alone wrongly rejects later-semester enrollment; a separate primary key alone does not prevent same-semester duplicates.

##### Repeated participation: employees rejoining projects

Assume employees may leave and rejoin a project and each participation must be retained:

| Participation ID | Employee ID | Project ID | Start | End |
| --- | --- | --- | --- | --- |
| R001 | E01 | P01 | 2026-01-01 | 2026-03-01 |
| R002 | E01 | P01 | 2026-06-01 | NULL (ongoing) |

Both share employee/project IDs but represent distinct participation. A unique constraint on that pair would reject rejoining. Identify each participation separately and end the specified record on departure.

Use half-open validity intervals: R001 is valid from January 1 until March 1, exclusive; R002 starts June 1 without an end. These intervals answer whether an employee belonged to a project on a date.

Separately define whether intervals for the same employee/project may overlap. Participation IDs alone prevent neither duplicate creation of one participation nor overlaps; enforce required limits through business uniqueness and main-document concurrency rules.

##### Repeated business events: tipping an article multiple times

Assume a user may tip the same article repeatedly:

| Tip order ID | User ID | Article ID | Amount (CNY yuan) | Event time |
| --- | --- | --- | --- | --- |
| T001 | U01 | A01 | 5.00 | 2026-10-16 10:00:00 |
| T002 | U01 | A01 | 10.00 | 2026-10-16 11:00:00 |

Both share user/article IDs but are separate tips. Identify events by tip order IDs and record event time; a relationship validity interval is usually unnecessary. Retries are not new tips; see [keys and constraints](../SKILL.md#keys-and-constraints) for request-identifier uniqueness.

##### Repeated attempts: retaking a course exam

Assume a student may take a course exam repeatedly. Student/course IDs alone cannot distinguish attempts; use an exam-record ID or exam session/attempt number according to business rules.

For attempts 1 and 2 in the same course, uniqueness on student ID + course ID + attempt number prevents duplicate recording. Exam time records the event; relationship validity intervals are usually unnecessary.

##### Distinct roles: a user joining an organization in multiple roles

Assume users may hold multiple roles in the same organization simultaneously:

| User ID | Organization ID | Role |
| --- | --- | --- |
| U01 | G01 | Administrator |
| U01 | G01 | Reviewer |

Both share user/organization but differ in role. If maintaining one current authorization per role, enforce uniqueness on user ID + organization ID + role, not just user/organization.

Business rules determine authorization intervals and whether repeated grants of the same role are retained. If history is retained, establish how each grant is distinguished.

Repeated associations can mean repeated participation, events, or roles. Establish meaning before identity and uniqueness scope. Define start/end and overlap rules only when validity intervals are actual business concepts.

#### Field ownership

A customer's current name belongs to the customer, a product's current price to the product, and transaction price/quantity to the order item. The following examples derive ownership from meaning and dependencies.

##### Field ownership and duplicate maintenance: current customer name

Suppose customer information exists only in orders, each maintaining the current customer name:

| Order ID | Customer ID | Current customer name |
| --- | --- | --- |
| O001 | C01 | Zhang San |
| O002 | C01 | Zhang San |

At a given time, C01 determines its current name. This dependency is a business rule, not a prohibition on renaming.

Duplicating this fact causes:

- Insert anomaly: no suitable place for customer information before their first order.
- Update anomaly: renaming requires changing multiple orders; omissions cause inconsistent names.
- Delete anomaly: deleting the last order may lose the customer information too.

Store customers and orders separately:

| Table | Example fields | Maintenance responsibility |
| --- | --- | --- |
| `customer` | Customer ID, current name | Maintain current customer name |
| `sales_order` | Order ID, customer ID | Store order and reference customer |

Rename only the customer row. Even after creating a customer table, check whether orders still redundantly maintain its current name; identifying entities and relationships alone does not ensure proper field ownership.

##### Historical snapshots: transaction price and product name at order time

Assume a product is named "White short-sleeve shirt" at purchase for 80 yuan, later renamed "White cotton short-sleeve shirt" with current price 90 yuan.

Products maintain current name/price; order items retain "White short-sleeve shirt" and 80 yuan. These describe the purchase and are historical snapshots, not synchronized current information.

##### Partial dependency: order date in items

A candidate key is a minimal set of fields uniquely identifying a record; select one as primary key. Non-key attributes belong to no candidate key.

Assume items are uniquely identified by order ID + item sequence, but each stores the order date:

| Order ID | Item sequence | Quantity | Order date |
| --- | --- | --- | --- |
| O001 | 1 | 2 | 2026-10-16 |
| O001 | 2 | 5 | 2026-10-16 |

Quantity depends on the complete order/item key, but order date depends only on order ID. This is a non-key attribute's partial dependency on a composite candidate key.

Put order date in the order table and keep quantity in items, avoiding repeated maintenance across items.

##### Transitive dependency and surrogate keys: customer names in orders

Suppose order ID determines customer ID, which determines current customer name:

`Order ID → Customer ID → Current customer name`

The name depends indirectly on order ID through customer ID: the transitive dependency to check here. Maintain current names in customers; orders need only customer IDs.

A surrogate key is an additional generated identifier such as auto-increment `id`. Adding it provides identity but does not remove business dependencies or duplicated names/dates. Continue checking ownership by business rules.

#### Referential integrity

##### Customer existence, state, and deletion

Assume orders may belong only to enabled customers; disabling retains historical orders, and customers with orders cannot be physically deleted:

| Operation | Required condition | Expected outcome |
| --- | --- | --- |
| Create or reassign order | Target customer exists and is enabled | Reject missing/disabled customer references |
| Disable customer | Change state through business flow | Retain existing orders; prohibit new ownership |
| Physically delete customer | No orders reference it | Reject deletion with references, avoiding dangling IDs |

A nonnull customer ID proves only a value was supplied, not existence or availability. Foreign keys are forbidden by this project; enforce rules through business writes.

A customer found enabled can be disabled/deleted before insertion. Coordinate creation, reassignment, disabling, and deletion under [concurrency control](../SKILL.md#concurrency-control) so committed data obeys the rules; one pre-write query is insufficient.

## Table design

### Keys and constraints

Corresponding rules: [keys and constraints](../SKILL.md#keys-and-constraints).

#### Application validation

For example, require integer `is_enabled` in {0,1}, valid start/end times, and `ends_at > starts_at`. Validate inserts, changes, and batches in the application outside explicit transactions; reject failures.

Even an `ends_at`-only change must validate against `starts_at`. Protect read-dependent validation and stock deductions with conditional updates or optimistic locking under [concurrency control](../SKILL.md#concurrency-control), ensuring write-time conditions still hold.

## Transactions and consistency

Examples follow the main skill's project bans on foreign keys and stored procedures. Application code controls decisions, commits, and rollbacks. Ensure queries described as outside transactions are not included in unfinished framework transactions or `autocommit = 0` transactions.

### Transaction management

Corresponding rules: [transaction management](../SKILL.md#transaction-management).

#### Statements inside transactions

Assume product information must be queried and parameters prepared before creating an order and initial items.

| Stage | Application action |
| --- | --- |
| Preparation outside transaction | Query products, validate request, prepare order/item parameters |
| Start transaction | `START TRANSACTION` on the same connection |
| Necessary writes | Insert order, then initial items; inspect every result |
| End transaction | `COMMIT` only if all succeed; otherwise `ROLLBACK` |

Generate order IDs in advance or use auto-increment IDs returned by the driver's insert response for item `order_id`; do not query `SELECT LAST_INSERT_ID()` within the transaction.

Data can change after preparation. Validate stock, enabled customers, and other write-time conditions using [business-conditional updates](#business-conditional-updates) and [concurrent customer-reference maintenance](#concurrent-customer-reference-maintenance); preparation success alone is insufficient.

#### Transaction connection

Suppose order and items must succeed together but asynchronous or independent-transaction writes use another connection:

| Step | Connection A | Connection B |
| --- | --- | --- |
| 1 | Begin transaction; insert order, uncommitted | — |
| 2 | — | Insert item and independently commit |
| 3 | Later write fails; rollback | Item remains committed, unaffected by A |

Without foreign keys, nothing prevents this item insert. The order disappears while its item remains.

Perform both writes in A's same transaction. Pools must retain the connection; check asynchronous tasks and propagation settings do not place required writes in independent transactions.

#### Implicit commits

Both following fragments are counterexamples; assume their order primary keys do not already exist.

Starting another transaction does not nest it:

```sql
START TRANSACTION;
INSERT INTO sales_order (id, customer_id) VALUES (1001, 10);
START TRANSACTION; -- Implicitly commits the order, then starts a new transaction
ROLLBACK;          -- Only rolls back the new transaction; order 1001 remains
```

Switching autocommit from off to on also commits:

```sql
SET autocommit = 0;
INSERT INTO sales_order (id, customer_id) VALUES (1002, 10);
SET autocommit = 1; -- Commits the preceding order insertion
ROLLBACK;           -- Order 1002 remains
```

Writes requiring joint success share one transaction boundary; these operations do not create inner transactions or harmless stage transitions. DDL such as `ALTER TABLE` and `TRUNCATE TABLE` also implicitly commits and must not occur between business writes; later `ROLLBACK` does not undo them together. See [implicit commits](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html).

#### Failure handling

If an order inserts successfully but a required item insert fails, do not catch and commit. Stop later writes and roll back the entire transaction.

| Failure | InnoDB handling | Application response |
| --- | --- | --- |
| Unique conflict without `IGNORE` | Failed statement rolled back; earlier writes may remain | Roll back all, then handle business uniqueness/idempotency |
| Deadlock | Entire transaction rolled back | Reprepare and finitely retry the whole transaction only if safe |
| Lock timeout | Normally current statement only; configuration may roll back all | Ensure full rollback before considering limited retries |
| Required conditional update returns 0 | No statement error or automatic rollback of earlier writes | Treat as business failure and roll back all |

Retry the complete business write, not just the failed statement; reread/revalidate dependent parameters outside the transaction. Limit retries with suitable backoff, then report failure. See [InnoDB error handling](https://dev.mysql.com/doc/refman/8.4/en/innodb-error-handling.html).

A disconnect after sending `COMMIT` can leave commit status unknown. Do not assume failure and issue a new request ID; verify outcomes with the original idempotency ID, then recover through the idempotent flow.

#### External operations

Corresponding rule: External operations under [transaction management](../SKILL.md#transaction-management). Suppose an operation writes orders and makes external payments:

| Order | Operations | Outcome |
| --- | --- | --- |
| Pay, then write | Payment succeeds; order write fails and rolls back | Database rollback does not undo payment |
| Commit, then pay | Order commits; payment fails | Payment failure does not undo committed order |

Both put external calls outside explicit database transactions. Reordering cannot give them local atomicity. Design business recovery separately; this example defines boundaries, not a particular recovery strategy.

### Concurrency control

Corresponding rules: [concurrency control](../SKILL.md#concurrency-control).

#### Business-conditional updates

Assume signed-integer stock `available` starts at 1; requests A and B each deduct 1. This incorrect flow checks only after reading, omitting write-time stock conditions:

| Step | Request A | Request B |
| --- | --- | --- |
| 1 | Reads stock 1 | — |
| 2 | — | Also reads 1 |
| 3 | Unconditionally deducts 1, leaving 0 | — |
| 4 | — | Deducts again, leaving -1 |

Previous reads do not guarantee sufficient stock; merely opening a transaction does not add the predicate. Validate a positive integer quantity outside the transaction, then issue one conditional update:

```sql
UPDATE stock
SET available = available - :quantity
WHERE id = :stock_id AND available >= :quantity;
```

With `quantity = 1` each and no replenishment, one updates 1 row and the other 0; either may win. Zero rows is not successful deduction. The statement combines checking and deduction, preventing negative stock. Autocommit suffices without another explicit transaction; include it in a shared transaction if order writes must commit together.

Prefer business fields for state transitions too; for example, only pending-payment orders can be cancelled:

```sql
UPDATE sales_order
SET status = 'cancelled'
WHERE id = :order_id AND status = 'pending_payment';
```

Other states yield zero updates and are not overwritten. Stock/state predicates directly express permitted changes without extra version columns.

These predicates protect write-time business conditions, not proof that the record never changed after reading. Overwriting `:new_available` computed from old stock with only `available >= :quantity` can lose concurrent changes. Use atomic deduction or validate all old values used in calculation. Detecting any intervening modification requires a non-reused version identifier, not merely a state that may revert.

#### Timestamp checks

Assume no suitable business state exists for concurrency checking when changing a customer remark. Define:

```sql
updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
    ON UPDATE CURRENT_TIMESTAMP(3)
```

A and B both read `updated_at = '2026-10-16 10:00:00.123'` outside transactions. Retain this original value and bind it as `:original_updated_at`:

```sql
UPDATE customer
SET remark = :remark
WHERE id = :customer_id AND updated_at = :original_updated_at;
```

Assume A changes the remark, the automatic timestamp becomes `.124`, and cannot revert to `.123` during this validation. B's subsequent update using `.123` matches zero rows and does not overwrite A.

Here `.123` and `.124` are milliseconds in the same second. Preserve all three digits through reading, writing, serialization, deserialization, and binding. Match the actual original timestamp, without truncation to seconds or substitution of current application time. The database maintains `updated_at`; do not redundantly assign it in `SET`.

`CURRENT_TIMESTAMP(3)` is not an incrementing version counter. It uses statement start time, not lock acquisition or commit time. Even under the premise excluding multiple changes in one millisecond, confirm waiting or clock changes cannot repeat/reuse timestamps; otherwise use non-reused versions. If all other fields remain unchanged, the automatic timestamp also stays unchanged; interpret results under [update results](#update-results).

See [automatic timestamp rules](https://dev.mysql.com/doc/refman/8.4/en/timestamp-initialization.html) and [current-time functions](https://dev.mysql.com/doc/refman/8.4/en/date-and-time-functions.html#function_now).

#### Concurrent customer-reference maintenance

Continue [customer existence, state, and deletion](#customer-existence-state-and-deletion): create/reassign only to enabled customers, retain existing orders after disabling, and prohibit physical deletion with orders.

Querying enabled status then inserting can race with deletion/disabling. Order uniqueness alone cannot coordinate these operations.

Maintain `order_count BIGINT UNSIGNED NOT NULL DEFAULT 0` in customers, counting all retained referencing orders. Start with no orders and count zero; existing-data adoption requires consistent counts first. This illustrates one coordination strategy, not a mandate to add counts everywhere.

Create orders in one connection using:

```sql
START TRANSACTION;
UPDATE customer
SET order_count = order_count + 1
WHERE id = :customer_id AND status = 'enabled';
-- Application: if updated rows != 1, ROLLBACK and stop later writes
INSERT INTO sales_order (id, customer_id) VALUES (:order_id, :customer_id);
-- Application: on insert failure ROLLBACK; COMMIT only after all succeed
```

Comments represent application branches: do not continue after failure. The order primary key is unique, so duplicate-insert failure rolls back the count increment too. The first update actually increments the count and holds the customer write lock until transaction end.

Delete and disable customers respectively using:

```sql
DELETE FROM customer
WHERE id = :customer_id AND order_count = 0;
```

```sql
UPDATE customer
SET status = 'disabled'
WHERE id = :customer_id AND status = 'enabled';
```

These operations and order creation write the same customer row, coordinating competition:

| Order of competition | First operation | Later operation and outcome |
| --- | --- | --- |
| Creation locks first | Increment count, insert order, commit | Deletion waits, sees positive count, deletes 0; disabling may succeed after waiting while retaining orders |
| Deletion finishes first | Delete at count zero and commit | Creation's count update finds no customer; stop |
| Disabling finishes first | Disable and commit | Creation's count update fails enabled predicate; stop |

If the first transaction rolls back, later operations judge rolled-back data. Do not guard creation while allowing deletion/disabling to bypass coordination on the same customer row.

For physical order deletion, read original customer ID outside the transaction, then decrement that customer's count and delete by both order and original customer in one transaction:

```sql
START TRANSACTION;
UPDATE customer
SET order_count = order_count - 1
WHERE id = :original_customer_id AND order_count > 0;
-- Application: if updated rows != 1, ROLLBACK and stop later writes
DELETE FROM sales_order
WHERE id = :order_id AND customer_id = :original_customer_id;
-- Application: if deleted rows != 1, ROLLBACK; COMMIT only after all succeed
```

Validate original customer ID: if reassigned, deletion by order ID alone decrements the old customer's count but leaves excess count for the new one. The original-customer predicate makes that race return zero, rolling back decrement. Do not reuse order IDs. Apply deletion/retention rules for items or other references too; this fragment only coordinates counts and ownership.

On reassignment to the same customer, leave counts unchanged. Otherwise decrement old and increment enabled target, then update ownership with an original-customer predicate in one transaction. Prepare parameters outside, require positive counts for decrement, inspect all required writes, and roll back all on failure. For two customers, choose update order under [write order](#write-order), not always decrement-first. Logical deletion retaining references does not decrement counts; all write paths must maintain them.

#### Update results

A positive conditional stock deduction necessarily changes stock when matched: one updated row means success, zero does not.

Zero alone cannot distinguish missing stock from insufficient stock. If required:

1. Ensure the autocommit update has finished; if in an explicit transaction, roll back all because a required write failed.
2. Query current stock by primary key outside explicit transactions; report absence or explain the unmet condition using current values.

This explains current state, not the exact past failure cause or guaranteed next-write success. Retries still require predicates.

Driver counts may mean matched or changed rows; verify configuration. For a table without automatic timestamps, setting an already "Contacted" remark to "Contacted" without other changes may return 1 matched but 0 changed. Thus zero does not universally mean missing record or optimistic-lock conflict. See [affected rows](https://dev.mysql.com/doc/c-api/8.4/en/mysql-affected-rows.html).

#### Write order

Assume A and B modify stock rows 1 and 2, holding locks to commit:

| Step | Transaction A | Transaction B |
| --- | --- | --- |
| 1 | Update 1; hold write lock | — |
| 2 | — | Update 2; hold write lock |
| 3 | Request 2; wait for B | — |
| 4 | — | Request 1; wait for A: deadlock |

With both updating 1 before 2, one waits at 1 while the lock holder updates 2 and commits, avoiding this opposite-order cycle.

```sql
START TRANSACTION;
UPDATE stock SET available = available - :quantity_1
WHERE id = 1 AND available >= :quantity_1;
-- Application: proceed only on success; otherwise roll back all
UPDATE stock SET available = available - :quantity_2
WHERE id = 2 AND available >= :quantity_2;
-- Application: commit only if all succeeded; otherwise roll back all
```

Both quantities must be positive. All competing paths use the same record order and, for multiple tables, the same table order; changing only one entry point is insufficient.

`WHERE id IN (1, 2)` is a predicate, not a promise to lock 1 before 2. The example uses separate primary-key-ordered updates. Predicate text order is not lock order, and consistent access order does not eliminate deadlocks involving other resources.

## Performance optimization

First classify under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). Perform dedicated verification only for complex SQL; keep correctness checks for non-complex SQL without extra plans or load tests.

### Index optimization

Corresponding rules: [index optimization](../SKILL.md#index-optimization).

#### Low-cardinality fields

Assume `sales_order` has 1,000,000 rows, primary key `id`, and five `status` values:

| Status | Rows |
| --- | ---: |
| Pending `pending` | 500 |
| Processing `processing` | 9,500 |
| Completed `completed` | 900,000 |
| Cancelled `cancelled` | 80,000 |
| Closed `closed` | 10,000 |

Few distinct values means low overall cardinality, not that every value matches many rows. Counts illustrate distributions, not index thresholds. Evaluate candidates independently without creating all. Conclusions below guide assessment, not measured results or guaranteed optimizer choices.

##### Positive example: rare-state filtering

Frequently retrieve pending-order details:

```sql
SELECT id, customer_id, total_amount, created_at
FROM sales_order
WHERE status = 'pending';
```

Evaluate `(status)`: despite five states, only 500 rows match. An index narrows location before table lookups. Frequent queries benefit if lookup cost is below a table scan; low distinct-value count alone does not exclude it.

##### Positive example: filter, sort, and fetch a few rows

Retrieve the latest 20 orders in a state:

```sql
SELECT id, created_at
FROM sales_order
WHERE status = :status
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Evaluate `(status, created_at, id)`. With status fixed, reverse index order supports sorting and stopping after enough rows; all required columns are covered. `id` breaks creation-time ties. A common state does not imply reading every matching row.

##### Positive example: tenant and state filtering

Retrieve the latest orders for a tenant and state:

```sql
SELECT id, created_at
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Evaluate `(tenant_id, status, created_at, id)` to locate the tenant/state pair, then read in timestamp/key order. This also reuses the tenant left prefix; consider other queries. Low-cardinality `status` may precede sort columns; do not mechanically put highest-cardinality columns first.

##### Positive example: covering query

Count orders in a state:

```sql
SELECT COUNT(*)
FROM sales_order
WHERE status = :status;
```

Evaluate `(status)` as a covering index, potentially reducing full-row reads even for 900,000 completed orders versus wide table rows. Counting still scans matching entries, not one lookup; verify actual table lookups and visibility-check costs.

##### Counterexample: common state and many table lookups

Retrieve multiple details for all completed orders at once:

```sql
SELECT id, customer_id, total_amount, shipping_address, remark
FROM sales_order
WHERE status = 'completed';
```

A `(status)` index could scan about 900,000 entries and fetch non-indexed fields. Many lookups may cost more than a table scan; a status predicate alone does not justify adding it.

This concerns the example's single-column index and bulk detail retrieval, not all status indexes; 90% is not a universal cutoff.

##### Counterexample: existing primary-key access

Check old state and update by order ID:

```sql
UPDATE sales_order
SET status = :new_status
WHERE id = :id AND status = :status;
```

Primary key `id` already locates at most one row before checking state. Without other needs, do not add `(status)` solely for this statement, increasing maintenance on transitions. Analyze whole queries rather than indexing each predicate independently.

##### Counterexample: an existing composite index suffices

Assume `(status, created_at, id)` already exists:

```sql
SELECT id, created_at
FROM sales_order
WHERE status = :status
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Its prefix filters status and remaining columns support sorting/coverage. Another `(status)` offers no clear benefit here but adds space/write costs. Do not add one merely because no single-column index exists; separately verify benefits for other queries needing a narrower index.

##### Counterexample: high write cost with little read benefit

Assume frequent state transitions but rare status queries, mainly the bulk completed-order detail query above. The proposed index remains `(status)`.

Every transition maintains entries. If rare reads also gain little due to lookups, write/storage/maintenance costs lack sufficient return; a million-row table alone is no justification.

This is not a ban on indexing frequently updated fields; substantial filtering, ordering, or coverage benefits warrant reassessment against actual load.

##### Verification

Classify under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). When dedicated verification is needed, compare common/rare states with representative data, scans, lookups, sorting, and full-result read costs with/without candidates; assess writes under actual transition load. Cover different parameters/results for `LIMIT`; do not generalize one state or run to all operations.


#### Prefix indexes

Corresponding rule: Prefix indexes under [index optimization](../SKILL.md#index-optimization). Assume `code VARCHAR(32) NOT NULL` is unique by full value; both should coexist:

| Full code | First eight characters |
| --- | --- |
| `ORDER001-A` | `ORDER001` |
| `ORDER001-B` | `ORDER001` |

`UNIQUE(code(8))` rejects the second value for a shared prefix despite distinct full codes. It is stricter than business uniqueness and rejects valid records.

The complete column is indexable here; `UNIQUE(code)` enforces full-code uniqueness. Comparison still follows collation, so different bytes do not automatically establish business uniqueness.

Nonunique `INDEX(code(8))` narrows candidates without uniqueness, but shared prefixes may still match many full values. Eight is illustrative; compare candidate counts, size, and query costs for actual prefix lengths. See [column indexes](https://dev.mysql.com/doc/refman/8.4/en/column-indexes.html).

#### Composite indexes

Corresponding rule: Composite indexes under [index optimization](../SKILL.md#index-optimization). Assume frequent latest-order retrieval for a tenant, state, and time range:

```sql
SELECT id, created_at
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
  AND created_at >= :start_time AND created_at < :end_time
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Compare ascending indexes:

| Candidate | Range and ordering |
| --- | --- |
| `(tenant_id, status, created_at, id)` | Fix tenant/state, locate time range, reverse-read by timestamp/key descending |
| `(tenant_id, created_at, status, id)` | Fix tenant, locate time range, then filter other states; status may not narrow the same contiguous range |

Status after the range column is not useless: it may support index filtering. With tenant/state fixed, both candidates may support required ordering; range position alone does not guarantee `filesort`. Compare actual scans/filtering, not merely index use.

For frequent queries filtering tenant/time without state, the second may suit better; the first is not universally optimal. Choose order for the whole workload, not cardinality rankings. See [multiple-column indexes](https://dev.mysql.com/doc/refman/8.4/en/multiple-column-indexes.html).

#### Sort cost

Corresponding rule: Sort cost under [index optimization](../SKILL.md#index-optimization). Retrieve a tenant's 20 highest-value orders:

```sql
SELECT id, total_amount
FROM sales_order
WHERE tenant_id = :tenant_id
ORDER BY total_amount DESC, id DESC
LIMIT 20;
```

| Approach | Benefits and costs |
| --- | --- |
| Existing `(tenant_id)` | Locate tenant orders, read amounts, sort; plan may show `filesort` |
| Candidate `(tenant_id, total_amount, id)` | Reverse-read sorted covered results; adds storage and insert/amount-update maintenance |

For rare queries on a few dozen orders, filtered sorting may be cheap enough without new indexes. For frequent queries with many candidates, verify whether reduced scans/lookups/sorting justify maintenance.

`LIMIT 20` does not bound the first approach to processing 20 rows. Finding highest amounts may read many candidates. Counts are illustrative, not thresholds; `filesort` means extra sorting, not necessarily disk sorting. See [ORDER BY optimization](https://dev.mysql.com/doc/refman/8.4/en/order-by-optimization.html).

#### Indexed columns and expressions

Corresponding rule under [index optimization](../SKILL.md#index-optimization). Assume Beijing-time `created_at`, ordinary `(created_at)`, and a business day of October 16, 2026.

Do not prefer extracting the date from the original column:

```sql
SELECT id, created_at
FROM sales_order
WHERE DATE(created_at) = :day;
```

Here `:day` is `2026-10-16`. An index ordered by original timestamps does not establish that `DATE(created_at)` equality automatically becomes an original-column range scan.

Prefer directly comparing the original column to time boundaries:

```sql
SELECT id, created_at
FROM sales_order
WHERE created_at >= :start_time AND created_at < :end_time;
```

Compute business-zone boundaries outside transactions; bind `:start_time = 2026-10-16 00:00:00.000` and `:end_time = 2026-10-17 00:00:00.000` with compatible types. Half-open intervals include fractional seconds without hard-coding the last millisecond or missing records after precision changes.

If stored time basis differs, convert business boundaries accordingly rather than copying literals.

If date-expression filtering is necessary, evaluate a matching `DATE(created_at)` functional index or indexed generated column; verify version support and expression matching. Do not infer all functions invalidate all indexes. Classify complexity and inspect plans/data when necessary. See [functional key parts](https://dev.mysql.com/doc/refman/8.4/en/create-index.html#create-index-functional-key-parts).

#### Leading wildcards

Corresponding rule under [index optimization](../SKILL.md#index-optimization). Assume string `product.name` with ordinary B-tree `(name)`:

```sql
SELECT id, name FROM product WHERE name LIKE 'abc%';
```

```sql
SELECT id, name FROM product WHERE name LIKE '%abc%';
```

| Pattern | Index range access |
| --- | --- |
| `'abc%'` | Fixed prefix may form a range under collation/optimization conditions; optimizer use is not guaranteed |
| `'%abc%'` | No fixed prefix, generally no useful range; a covering-index scan is not a range lookup |

The second query requires substring `abc` anywhere. Tokenized full-text search uses terms/parser rules and is not equivalent. Preserve matching semantics before evaluating full-text or dedicated search. For small/infrequent queries, retaining an acceptable measured scan may be reasonable. See [range optimization](https://dev.mysql.com/doc/refman/8.4/en/range-optimization.html).

These five groups explain principles, not real-MySQL measurements. Classify under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification); verify complex SQL before adopting candidates.


#### Index reuse and changes

Corresponding rule under [index optimization](../SKILL.md#index-optimization). Continue the order table with primary `id` and ordinary `(tenant_id, status, created_at, id)`. Check existing paths before adding SQL/predicates; not every predicate needs an index column.

##### Reuse the old index with added predicates

Add channel filtering to latest orders by tenant, state, and time:

```sql
SELECT id, created_at, channel
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
  AND created_at >= :start_time AND created_at < :end_time
  AND channel = :channel
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

The existing index still locates tenant/state/time and reads timestamp/key descending, checking `channel` via table lookup until enough results or exhaustion.

Small candidate ranges may meet latency targets without a new channel index. A missing indexed channel does not make the query unacceptable, and `LIMIT 20` does not imply only 20 candidates scanned.

##### Adjust only for an actual bottleneck

If many candidates must be scanned for a few matching-channel rows on a frequent/critical path, evaluate `(tenant_id, status, channel, created_at, id)`: channel joins the equality prefix before time-range and ordered reads.

But the original query without channel may remain:

```sql
SELECT id, created_at
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
  AND created_at >= :start_time AND created_at < :end_time
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

The new index inserts unfixed `channel` before time, ordering times separately by channel rather than necessarily globally across channels.

| Change | Benefits and costs |
| --- | --- |
| Keep old, add nothing | No extra cost; new query filters candidates, subject to performance targets |
| Keep old and add new | Evaluate paths for both query types; more storage/insert/update maintenance |
| Replace old with new | Avoid dual maintenance, but old no-channel queries may scan/sort more; verify before replacing |

Small/large depends on data, frequency, and targets, not universal counts. More columns does not mean complete replacement.

##### Check purposes before merging or replacing

Inventory major queries and constraints, not just overlapping index columns:

| Query or constraint | Index | Purpose to check |
| --- | --- | --- |
| Read/update by order ID | Primary `(id)` | Exact lookup and primary uniqueness |
| Latest orders by tenant/state/time | `(tenant_id, status, created_at, id)` | Filter, time range, order |
| Add channel filtering | Reuse old, then evaluate `(tenant_id, status, channel, created_at, id)` | Scans before channel filtering, lookups, sorting |
| Tenant/state without time order | Existing composite left prefix | Do not mechanically add `(tenant_id, status)`; verify benefits of a narrower index first |
| Unique order number per tenant | Unique `(tenant_id, order_no)` | Business uniqueness; ordinary or status-extended uniqueness is not a substitute |

The final row is another constraint: ordinary indexes containing tenant/order number do not enforce uniqueness; `UNIQUE(tenant_id, order_no, status)` permits repeated order numbers in different states, changing business rules.

Classify new and affected existing queries under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). If needed, compare under equivalent conditions including write/storage costs before retaining/merging/replacing. This is design analysis, not real-MySQL measurement; candidates are not guaranteed faster and not all listed indexes are required.


### Query optimization

Corresponding rules: [query optimization](../SKILL.md#query-optimization). Analyze target-version semantics, bind parameters, and keep queries outside explicit transactions. Amounts/counts explain results, not optimization thresholds; rewrites have not been measured in real MySQL.

#### Batch queries

Corresponding rules: Batch queries under [query optimization](../SKILL.md#query-optimization), and Request round trips under [performance optimization](../SKILL.md#performance-optimization). Counts mean actual business-statement sends, excluding connection setup and transaction control. Sending concurrently does not reduce request count.

##### Many-to-one joins instead of per-row enrichment

Suppose an order page displays current customer names and `customer.id` is globally unique. Reading orders then fetching each customer's name requires 1 + N requests, where N is returned orders; repeated customers still cause repeated requests.

Evaluate retrieving orders/names in one query:

```sql
SELECT o.id, o.created_at, o.customer_id, c.name AS customer_name
FROM sales_order AS o
LEFT JOIN customer AS c ON c.id = o.customer_id
WHERE o.tenant_id = :tenant_id
ORDER BY o.created_at DESC, o.id DESC
LIMIT 20;
```

Unique customer keys mean at most one match per order, without row multiplication. `LEFT JOIN` retains missing customers with `NULL` names. Preserve the original missing-customer contract; do not silently convert errors to nulls. Select only needed fields, assess static costs of filtering/ordering/key joins first, then verify complex paths; fewer requests does not remove scanning costs.

Alternatively retain two batch queries:

```sql
SELECT id, created_at, customer_id
FROM sales_order
WHERE tenant_id = :tenant_id
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

```sql
SELECT id, name
FROM customer
WHERE id IN (:customer_id_1, :customer_id_2);
```

Extract/deduplicate customer IDs and expand driver-bound placeholders for actual count; two IDs are illustrative, not a batch limit. Map names by ID, retain order sequence and missing customers, and avoid per-order queries. Skip the second request when no valid customer IDs exist.

Joins reduce round trips but may repeat customer data. Two batches return each customer once with an extra round trip and no automatic consistent view. Choose by consistency, field size, duplication, and measured cost, not an obligation to use one SQL. See [repeated large-field transfer](#repeated-large-field-transfer) for consistency boundaries.

##### Chunked reads instead of per-ID queries

For an order-ID list, N individual queries may become one batch:

```sql
SELECT id, status, total_amount
FROM sales_order
WHERE tenant_id = :tenant_id AND id IN (:order_id_1, :order_id_2);
```

`IN` guarantees neither input order nor missing records. Map by ID and reconstruct input order, handling missing IDs per contract. If repeated IDs require repeated outputs, preserve repetition when assembling; database row uniqueness must not change the contract.

Chunk large lists or large-field results, binding actual group sizes without broad unscoped queries. More batches add requests but control parameters, result size, and memory. Chunking guarantees no cross-request consistent view and has no universal size.

#### Database-side computation

Corresponding rule under [query optimization](../SKILL.md#query-optimization). These examples reduce read requests or detail transfer, not the database's need to access and compute data.

##### Atomic increment: fewer round trips without lost updates

Assume nonnull `counter.a` starts at 2 and two increments cannot overflow. Read-then-write requires two business statements:

```sql
SELECT a FROM counter WHERE id = :id;
-- Application reads 2 and computes new_value = 3
UPDATE counter SET a = :new_value WHERE id = :id;
```

This is a counterexample: putting reads outside explicit transactions does not remove the race:

| Step | Request A | Request B |
| --- | --- | --- |
| 1 | Reads 2 | — |
| 2 | — | Also reads 2 |
| 3 | Writes 3 | — |
| 4 | — | Also writes 3; one increment is lost |

Direct database updates need one business-statement request:

```sql
UPDATE counter SET a = a + 1 WHERE id = :id;
```

If both succeed without other changes, the total becomes 4 without overwriting from an earlier application read. For an upper limit, validate in the same statement:

```sql
UPDATE counter
SET a = a + 1
WHERE id = :id AND a < :upper_limit;
```

The limit must fit the integer type without overflow. Zero updated rows is not success. Do not add explicit transactions for single-statement operations; preserve existing boundaries when other writes must succeed together. For old-value-dependent calculations not accurately expressible in SQL, use [concurrency control](../SKILL.md#concurrency-control), not blind substitution of increment patterns.

##### Database aggregation reduces detail transfer

Suppose a tenant customer's cumulative order amount includes every state and nonnull exact `total_amount`. Read details and sum in application:

```sql
SELECT total_amount
FROM sales_order
WHERE tenant_id = :tenant_id AND customer_id = :customer_id;
```

Evaluate database aggregation instead:

```sql
SELECT customer_id, SUM(total_amount) AS total_amount
FROM sales_order
WHERE tenant_id = :tenant_id AND customer_id = :customer_id
GROUP BY customer_id;
```

Both need one request. The benefit is less detail transfer, summation, and application memory, not fewer requests. The database still processes matching rows and takes on computation; assess access paths and concurrent load.

If only completed orders count, add the same state predicate to both versions without widening scope. No matches yields no grouped result row, not automatically zero. Multiple currencies require business-defined separation or conversion, not direct summation.

Classify under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). If needed, compare requests, full-read/computation latency, database work, and resources. Fewer round trips/bytes does not guarantee faster overall execution. Examples are not measured on real MySQL; queries stay outside explicit transactions.

#### Multiple detail joins

Assume order 1001 has two items, each quantity 1 and unit price 10 yuan, plus successful payments of 5 and 15 yuan. Independent item/payment totals should each be 20 yuan.

Directly joining both detail sets before summing is a counterexample:

```sql
SELECT o.id,
       SUM(i.quantity * i.unit_price) AS item_total,
       SUM(p.amount) AS paid_total
FROM sales_order AS o
LEFT JOIN order_item AS i ON i.order_id = o.id
LEFT JOIN payment_attempt AS p
       ON p.order_id = o.id AND p.status = 'succeeded'
WHERE o.id = :order_id
GROUP BY o.id;
```

With `:order_id = 1001`, two items combine with two payments into four rows:

| Item | Item amount | Payment | Payment amount |
| --- | ---: | --- | ---: |
| I1 | 10 | P1 | 5 |
| I1 | 10 | P2 | 15 |
| I2 | 10 | P1 | 5 |
| I2 | 10 | P2 | 15 |

Both totals become 40. Row multiplication is the cause, not a missing deduplication function. `SUM(DISTINCT i.quantity * i.unit_price)` incorrectly merges two legitimate 10-yuan items into 10.

These totals are independent: aggregate by order separately, then join at-most-one-row results:

```sql
SELECT o.id, COALESCE(i.item_total, 0) AS item_total,
       COALESCE(p.paid_total, 0) AS paid_total
FROM sales_order AS o
LEFT JOIN (
    SELECT order_id, SUM(quantity * unit_price) AS item_total
    FROM order_item
    WHERE order_id = :order_id
    GROUP BY order_id
) AS i ON i.order_id = o.id
LEFT JOIN (
    SELECT order_id, SUM(amount) AS paid_total
    FROM payment_attempt
    WHERE order_id = :order_id AND status = 'succeeded'
    GROUP BY order_id
) AS p ON p.order_id = o.id
WHERE o.id = :order_id;
```

Totals return to 20 each without Cartesian detail combinations. `COALESCE` applies only because this business defines missing details as zero. Failed payments remain excluded in both versions.

Both aggregations restrict `order_id` because only one order is needed. For batches, aggregate required orders rather than the entire detail table mechanically. If item/payment allocation relationships matter, join actual relationships; independent totals are no substitute.

#### Pagination with joins

Assume pagination by order, at most 20 per page, with all items returned. `sales_order.id` and `order_item.id` are primary keys and order creation times are nonnull.

This counterexample paginates joined rows:

```sql
SELECT o.id, o.created_at, i.id AS item_id, i.product_id, i.quantity
FROM sales_order AS o
LEFT JOIN order_item AS i ON i.order_id = o.id
WHERE o.tenant_id = :tenant_id AND o.status = :status
ORDER BY o.created_at DESC, o.id DESC, i.id ASC
LIMIT 20;
```

If the newest order has 30 items, only its first 20 are returned: neither 20 orders nor a complete order.

Page primary orders first, then retrieve all items:

```sql
SELECT o.id, o.created_at, i.id AS item_id, i.product_id, i.quantity
FROM (
    SELECT id, created_at
    FROM sales_order
    WHERE tenant_id = :tenant_id AND status = :status
    ORDER BY created_at DESC, id DESC
    LIMIT 20
) AS o
LEFT JOIN order_item AS i ON i.order_id = o.id
ORDER BY o.created_at DESC, o.id DESC, i.id ASC;
```

The inner query selects at most 20 orders; the outer may exceed 20 rows to retain all items, including empty orders via `LEFT JOIN`. Do not add outer `LIMIT 20`; explicitly order orders and items.

If requiring orders containing a specified product, enforce it inside before pagination:

```sql
SELECT o.id, o.created_at, i.id AS item_id, i.product_id, i.quantity
FROM (
    SELECT so.id, so.created_at
    FROM sales_order AS so
    WHERE so.tenant_id = :tenant_id AND so.status = :status
      AND EXISTS (
          SELECT 1 FROM order_item AS matched
          WHERE matched.order_id = so.id AND matched.product_id = :product_id
      )
    ORDER BY so.created_at DESC, so.id DESC
    LIMIT 20
) AS o
LEFT JOIN order_item AS i ON i.order_id = o.id
ORDER BY o.created_at DESC, o.id DESC, i.id ASC;
```

The outer query still returns all items of selected orders, not only matching-product items: these are different requirements. Filtering after an arbitrary 20 orders can omit eligible orders or underfill pages.

Likewise for detail-dependent ordering: compute totals across candidate orders, page by total plus order primary key, then retrieve all items. Do not choose 20 by creation time then reorder only those by amount. Evaluate `(order_id)` for details or `(order_id, product_id)` for existence; verify complex plans without requiring every candidate index.

#### Repeated large-field transfer

Assume orders have `description TEXT` and `extension JSON`, with multiple items. A page selected by complete criteria is read in one query:

```sql
SELECT o.id, o.created_at, o.description, o.extension,
       i.id AS item_id, i.product_id, i.quantity
FROM (
    SELECT id, created_at, description, extension
    FROM sales_order
    WHERE tenant_id = :tenant_id AND status = :status
    ORDER BY created_at DESC, id DESC
    LIMIT 20
) AS o
LEFT JOIN order_item AS i ON i.order_id = o.id
ORDER BY o.created_at DESC, o.id DESC, i.id ASC;
```

An order with 30 items repeats its description/JSON in 30 rows. Evaluate two batch queries; first read orders with large fields:

```sql
SELECT id, created_at, description, extension
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Then read all items for actual returned order IDs:

```sql
SELECT order_id, id AS item_id, product_id, quantity
FROM order_item
WHERE order_id IN (:order_id_1, :order_id_2)
ORDER BY order_id ASC, id ASC;
```

Two IDs illustrate driver expansion to actual counts; skip query two for no orders. Group items by `order_id`, retaining order sequence and empty collections without per-order queries.

This reduces repeated transfer but adds a round trip and may mix times: old description with newer items.

If a consistent view is required, use one join meeting the target isolation level's consistent-read requirements and assess transfer costs. Do not put multiple split reads inside explicit transactions. Alternatively validate a whole-order/items version:

Prerequisites: every order-content/item change commits with incrementing the owning order's integer `content_revision` in the same write transaction. Initialize versions for new orders; never reuse deleted IDs or roll back/reuse versions. All following reads are autocommit consistent reads from the same primary, not caches or asynchronous replicas.

1. Read the order page including each version.
2. Batch-read items by selected IDs.
3. Batch-reread versions. Assemble only if all selected orders still exist with identical versions. Otherwise discard the batch and reread or report changes as required.

This validates selected orders/items, not new orders entering the filter or whether the page remains latest. Rerun complete selection if the latest set must be established.

This version strategy is optional for strict validation, not a mandate for version columns everywhere or a replacement for business-field-first writes. Order `updated_at` does not automatically cover item changes and cannot alone guarantee a consistent order/items view. Weigh transfer, extra round trips, and consistency-maintenance costs before splitting.

#### Deferred large-field reads

Assume filtering only by tenant/state and sorting by creation time/key; descriptions and JSON do not participate. Direct query:

```sql
SELECT id, created_at, description, extension
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Evaluate selecting only IDs/sort keys first, then joining large fields:

```sql
SELECT o.id, o.created_at, o.description, o.extension
FROM (
    SELECT id, created_at
    FROM sales_order
    WHERE tenant_id = :tenant_id AND status = :status
    ORDER BY created_at DESC, id DESC
    LIMIT 20
) AS page
JOIN sales_order AS o ON o.id = page.id
ORDER BY page.created_at DESC, page.id DESC;
```

Candidate `(tenant_id, status, created_at, id)` covers inner fields without explicitly carrying large values; the outer retrieves target records. This may reduce unnecessary reads/intermediate data, but the original may already be efficient and derived-table/join costs may increase. Rewriting alone proves no speedup.

If filtering JSON properties or grouping by description, these are necessary page/aggregation conditions and cannot be deferred until after selection.

Deduplication cannot arbitrarily switch to IDs. Suppose two orders share description "Contact before delivery" and distinct descriptions are required:

```sql
SELECT DISTINCT description
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status;
```

This rewrite is a counterexample:

```sql
SELECT o.description
FROM (
    SELECT DISTINCT id
    FROM sales_order
    WHERE tenant_id = :tenant_id AND status = :status
) AS chosen
JOIN sales_order AS o ON o.id = chosen.id;
```

The original deduplicates descriptions into one row; the counterexample deduplicates already-unique IDs and returns the same text twice. Preserve large-field comparison semantics for deduplication/grouping rather than dropping them to shrink intermediates.

Check results first, then classify under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). If needed, compare intermediate join rows, scans, sorts/temp tables, large-field bytes, full-read time, and application memory, not final row count alone.


### Write optimization

Corresponding rules: [write optimization](../SKILL.md#write-optimization).

#### Batch writes

Assume queries, validation, and parameters are prepared outside transactions for InnoDB batch writes. Omit unrelated required fields and bind all values. See [atomic increment](#atomic-increment-fewer-round-trips-without-lost-updates) for single-record calculations.

##### Multi-row inserts reduce round trips

Two separately sent statements need two requests:

```sql
INSERT INTO sales_order (id, status) VALUES (:id_1, :status_1);
INSERT INTO sales_order (id, status) VALUES (:id_2, :status_2);
```

Combine into one multi-row insert carrying both records in one request:

```sql
INSERT INTO sales_order (id, status)
VALUES (:id_1, :status_1), (:id_2, :status_2);
```

Benefits are fewer round trips and repeated statement processing, not less data or index maintenance. Driver batch APIs may generate multi-row SQL or execute individually; inspect actual behavior. Compare with identical commit strategy to separate statement-merging gains from fewer commits.

For text and JSON:

```sql
INSERT INTO sales_order (id, status, description, extension)
VALUES (:id_1, :status_1, :description_1, :extension_1),
       (:id_2, :status_2, :description_2, :extension_2);
```

The same row count can transmit/process far more than short records. Oversized batches increase latency/resources and may hit client, driver, or server packet limits. Two rows is illustrative, not recommended. Measure throughput, statement/transaction times, and other-request latency for actual sizes and concurrency before choosing.

##### Set-based updates instead of loops

Assume two nonnull counters each increment once without overflow and each ID should update only once. Evaluate replacing two individual updates with:

```sql
UPDATE counter
SET a = a + 1
WHERE id IN (:id_1, :id_2);
```

This merges two requests but still updates all matching rows/indexes; consider locks and time. Check expected affected counts. If every target must exist, use an explicit transaction and commit only when count equals deduplicated IDs; otherwise roll back all. Post-autocommit checking cannot undo partial updates.

For input `[1, 1, 2]`, loops increment 1 twice and 2 once, while `IN (1, 1, 2)` updates each once. Establish duplicate-ID meaning and preserve multiplicities or deduplicate accordingly; do not assume equivalence.

Do not force one set update when rows require different predicates, order, or failure semantics. Chunk by parameter size, runtime, and lock waits for large targets; chunking reduces per-request pressure but adds requests. Preserve necessary transaction boundaries.

Concurrent individual writes may hide waiting but do not reduce requests and may raise database load. Concurrency is no substitute for validating batch costs.

##### Costs of committing batches to shorten lock duration

Assume batches A and B:

| Method | Flow | Benefits and costs |
| --- | --- | --- |
| Split statements within one transaction | Begin → insert A → insert B → commit | Smaller statements; A's locks may last to final commit, so overall lock duration is not necessarily shorter |
| Independent batch commits | Begin → insert A → commit; begin → insert B → commit | A's transaction locks can release earlier, potentially reducing waits, but adds commits and permits partial success |

Independent commits may improve other requests' waits without speeding the whole task. Commit count, batch sizes, and contention matter. Split only if partial completion is allowed; do not change success conditions merely to shorten locks.

An order plus all initial items requiring atomic success may use several multi-row statements but must retain one connection/transaction and roll back all on failure. Independently valid imports may evaluate batch commits, accepting that later failures do not undo earlier commits.

Classify under [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). If needed, compare requests/throughput and, where transaction splitting is allowed, commit costs, lock duration, and waits. This is analysis, not real-MySQL measurement or a promise larger batches/partial commits are faster.

### Execution plans and performance verification

Corresponding rules: [execution plans and performance verification](../SKILL.md#execution-plans-and-performance-verification). Complex means major costs cannot reliably be inferred statically, not long/difficult syntax. Non-complex SQL requires no dedicated performance data, plans, or load tests under this specification.

#### Classifying complex SQL

Assume known schema/indexes; bounded row counts do not imply constant time in all conditions. Reclassify if fields, execution logic, or known load introduce other uncertain costs.

| Example | Known conditions | Reasoning | Dedicated verification? |
| --- | --- | --- | --- |
| A: primary-key read | `sales_order.id` primary; fixed short fields | At most one row; no aggregation/sort/large fields | No |
| B: primary-key read joined to customer | A plus primary `customer.id` and bounded name length | At most one order/customer, no row multiplication | No |
| C: status/time filter, latest 20 | Multiple indexes; unknown state/time distribution and correlation | Parameters may change access path; 20 returned rows does not bound scans | Yes |
| D: multi-detail counts and sort | No reliable bound on items, attempts, or tenant orders | Intermediate joins, aggregation/deduplication, and sorting depend on data | Yes |

##### A: ordinary record by primary key

```sql
SELECT id, status
FROM sales_order
WHERE id = :order_id;
```

Exact primary-key access to short fields matches at most one row even in a million-row table. No dedicated `EXPLAIN` or load test is required here; keep ordinary existence/state correctness checks.

##### B: join with unique bounds

```sql
SELECT o.id, o.status, c.name AS customer_name
FROM sales_order AS o
LEFT JOIN customer AS c ON c.id = o.customer_id
WHERE o.id = :order_id;
```

Both order/customer use primary keys; a join alone does not justify dedicated verification. `LEFT JOIN` retains missing-customer orders with `NULL` names. Reconsider if adding one-to-many joins or unbounded large fields.

##### C: short SQL can depend on actual data

```sql
SELECT id, created_at
FROM sales_order
WHERE tenant_id = :tenant_id AND status = :status
  AND created_at >= :start_time AND created_at < :end_time
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Assume ordinary `(tenant_id, status)` and `(tenant_id, created_at, id)`. The first narrows tenant/state but still handles time/order; the second reads time order but filters state. Relative cost depends on frequency, range, and correlation; short SQL or `LIMIT 20` does not establish bounded cost.

Unknown distribution and competing paths are explicit assumptions here. Reclassify if another index or reliable business bound removes uncertainty; this syntax is not permanently complex.

##### D: multiple joins, distinct counts, and aggregate ordering

```sql
SELECT o.id,
       COUNT(DISTINCT i.id) AS item_count,
       COUNT(DISTINCT p.id) AS payment_count
FROM sales_order AS o
LEFT JOIN order_item AS i ON i.order_id = o.id
LEFT JOIN payment_attempt AS p ON p.order_id = o.id
WHERE o.tenant_id = :tenant_id
GROUP BY o.id
ORDER BY item_count DESC, o.id DESC
LIMIT 20;
```

Assume primary `id` in each table; count items and all payment attempts per order, ordered by item count. `COUNT(DISTINCT primary_key)` counts identities without duplicate counts but does not remove intermediate combinations.

Without reliable order/item/attempt bounds, schema alone cannot establish work. Inspect join multiplication, deduplication, and sorting. Evaluate independent aggregation under [multiple detail joins](#multiple-detail-joins), but rewriting does not prove performance. This does not use `SUM(DISTINCT amount)`; identity-based counting does not generalize to monetary deduplication.

#### Verification using actual data

For example C, ask which path scans less across states/time ranges and meets business targets, then choose data/parameters for that uncertainty:

| Parameter scenario | Preparation | Uncertainty |
| --- | --- | --- |
| Rare state | Pending from low-cardinality example; ranges with and without matches | Whether state access helps and empty results still scan heavily |
| Common state | Completed, short and long business ranges | Rows read and filter/sort costs |
| Correlated state/time | Preserve recent pending concentration or sparse states in target periods | Rows crossed before finding 20 matches in time order |
| Tenant differences | Actual tenants of differing order scales | Estimated/actual scans for different tenant parameters |

Use redacted copies or representative synthetic data covering supported scale/growth while preserving state/time correlation. Uniform random data can hide these differences.

Run all queries outside explicit transactions:

1. **Inspect estimated plans**: run `EXPLAIN` for these scenarios; inspect indexes, filtering, ordering, and estimates.
2. **Check actual execution**: after assessing cost/effects, use supported `EXPLAIN ANALYZE` as needed for actual rows, loops, and time, plus metrics for scans/lookups/sorts. Twenty output rows is not total processing, nor are average rows per loop the total across all loops.
3. **Measure the complete path**: fully read via the actual driver, recording requests and end-to-end time. Include transfer, assembly, and computation when comparing joins, batches, or application computation. Add load tests only for key concurrent paths.
4. **Bound conclusions**: if only static plans or small tests were performed, identify real-load scope still unverified; do not claim actual-load verification passed.
