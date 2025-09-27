# QuanLyBanHang

**QuanLyBanHang** is a Python-based inventory management system designed to help you manage a collection of items efficiently. It provides a simple and extensible structure for adding, removing, searching, and managing items in an inventory, making it suitable for learning, prototyping, or building small-scale sales or stock management applications.

---

## 🟠 Workflow Status

[![GitHub Actions Status](https://github.com/KhoaNguyen01004/QuanLyBanHang/actions/workflows/python-app.yml/badge.svg)](https://github.com/KhoaNguyen01004/QuanLyBanHang/actions)
> **Latest run:** [failure - sửa size và equal method](https://github.com/KhoaNguyen01004/QuanLyBanHang/actions/runs/18058632300) on branch `master`

---

## Repository Structure

```
├── Inventory.py        # Inventory class implementation
├── Item.py             # Item class implementation
└── tests/
    └── test_everything.py  # Unit tests for inventory functionality
```

## Getting Started

### Prerequisites

- Python 3.13 or higher

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/KhoaNguyen01004/QuanLyBanHang.git
   cd QuanLyBanHang
   ```

2. **(Optional) Create a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

### Usage

You can use the `Inventory` and `Item` classes in your own scripts, or run the provided unittests to verify functionality:

```sh
python -m unittest tests/test_everything.py
```

#### Example

```python
from Inventory import Inventory
from Item import Item

item1 = Item("Cá", "c1", 100.0)
item2 = Item("Trứng", "tr1", 80.0)
inventory = Inventory([item1, item2])
print(inventory.get_size())  # Output: 2

inventory.remove_by_item_id("c1")
print(inventory.get_size())  # Output: 1
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

- [Khoa Nguyen](https://github.com/KhoaNguyen01004)
- [Thao Nguyen](https://github.com/TyraJr1)
