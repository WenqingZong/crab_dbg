## Version `0.1.4` 2025-04-17
### Fixed
- Add support for class variables. [issue](https://github.com/WenqingZong/crab_dbg/issues/18)
- Add support for special character. [issue](https://github.com/WenqingZong/crab_dbg/issues/17)

## Version `0.1.3` 2025-04-07
### Added
- More unit tests.
### Changed
- Print relative path, not absolute path.
- Deleted `numpy`, `torch` and `pandas` dependencies. Faster import now.
- Now we use `ast` to parse and unparse source code.
### Fixed
- Infinite recursion bug of customised class object.
- Ident error if the class's customised `__repr__` or `__str__` is formated to multiline string.

## Version `0.1.2` 2025-03-28
### Changed
- Fixed import error introduced in `0.1.1`.

## Version `0.1.1` 2025-03-28
### Changed
- Minimum supported python version changed from 3.12 to 3.10, so more users can use this library!
- `numpy`, `pandas`, and `torch` are now optional dependencies so adding `crab-dbg` won't blow up your dependencies.

## Version `0.1.0` 2024-10-08
### Added
- Python equivalent to Rust's `dbg!()` macro.
