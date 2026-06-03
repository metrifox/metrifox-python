# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2026-06-03

This release fixes field names on the typed request dataclasses. Calls made
with plain dicts (e.g. `{"quantity": ...}`) were unaffected and continue to
work as before.

### Fixed
- `AccessCheckRequest` now exposes a `quantity` field. Previously it only had
  `requested_quantity`, which the API does not recognize — so access checks
  built from `AccessCheckRequest` were sent without a quantity and defaulted to
  1, regardless of the value passed. Dict-based callers passing `quantity` were
  not affected.
- `UsageEventRequest` now uses `quantity` as its canonical field name (it
  previously exposed `amount`).
- Removed `customer_type` from `CustomerUpdateRequest` (it is not an updatable
  field and was silently ignored on update).

### Changed
- The old `amount` (`UsageEventRequest`) and `requested_quantity`
  (`AccessCheckRequest`) field names are kept as deprecated aliases that map to
  `quantity`, so existing callers continue to work.
- Updated docs and examples to use `quantity`.

## [1.3.0] - 2026-05-14

### Added
- `usages.quantity_price()` — compute the price for a given quantity of a
  feature based on the customer's plan, including a per-tier breakdown
  (`applied_tiers`). Available to tenants whose plan includes the finance API
  feature.

## [1.2.0] - 2026-05-05

### Added
- Wallets module (`client.wallets`) — list wallets, list credit allocations,
  and get a single credit allocation.
- `checkout.card_collection_url()` — generate a card-collection URL for an
  existing subscription or order.
- `customers.archive()` and `customers.unarchive()`.
- `usages.list_events()` — list usage events with optional filters and
  pagination.
- Additional response type definitions.

## [1.1.2] - 2026-03-24

### Added
- `customers.bulk_create()` — create multiple customers in a single request.
- `subscriptions.bulk_assign_plan()` — assign a plan to multiple customers in a
  single request.

## [1.1.1] - 2026-02-16

### Changed
- Documentation updates (subscriptions module added to the README).

## [1.1.0] - 2026-02-16

### Added
- Subscriptions module (`client.subscriptions`) — billing history, billing
  cycles, and entitlements endpoints.

## [1.0.0] - 2025-02-01

### Added
- Initial release of Metrifox Python SDK
- Customer management module
  - Create, update, get, list, and delete customers
  - Get detailed customer information
  - Check for active subscriptions
  - Bulk CSV upload
- Usage tracking module
  - Check feature access
  - Record usage events
  - Support for meter service
- Checkout module
  - Generate checkout URLs
- Type-safe dataclasses for all request types
- Comprehensive error handling with custom exceptions
- Full type hints support
- Detailed documentation and examples
- Support for environment variable configuration
