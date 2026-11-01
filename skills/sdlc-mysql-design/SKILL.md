---
name: sdlc-mysql-design
description: Design, write, modify, review, or optimize MySQL data models, table structures, SQL, indexes, transactions, and concurrency control. Use when the task or project context establishes MySQL as the target database; do not select MySQL for generic database tasks or apply this skill to other databases.
license: MIT
---

# MySQL Table and SQL Design

## Applicability

- Apply when the task or project establishes MySQL as the target database and involves data modeling, table design, SQL, indexes, transactions, or concurrency control; explicit invocation is unnecessary.
- Use independently of the SDLC workflow. Do not select MySQL for generic database work or apply to tasks concerning only other databases.

## Usage

- Use official MySQL 8.4 semantics as the validation baseline without restricting the deployed version. Verify feature support, constraint enforcement, and deprecation in the actual target version when differences matter.
- Establish the business meaning, integrity requirements, main access patterns, data scale and growth, concurrency, and consistency requirements relevant to the task. Use existing designs and workload evidence where available; state assumptions and their impact when key information is missing.
- Apply transaction and concurrency rules to local InnoDB transactions. Explicitly identify the bans on queries within transactions, `CHECK` constraints, foreign-key constraints, and stored procedures as project conventions rather than MySQL limitations.
- Assume a record is modified at most once per millisecond. This assumption does not guarantee that `updated_at` is a non-reused version identifier; apply the conditions under [timestamp checks](references/mysql-design-examples.md#timestamp-checks) before using it for concurrency control.
- Apply only the rules relevant to the task. Read the corresponding topic in [MySQL design examples](references/mysql-design-examples.md) when a rule needs clarification; do not load all examples by default.

## Data modeling

### Entities, relationships, and field ownership

- **Row grain**: define the business object, relationship, or event represented by a row; keep grain consistent within a table. See [examples](references/mysql-design-examples.md#row-grain).

- **Relationships and uniqueness**: define minimum and maximum cardinality on both sides. Store one-to-many references on the many side, use unique references to limit one-to-one relationships to at most one match, and use junction tables for many-to-many relationships. For repeated associations of the same objects, define each association's business meaning, identity, and uniqueness scope. See [examples](references/mysql-design-examples.md#relationships-and-uniqueness).

- **Field ownership**: place a field with the object, relationship, or event determining its value; avoid duplicating current facts. Keep historical snapshots at event-time values, unchanged by current-value updates. See [examples](references/mysql-design-examples.md#field-ownership).

- **Referential integrity**: define whether a referenced target must exist and which states it must satisfy when creating or changing a reference. Define how existing references are handled when the target is deleted or becomes invalid. Enforce these requirements through business write flows under [keys and constraints](#keys-and-constraints) and [concurrency control](#concurrency-control). See [examples](references/mysql-design-examples.md#referential-integrity).

## Table design

### Names and comments

- Name databases, tables, and columns using lowercase letters, digits, and underscores; do not begin with digits, use reserved words, or use unclear abbreviations.

- Name indexes for their columns or purpose. `uniq_` and `idx_` may identify unique and ordinary indexes; the primary index name is `PRIMARY`.

- Update column comments and related definitions when meanings, state values, or constraints change.

### Data types

- Keep columns used to reference or compare the same values compatible in data type and signedness; use consistent definitions where possible.

- Represent exact monetary amounts with `DECIMAL` of explicit precision and scale, or integers in a defined smallest unit; define the currency and rounding rules. Preserve exact representation through storage, parameters, and calculations; do not calculate in floating point before conversion.

- Do not set deprecated `UNSIGNED` on `FLOAT`, `DOUBLE`, or `DECIMAL`.

- Use `is_xxx` and `TINYINT UNSIGNED` for booleans, with application validation restricting values to 0 or 1.

- When using `CHAR`, verify that its trailing-space handling matches the field's business meaning.

- `TIMESTAMP` converts between session time zone and UTC; `DATETIME` does not. Store original zone names or offsets separately when needed.

- Use `created_at` for creation and `updated_at` for last modification. Mutable business records need both; append-only records need only creation time. Add them to junction or other tables according to audit needs.

- Use `DATETIME(3)`, millisecond precision, and Beijing time for audit timestamps, with connection time zone `+08:00`.

- Set audit timestamps to `NOT NULL DEFAULT CURRENT_TIMESTAMP(3)` and add `ON UPDATE CURRENT_TIMESTAMP(3)` for `updated_at`. Let the database maintain them; do not assign redundantly in the application.

### Keys and constraints

- Explicitly define stable, short primary keys for InnoDB tables. Secondary-index records contain primary-key columns, so wide primary keys increase secondary-index cost.

- Mark required fields `NOT NULL`.

- Do not use `CHECK`; validate ranges, enums, and field combinations in every application write entry point, rejecting invalid writes. See [examples](references/mysql-design-examples.md#application-validation).

- Enforce business uniqueness with unique indexes, not query-before-insert. Unique indexes allow multiple `NULL` values.

- Enforce uniqueness for idempotency identifiers within the applicable business-operation and tenant scope, with all participating columns `NOT NULL`.

- Do not use foreign-key constraints or cascades; preserve referential integrity through business write flows.

### Character sets and collations

- Use `utf8mb4` for text.

- Keep text columns used to reference or compare the same values compatible in character set and collation; use consistent definitions where possible.

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

- Under the audit-timestamp definition above, `updated_at` changes automatically when row content changes; it does not record every update statement's execution time.

- Do not replace ordinary updates with `REPLACE INTO`: on primary/unique conflict its replacement semantics can reset unspecified fields to defaults and trigger delete/insert behavior.

### Expressions and functions

- Match comparison types; do not let implicit conversion determine critical business comparisons.

- Distinguish bytes, characters, and user-visible graphemes in length checks. `LENGTH` counts bytes and `CHAR_LENGTH` characters, not visible graphemes.

- If the set used by `NOT IN` contains `NULL`, a value matching no member may yield `UNKNOWN`; do not interpret this as confirmed non-membership.

- `COUNT(DISTINCT col)` excludes `NULL`; its multi-column form counts distinct combinations only when all participating columns are non-`NULL`.

- `SUM` returns `NULL` for empty or all-`NULL` inputs. If `GROUP BY` forms no group, no row is returned for it. Substitute zero only when business rules define empty aggregation as zero.

- Prefer half-open time intervals: include the start and exclude the end. Compute boundaries in business time zone with the same time basis as stored values.

## Transactions and consistency

### Transaction management

- **Statements inside transactions**: perform queries, business validation, and write preparation outside explicit transactions. Inside the transaction, allow only necessary data modifications and transaction control. Forbid ordinary queries, locking queries, and query components within writes, including subqueries. See [examples](references/mysql-design-examples.md#statements-inside-transactions).

- **Transaction connection**: execute writes that must succeed together on the same connection within the same transaction. Connection switching, asynchronous execution, and propagation settings must preserve that boundary. See [examples](references/mysql-design-examples.md#transaction-connection).

- **Implicit commits**: do not simulate nested transactions with `START TRANSACTION` or switch `autocommit` from 0 to 1 between business writes; both implicitly commit. Keep DDL such as `ALTER TABLE` and `TRUNCATE TABLE` out of business write transactions. See [examples](references/mysql-design-examples.md#implicit-commits).

- **Failure handling**: on required-write errors or unmet business conditions, stop later writes and roll back the entire transaction. Do not assume a failed statement undoes earlier writes. After a deadlock or lock timeout, ensure full rollback and retry the whole transaction only when safe, with a finite retry limit. For uncertain commits, verify using idempotency identifiers first. See [examples](references/mysql-design-examples.md#failure-handling).

- **External operations**: local transactions do not atomically commit/roll back external calls or message sending. See [examples](references/mysql-design-examples.md#external-operations).

### Concurrency control

- **Business-conditional updates**: prefer write-time business-field predicates. When computing new values from data read outside the transaction, include predicates checking the relevant original values or a valid version identifier to avoid overwriting concurrent changes. Do not add explicit transactions when one conditional statement suffices. See [examples](references/mysql-design-examples.md#business-conditional-updates).

- **Timestamp checks**: if suitable business fields are absent, match the original `updated_at` only if every relevant modification changes it and the old value cannot be reused during validation. Preserve milliseconds in reads, writes, serialization, and binding. Otherwise use a non-reused version identifier or another concurrency mechanism. See [examples](references/mysql-design-examples.md#timestamp-checks).

- **Referential integrity**: use conditional updates, uniqueness, and necessary transactions to coordinate reference creation/change against target deletion/invalidation. See [examples](references/mysql-design-examples.md#concurrent-customer-reference-maintenance).

- **Update results**: determine whether the driver reports matched or changed rows, then assess whether the required write succeeded. An unmet predicate is not success; zero changed rows alone does not prove an unmet predicate. See [examples](references/mysql-design-examples.md#update-results).

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

- **Multiple detail joins**: prevent independent one-to-many joins from multiplying rows and double-counting. For independent totals, aggregate each detail set at the required result grain before joining; do not use `SUM(DISTINCT ...)` to compensate for row multiplication. See [examples](references/mysql-design-examples.md#multiple-detail-joins).

- **Pagination with joins**: when the page unit is a primary record, select the page using the complete filtering and ordering criteria before retrieving its details. If filtering/ordering depends on details, do not paginate first and apply criteria afterward. See [examples](references/mysql-design-examples.md#pagination-with-joins).

- **Repeated large-field transfer**: evaluate separate batch reads for primary records and details when joins repeatedly transmit large primary fields. Handle version consistency and avoid per-row queries. See [examples](references/mysql-design-examples.md#repeated-large-field-transfer).

- **Deferred large-field reads**: if filtering, sorting, and grouping do not depend on large fields, evaluate processing IDs/necessary fields first, then fetching large fields. Omitting them must not change deduplication/grouping semantics. See [examples](references/mysql-design-examples.md#deferred-large-field-reads).

### Write optimization

- **Batch writes**: prefer multi-row `INSERT ... VALUES` for mergeable inserts; evaluate set-based updates. Validate batch sizes against field sizes and load. Split transactions only for independently committable batches, preserving writes that must succeed together. See [batch writes](references/mysql-design-examples.md#batch-writes) and [atomic updates](references/mysql-design-examples.md#atomic-increment-fewer-round-trips-without-lost-updates).

### Execution plans and performance verification

#### Applicability and classification

- For this skill, classify SQL as complex when its main execution costs cannot reliably be inferred from the schema, indexes, and SQL. Require dedicated performance verification only for complex SQL; do not require additional execution plans, performance datasets, or load tests for non-complex SQL.

- Classify SQL as complex when static analysis leaves material uncertainty about any of these costs:
  - Scans, table lookups, or index choices affected by data distribution and parameters.
  - Intermediate-result sizes or execution counts from joins, subqueries, aggregation, or deduplication.
  - Sorting, transfer, or batch-write costs determined by actual data scale and field sizes.

- Do not classify by statement length, join count, or returned rows alone. See [classification examples](references/mysql-design-examples.md#classifying-complex-sql).

#### Verification method

- Use real MySQL with the target version/engine and data covering the scale, distribution, parameters, and field sizes causing uncertainty, not empty databases or a few sample rows.

- Use `EXPLAIN` to inspect access paths. Use `EXPLAIN ANALYZE` as needed for actual rows, loops, and time on supported statements; it executes the statement, so assess costs and effects first. See [official EXPLAIN documentation](https://dev.mysql.com/doc/refman/8.4/en/explain.html).

- Measure actual requests and complete business-path latency, including transfer, reading, and application computation, not just first-row or individual-query time. Add load validation only for key concurrent paths. See [verification example](references/mysql-design-examples.md#verification-using-actual-data).

- Report verification conditions, results, and unverified scope. Index use, static plans, or small tests are not evidence of passing actual-load verification.

## Deliverables

- Provide the design, SQL, changes, or review findings requested by the task, with the relevant business assumptions and reasons for consequential choices. Identify unresolved correctness or performance questions and distinguish static analysis from executed checks.
