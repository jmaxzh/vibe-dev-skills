---
name: sdlc-mysql-design
description: Design, write, modify, review, or optimize MySQL data models, table structures, SQL, indexes, transactions, and concurrency control. Use when the task or project context establishes MySQL as the target database; do not select MySQL for generic database tasks or apply this skill to other databases.
---

# MySQL Table and SQL Design

## Applicability

- Apply automatically when MySQL is established by the task or project and work involves designing, writing, modifying, reviewing, or optimizing models, tables, SQL, indexes, transactions, or concurrency. Explicit invocation is unnecessary.
- Use independently of the SDLC workflow. Do not select MySQL for generic database work or apply to tasks concerning only other databases.

## Usage

- Use official MySQL 8.4 semantics as the validation baseline without restricting the deployed version. Verify feature support, constraint enforcement, and deprecation in the actual target version when differences matter.
- Establish business meaning, integrity, main access patterns, scale/growth, concurrency, and consistency as needed. Prefer existing design/load evidence; explain assumptions and impacts when key conditions are absent.
- Apply transaction and concurrency rules to local InnoDB transactions. Explicitly identify bans on queries within transactions, `CHECK`, foreign keys, and stored procedures as project conventions, not MySQL limitations.
- Assume a record is not modified multiple times within one millisecond; such repeated changes are outside this specification's premise. This does not imply the database guarantees `updated_at` is a unique version identifier.
- Follow applicable rules within task scope. If meaning or application is unclear, read the corresponding topic in [MySQL design examples](references/mysql-design-examples.md), not all examples by default.

## Data modeling

### Entities, relationships, and field ownership

- **Row grain**: define the business object, relationship, or event represented by a row; keep grain consistent within a table. See [examples](references/mysql-design-examples.md#row-grain).

- **Relationships and uniqueness**: define minimum and maximum cardinality on both sides. Store one-to-many references on the many side, enforce one-to-one with unique references, and use junction tables for many-to-many. For repeated associations of the same objects, define each event's meaning, identity, and uniqueness scope. See [examples](references/mysql-design-examples.md#relationships-and-uniqueness).

- **Field ownership**: place a field with the object, relationship, or event determining its value; avoid duplicating current facts. Keep historical snapshots at event-time values, unchanged by current-value updates. See [examples](references/mysql-design-examples.md#field-ownership).

- **Referential integrity**: define target existence/state conditions for new or changed references and handling of existing references after target deletion/invalidation. Enforce through write paths under Keys and constraints and Concurrency control. See [examples](references/mysql-design-examples.md#referential-integrity).

## Table design

### Names and comments

- Name databases, tables, and columns using lowercase letters, digits, and underscores; do not begin with digits, use reserved words, or use unclear abbreviations.

- Name indexes for their columns or purpose. `uniq_` and `idx_` may identify unique and ordinary indexes; the primary index name is `PRIMARY`.

- Update column comments and related definitions when meanings, state values, or constraints change.

### Data types

- Keep related columns' types and signedness compatible and as consistent as possible.

- Represent exact money with explicitly sized `DECIMAL` or integers in a defined smallest unit; define currency and rounding. Preserve exact representation through storage, parameters, and calculations; do not calculate in floating point before conversion.

- Do not set deprecated `UNSIGNED` on `FLOAT`, `DOUBLE`, or `DECIMAL`.

- Use `is_xxx` and `TINYINT UNSIGNED` for booleans, with application validation restricting values to 0 or 1.

- Verify trailing-space semantics for `CHAR`.

- `TIMESTAMP` converts between session time zone and UTC; `DATETIME` does not. Store original zone names or offsets separately when needed.

- Use `created_at` for creation and `updated_at` for last modification. Mutable business records need both; append-only records need only creation time. Add them to junction or other tables according to audit needs.

- Use `DATETIME(3)`, millisecond precision, and Beijing time for audit timestamps, with connection time zone `+08:00`.

- Set audit timestamps to `NOT NULL DEFAULT CURRENT_TIMESTAMP(3)` and add `ON UPDATE CURRENT_TIMESTAMP(3)` for `updated_at`. Let the database maintain them; do not assign redundantly in the application.

### Keys and constraints

- Explicitly define stable, short primary keys for InnoDB. Secondary records contain primary-key columns, so wide primary keys increase secondary-index cost.

- Mark required fields `NOT NULL`.

- Do not use `CHECK`; validate ranges, enums, and field combinations in every application write entry point, rejecting invalid writes. See [examples](references/mysql-design-examples.md#application-validation).

- Enforce business uniqueness with unique indexes, not query-before-insert. Unique indexes allow multiple `NULL` values.

- Enforce uniqueness for idempotency identifiers within business-operation/tenant scope, with all participating columns `NOT NULL`.

- Do not use foreign-key constraints or cascades; preserve referential integrity through business write flows.

### Character sets and collations

- Use `utf8mb4` for text.

- Keep related columns' character sets and collations compatible and as consistent as possible.

- Before collation changes, check equality changes and newly duplicate values violating uniqueness.

## SQL programming

- Do not use stored procedures. Application code controls branching, commits, and rollbacks.

### Queries

- Explicitly select required columns in stable business queries; avoid `SELECT *`.

- When pagination or single-row selection requires deterministic order, use a combination of sort keys uniquely ordering rows.

- Include all sort keys in cursors. Concurrent sort-key changes can cause cross-page omissions/duplicates; cursor pagination does not guarantee a consistent cross-page snapshot.

### Data modification

- Do not hide errors that should fail using `INSERT IGNORE` or `UPDATE IGNORE`.

- Prevent `UPDATE`/`DELETE` from degenerating into full-table operations due to empty parameters or missing dynamic predicates. `LIMIT` does not replace business scope conditions.

- `updated_at` automatically tracks content changes, not execution time of every update statement.

- Do not replace ordinary updates with `REPLACE INTO`: on primary/unique conflict its replacement semantics can reset unspecified fields to defaults and trigger delete/insert behavior.

### Expressions and functions

- Match comparison types; do not let implicit conversion determine critical business comparisons.

- Distinguish bytes, characters, and user-visible graphemes in length checks. `LENGTH` counts bytes and `CHAR_LENGTH` characters, not visible graphemes.

- With `NULL` in a `NOT IN` set, an unmatched result may be `UNKNOWN`; do not treat it as ordinary non-membership.

- `COUNT(DISTINCT col)` excludes `NULL`; its multi-column form counts distinct combinations only when all participating columns are non-`NULL`.

- `SUM` returns `NULL` for empty or all-`NULL` inputs. If `GROUP BY` forms no group, no row is returned for it. Substitute zero only when business rules define empty aggregation as zero.

- Prefer half-open time intervals: include the start and exclude the end. Compute boundaries in business time zone with the same time basis as stored values.

## Transactions and consistency

### Transaction management

- **Statements inside transactions**: perform queries, business validation, and write preparation outside explicit transactions. Inside, allow only necessary modifications and transaction control; forbid ordinary/locking queries and subqueries or other query parts within writes. See [examples](references/mysql-design-examples.md#statements-inside-transactions).

- **Transaction connection**: writes that must succeed together must not escape the transaction through connection switching, asynchronous execution, or propagation settings. See [examples](references/mysql-design-examples.md#transaction-connection).

- **Implicit commits**: do not simulate nested transactions with `START TRANSACTION` or switch `autocommit` from 0 to 1 between business writes; both implicitly commit. Keep DDL such as `ALTER TABLE` and `TRUNCATE TABLE` out of business write transactions. See [examples](references/mysql-design-examples.md#implicit-commits).

- **Failure handling**: on required-write errors or unmet business conditions, stop later writes and roll back the entire transaction. Do not assume a failed statement undoes earlier writes. After deadlocks or lock timeouts, retry the whole transaction only finitely after full rollback and only when safe. For uncertain commits, verify using idempotency identifiers first. See [examples](references/mysql-design-examples.md#failure-handling).

- **External operations**: local transactions do not atomically commit/roll back external calls or message sending. See [examples](references/mysql-design-examples.md#external-operations).

### Concurrency control

- **Business-conditional updates**: prefer write-time business-field predicates. When new values depend on reads outside the transaction, check relevant old values or a valid version identifier to avoid overwriting concurrent changes. Do not add explicit transactions when one conditional statement suffices. See [examples](references/mysql-design-examples.md#business-conditional-updates).

- **Timestamp checks**: if suitable business fields are absent, match the original `updated_at` only if every relevant modification changes it and the old value cannot be reused during validation. Preserve milliseconds in reads, writes, serialization, and binding. Otherwise use a non-reused version identifier or another concurrency mechanism. See [examples](references/mysql-design-examples.md#timestamp-checks).

- **Referential integrity**: use conditional updates, uniqueness, and necessary transactions to coordinate reference creation/change against target deletion/invalidation. See [examples](references/mysql-design-examples.md#concurrent-customer-reference-maintenance).

- **Update results**: interpret conditional-update counts using the driver's affected-row semantics. An unmet predicate is not success. See [examples](references/mysql-design-examples.md#update-results).

- **Write order**: competing transactions should use consistent table/record order. SQL text order does not establish actual lock order. See [examples](references/mysql-design-examples.md#write-order).

## Database security

- Bind application data as parameters rather than concatenating it into SQL.

- Map dynamic table/column names and sort directions through code allowlists into SQL structure; value placeholders cannot replace them.

## Performance optimization

- **Request round trips**: reduce database requests per business operation while preserving correctness and overall performance.

### Index optimization

- **Index reuse and changes**: reuse indexes across primary queries. Do not add indexes merely for new SQL/predicates when existing paths meet performance needs. Check other queries and unique constraints before merging or replacing. See [examples](references/mysql-design-examples.md#index-reuse-and-changes).

- **Low-cardinality fields**: do not reject indexes solely for few distinct values. Consider target distribution, combined filters, ordering, covering benefits, table lookups, and write costs. See [examples](references/mysql-design-examples.md#low-cardinality-fields).

- **Prefix indexes**: select string-prefix lengths from actual data. Unique prefix indexes may reject distinct full values sharing a prefix and cannot replace full-value uniqueness. See [examples](references/mysql-design-examples.md#prefix-indexes).

- **Composite indexes**: balance filtering, left-prefix reuse, ordering, and grouping. Equality columns commonly precede range columns; do not universally order by selectivity. See [examples](references/mysql-design-examples.md#composite-indexes).

- **Sort cost**: `filesort` alone does not mean a bad index. Compare sorting, scans, and maintenance costs of added indexes. See [examples](references/mysql-design-examples.md#sort-cost).

- **Indexed columns and expressions**: prefer direct time-range predicates for daily filtering. If expressions are necessary, evaluate matching functional or generated-column indexes. See [examples](references/mysql-design-examples.md#indexed-columns-and-expressions).

- **Leading wildcards**: ordinary B-tree indexes generally cannot turn leading-wildcard searches into effective range scans. Full-text or dedicated search must retain original match semantics. See [examples](references/mysql-design-examples.md#leading-wildcards).

### Query optimization

- **Batch queries**: replace mergeable per-row queries with joins or batches, chunking large sets according to parameter count, result volume, and actual load. See [examples](references/mysql-design-examples.md#batch-queries).

- **Database-side computation**: prefer SQL-expressible computations with acceptable overall performance in the database. Combine update calculations and necessary business predicates in one write. See [examples](references/mysql-design-examples.md#database-side-computation).

- **Multiple detail joins**: prevent independent one-to-many joins from multiplying rows and double-counting. Aggregate each independent detail at its own grain first; do not patch with `SUM(DISTINCT ...)`. See [examples](references/mysql-design-examples.md#multiple-detail-joins).

- **Pagination with joins**: page primary records by the complete filtering criteria before retrieving details. If filtering/ordering depends on details, do not paginate first and apply criteria afterward. See [examples](references/mysql-design-examples.md#pagination-with-joins).

- **Repeated large-field transfer**: evaluate separate batch reads for primary records and details when joins repeatedly transmit large primary fields. Handle version consistency and avoid per-row queries. See [examples](references/mysql-design-examples.md#repeated-large-field-transfer).

- **Deferred large-field reads**: if filtering, sorting, and grouping do not depend on large fields, evaluate processing IDs/necessary fields first, then fetching large fields. Omitting them must not change deduplication/grouping semantics. See [examples](references/mysql-design-examples.md#deferred-large-field-reads).

### Write optimization

- **Batch writes**: prefer multi-row `INSERT ... VALUES` for mergeable inserts; evaluate set-based updates. Validate batch sizes against field sizes and load. Split transactions only for independently committable batches, preserving writes that must succeed together. See [batch writes](references/mysql-design-examples.md#batch-writes) and [atomic updates](references/mysql-design-examples.md#atomic-increment-fewer-round-trips-without-lost-updates).

### Execution plans and performance verification

#### Applicability and classification

- Perform dedicated performance verification only for complex SQL whose main costs cannot reliably be inferred from schema, indexes, and SQL. Do not additionally require plans, performance datasets, or load tests for non-complex SQL.

- Classify as complex when static analysis cannot establish scans, table lookups, or index choices affected by distribution/parameters; intermediate results or execution counts from joins/subqueries/aggregation/deduplication; or sorting, transfer, and batch-write costs determined by actual scale/field sizes.

- Do not classify by statement length, join count, or returned rows alone. See [classification examples](references/mysql-design-examples.md#classifying-complex-sql).

#### Verification method

- Use real MySQL with the target version/engine and data covering the scale, distribution, parameters, and field sizes causing uncertainty, not empty databases or a few sample rows.

- Use `EXPLAIN` for paths and `EXPLAIN ANALYZE` as needed for actual rows, loops, and time. The latter executes statements: assess costs and effects first. See [official EXPLAIN documentation](https://dev.mysql.com/doc/refman/8.4/en/explain.html).

- Measure actual requests and complete business-path latency, including transfer, reading, and application computation, not just first-row or individual-query time. Add load validation only for key concurrent paths. See [verification example](references/mysql-design-examples.md#verification-using-actual-data).

- Report conditions, results, and unverified scope. Index use, static plans, or small tests are not evidence of passing actual-load verification.
