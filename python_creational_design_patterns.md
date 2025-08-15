# Python Creational Design Patterns

Creational design patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation. These patterns provide various object creation mechanisms, which increase flexibility and reuse of existing code.

## Table of Contents

1. [Singleton Pattern](#singleton-pattern)
2. [Factory Method Pattern](#factory-method-pattern)
3. [Abstract Factory Pattern](#abstract-factory-pattern)
4. [Builder Pattern](#builder-pattern)
5. [Prototype Pattern](#prototype-pattern)

---

## Singleton Pattern

### Overview

The Singleton pattern ensures that a class has only one instance and provides a global point of access to that instance. It's useful when exactly one object is needed to coordinate actions across the system.

### When to Use

- When you need exactly one instance of a class (e.g., database connection pool, logger, configuration manager)
- When you want to control access to some shared resource
- When you need to provide a global access point to an object

### Python Implementation

```python
import threading
from typing import Optional

class Singleton:
    """Thread-safe singleton implementation using metaclass."""
    _instances = {}
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-check locking pattern
                if cls not in cls._instances:
                    cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

class DatabaseConnection(Singleton):
    """Example: Database connection singleton."""
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.connection_string = "postgresql://localhost:5432/mydb"
            self._connection = None
            print(f"Initializing database connection to {self.connection_string}")
    
    def connect(self):
        if self._connection is None:
            self._connection = f"Connected to {self.connection_string}"
            print(self._connection)
        return self._connection
    
    def execute_query(self, query: str):
        if self._connection:
            return f"Executing: {query}"
        raise Exception("Not connected to database")

# Alternative implementation using decorator
def singleton(cls):
    """Decorator-based singleton implementation."""
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Logger:
    """Example: Logger singleton using decorator."""
    
    def __init__(self):
        self.log_file = "app.log"
        print(f"Logger initialized with file: {self.log_file}")
    
    def log(self, message: str, level: str = "INFO"):
        log_entry = f"[{level}] {message}"
        print(f"Logging to {self.log_file}: {log_entry}")
        return log_entry

# Usage example
if __name__ == "__main__":
    # Database connection example
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")  # True
    
    db1.connect()
    result = db1.execute_query("SELECT * FROM users")
    print(result)
    
    # Logger example
    logger1 = Logger()
    logger2 = Logger()
    
    print(f"Same logger instance: {logger1 is logger2}")  # True
    
    logger1.log("Application started")
    logger2.log("User logged in", "DEBUG")
```

### Pros and Cons

**Pros:**
- Ensures only one instance exists
- Provides global access point
- Lazy initialization possible
- Memory efficient

**Cons:**
- Violates Single Responsibility Principle
- Difficult to unit test
- Can create hidden dependencies
- Thread safety concerns in multi-threaded environments

### Real-world Use Cases

- Database connection pools
- Logging systems
- Configuration managers
- Cache implementations
- Thread pools

---

## Factory Method Pattern

### Overview

The Factory Method pattern creates objects without specifying their exact classes. It defines an interface for creating objects, but lets subclasses decide which class to instantiate.

### When to Use

- When you don't know beforehand the exact types of objects your code should work with
- When you want to provide users with a way to extend your library's components
- When you want to save system resources by reusing existing objects

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import json
import xml.etree.ElementTree as ET

# Product interface
class DataParser(ABC):
    """Abstract base class for data parsers."""
    
    @abstractmethod
    def parse(self, data: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_format(self) -> str:
        pass

# Concrete products
class JSONParser(DataParser):
    """JSON data parser."""
    
    def parse(self, data: str) -> Dict[str, Any]:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")
    
    def get_format(self) -> str:
        return "JSON"

class XMLParser(DataParser):
    """XML data parser."""
    
    def parse(self, data: str) -> Dict[str, Any]:
        try:
            root = ET.fromstring(data)
            return self._xml_to_dict(root)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML data: {e}")
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = self._xml_to_dict(child)
        return result
    
    def get_format(self) -> str:
        return "XML"

class CSVParser(DataParser):
    """CSV data parser."""
    
    def parse(self, data: str) -> Dict[str, Any]:
        lines = data.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("CSV must have at least header and one data row")
        
        headers = [h.strip() for h in lines[0].split(',')]
        rows = []
        
        for line in lines[1:]:
            values = [v.strip() for v in line.split(',')]
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))
        
        return {"headers": headers, "data": rows}
    
    def get_format(self) -> str:
        return "CSV"

# Creator (Factory) interface
class DataParserFactory(ABC):
    """Abstract factory for creating data parsers."""
    
    @abstractmethod
    def create_parser(self) -> DataParser:
        pass
    
    def process_data(self, data: str) -> Dict[str, Any]:
        """Template method using the factory method."""
        parser = self.create_parser()
        print(f"Processing data using {parser.get_format()} parser")
        return parser.parse(data)

# Concrete creators
class JSONParserFactory(DataParserFactory):
    def create_parser(self) -> DataParser:
        return JSONParser()

class XMLParserFactory(DataParserFactory):
    def create_parser(self) -> DataParser:
        return XMLParser()

class CSVParserFactory(DataParserFactory):
    def create_parser(self) -> DataParser:
        return CSVParser()

# Factory registry for dynamic creation
class ParserFactoryRegistry:
    """Registry for managing parser factories."""
    
    def __init__(self):
        self._factories = {}
    
    def register_factory(self, format_type: str, factory: DataParserFactory):
        self._factories[format_type.lower()] = factory
    
    def create_parser(self, format_type: str) -> DataParser:
        factory = self._factories.get(format_type.lower())
        if not factory:
            raise ValueError(f"Unknown format type: {format_type}")
        return factory.create_parser()

# Usage example
if __name__ == "__main__":
    # Direct factory usage
    json_factory = JSONParserFactory()
    xml_factory = XMLParserFactory()
    csv_factory = CSVParserFactory()
    
    # Test data
    json_data = '{"name": "John", "age": 30, "city": "New York"}'
    xml_data = '<person><name>John</name><age>30</age><city>New York</city></person>'
    csv_data = 'name,age,city\nJohn,30,New York\nJane,25,Boston'
    
    # Process different data formats
    json_result = json_factory.process_data(json_data)
    print(f"JSON Result: {json_result}")
    
    xml_result = xml_factory.process_data(xml_data)
    print(f"XML Result: {xml_result}")
    
    csv_result = csv_factory.process_data(csv_data)
    print(f"CSV Result: {csv_result}")
    
    # Using registry for dynamic creation
    registry = ParserFactoryRegistry()
    registry.register_factory("json", JSONParserFactory())
    registry.register_factory("xml", XMLParserFactory())
    registry.register_factory("csv", CSVParserFactory())
    
    # Dynamic parser creation
    for format_type, test_data in [("json", json_data), ("xml", xml_data), ("csv", csv_data)]:
        parser = registry.create_parser(format_type)
        result = parser.parse(test_data)
        print(f"Dynamic {format_type.upper()} parsing: {result}")
```

### Pros and Cons

**Pros:**
- Decouples object creation from usage
- Easy to extend with new product types
- Follows Open/Closed Principle
- Promotes code reuse

**Cons:**
- Can make code more complex
- Requires creating many subclasses
- May introduce unnecessary abstraction

### Real-world Use Cases

- GUI toolkit factories (creating buttons, dialogs for different OS)
- Database driver factories
- File format parsers
- Plugin systems
- Document generators

---

## Abstract Factory Pattern

### Overview

The Abstract Factory pattern provides an interface for creating families of related objects without specifying their concrete classes. It's a factory of factories.

### When to Use

- When you need to create families of related products
- When you want to ensure products from one family are used together
- When you want to hide the implementation details of products

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import Protocol
import platform

# Abstract products
class Button(ABC):
    """Abstract button interface."""
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def click(self) -> str:
        pass

class Window(ABC):
    """Abstract window interface."""
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    @abstractmethod
    def close(self) -> str:
        pass

class Dialog(ABC):
    """Abstract dialog interface."""
    
    @abstractmethod
    def show(self) -> str:
        pass

# Windows concrete products
class WindowsButton(Button):
    def render(self) -> str:
        return "Rendered Windows-style button with gradient"
    
    def click(self) -> str:
        return "Windows button clicked with system sound"

class WindowsWindow(Window):
    def render(self) -> str:
        return "Rendered Windows window with title bar and borders"
    
    def close(self) -> str:
        return "Windows window closed with fade animation"

class WindowsDialog(Dialog):
    def show(self) -> str:
        return "Showing Windows dialog with system modal style"

# macOS concrete products
class MacButton(Button):
    def render(self) -> str:
        return "Rendered macOS button with rounded corners"
    
    def click(self) -> str:
        return "macOS button clicked with haptic feedback"

class MacWindow(Window):
    def render(self) -> str:
        return "Rendered macOS window with traffic lights"
    
    def close(self) -> str:
        return "macOS window closed with zoom animation"

class MacDialog(Dialog):
    def show(self) -> str:
        return "Showing macOS dialog with sheet animation"

# Linux concrete products
class LinuxButton(Button):
    def render(self) -> str:
        return "Rendered Linux button with flat design"
    
    def click(self) -> str:
        return "Linux button clicked"

class LinuxWindow(Window):
    def render(self) -> str:
        return "Rendered Linux window with minimize/maximize buttons"
    
    def close(self) -> str:
        return "Linux window closed"

class LinuxDialog(Dialog):
    def show(self) -> str:
        return "Showing Linux dialog with standard appearance"

# Abstract factory
class GUIFactory(ABC):
    """Abstract factory for creating GUI components."""
    
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_window(self) -> Window:
        pass
    
    @abstractmethod
    def create_dialog(self) -> Dialog:
        pass

# Concrete factories
class WindowsFactory(GUIFactory):
    """Factory for creating Windows GUI components."""
    
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_window(self) -> Window:
        return WindowsWindow()
    
    def create_dialog(self) -> Dialog:
        return WindowsDialog()

class MacFactory(GUIFactory):
    """Factory for creating macOS GUI components."""
    
    def create_button(self) -> Button:
        return MacButton()
    
    def create_window(self) -> Window:
        return MacWindow()
    
    def create_dialog(self) -> Dialog:
        return MacDialog()

class LinuxFactory(GUIFactory):
    """Factory for creating Linux GUI components."""
    
    def create_button(self) -> Button:
        return LinuxButton()
    
    def create_window(self) -> Window:
        return LinuxWindow()
    
    def create_dialog(self) -> Dialog:
        return LinuxDialog()

# Client code
class Application:
    """Application that uses the abstract factory."""
    
    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = factory.create_button()
        self.window = factory.create_window()
        self.dialog = factory.create_dialog()
    
    def run(self):
        """Run the application with platform-specific components."""
        print("Starting application...")
        print(self.window.render())
        print(self.button.render())
        print(self.button.click())
        print(self.dialog.show())
        print(self.window.close())

# Factory selector
def get_factory() -> GUIFactory:
    """Get appropriate factory based on the current platform."""
    system = platform.system().lower()
    
    if system == "windows":
        return WindowsFactory()
    elif system == "darwin":  # macOS
        return MacFactory()
    elif system == "linux":
        return LinuxFactory()
    else:
        # Default to Linux factory
        return LinuxFactory()

# Database example with Abstract Factory
class Database(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> str:
        pass

class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        pass
    
    @abstractmethod
    def set(self, key: str, value: str) -> str:
        pass

# PostgreSQL implementations
class PostgreSQLDatabase(Database):
    def connect(self) -> str:
        return "Connected to PostgreSQL database"
    
    def execute_query(self, query: str) -> str:
        return f"PostgreSQL: Executing {query}"

class RedisCache(Cache):
    def get(self, key: str) -> str:
        return f"Redis: Retrieved value for {key}"
    
    def set(self, key: str, value: str) -> str:
        return f"Redis: Set {key} = {value}"

# MongoDB implementations
class MongoDatabase(Database):
    def connect(self) -> str:
        return "Connected to MongoDB database"
    
    def execute_query(self, query: str) -> str:
        return f"MongoDB: Executing {query}"

class MemcachedCache(Cache):
    def get(self, key: str) -> str:
        return f"Memcached: Retrieved value for {key}"
    
    def set(self, key: str, value: str) -> str:
        return f"Memcached: Set {key} = {value}"

# Database factory
class DatabaseFactory(ABC):
    @abstractmethod
    def create_database(self) -> Database:
        pass
    
    @abstractmethod
    def create_cache(self) -> Cache:
        pass

class PostgreSQLFactory(DatabaseFactory):
    def create_database(self) -> Database:
        return PostgreSQLDatabase()
    
    def create_cache(self) -> Cache:
        return RedisCache()

class MongoFactory(DatabaseFactory):
    def create_database(self) -> Database:
        return MongoDatabase()
    
    def create_cache(self) -> Cache:
        return MemcachedCache()

# Usage example
if __name__ == "__main__":
    # GUI Factory example
    print("=== GUI Factory Example ===")
    factory = get_factory()
    app = Application(factory)
    app.run()
    
    print("\n=== Database Factory Example ===")
    # Database factory example
    db_factory = PostgreSQLFactory()
    database = db_factory.create_database()
    cache = db_factory.create_cache()
    
    print(database.connect())
    print(database.execute_query("SELECT * FROM users"))
    print(cache.set("user:1", "John Doe"))
    print(cache.get("user:1"))
    
    # Switch to MongoDB stack
    mongo_factory = MongoFactory()
    mongo_db = mongo_factory.create_database()
    mongo_cache = mongo_factory.create_cache()
    
    print(mongo_db.connect())
    print(mongo_db.execute_query("db.users.find()"))
    print(mongo_cache.set("user:1", "John Doe"))
    print(mongo_cache.get("user:1"))
```

### Pros and Cons

**Pros:**
- Ensures compatibility between products
- Isolates concrete classes from client
- Easy to swap entire product families
- Promotes consistency among products

**Cons:**
- Adding new products requires changing all factories
- Can lead to complex hierarchies
- Overkill for simple applications

### Real-world Use Cases

- Cross-platform GUI libraries
- Database abstraction layers
- Theme systems (dark/light mode)
- Cloud service abstractions (AWS/GCP/Azure)
- Game engines (different rendering backends)

---

## Builder Pattern

### Overview

The Builder pattern constructs complex objects step by step. It allows you to produce different types and representations of an object using the same construction code.

### When to Use

- When creating complex objects with many optional parameters
- When you want to create different representations of the same object
- When construction process must allow different representations
- To avoid "telescoping constructor" anti-pattern

### Python Implementation

```python
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

# Product classes
@dataclass
class Computer:
    """Computer product with various components."""
    cpu: str = ""
    memory: str = ""
    storage: str = ""
    graphics: str = ""
    motherboard: str = ""
    power_supply: str = ""
    case: str = ""
    cooling: str = ""
    network: str = ""
    operating_system: str = ""
    software: List[str] = field(default_factory=list)
    peripherals: List[str] = field(default_factory=list)
    warranty: str = ""
    price: float = 0.0
    
    def __str__(self) -> str:
        specs = []
        for key, value in self.__dict__.items():
            if value:
                if isinstance(value, list) and value:
                    specs.append(f"{key.title()}: {', '.join(value)}")
                elif not isinstance(value, list):
                    specs.append(f"{key.title()}: {value}")
        return f"Computer Configuration:\n" + "\n".join(f"  {spec}" for spec in specs)

@dataclass
class DatabaseQuery:
    """Database query product."""
    query_type: str = ""
    table: str = ""
    fields: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    joins: List[str] = field(default_factory=list)
    order_by: List[str] = field(default_factory=list)
    group_by: List[str] = field(default_factory=list)
    having: List[str] = field(default_factory=list)
    limit: Optional[int] = None
    offset: Optional[int] = None
    
    def build_query(self) -> str:
        """Build the actual SQL query."""
        if self.query_type.upper() == "SELECT":
            return self._build_select_query()
        elif self.query_type.upper() == "INSERT":
            return self._build_insert_query()
        elif self.query_type.upper() == "UPDATE":
            return self._build_update_query()
        elif self.query_type.upper() == "DELETE":
            return self._build_delete_query()
        else:
            raise ValueError(f"Unsupported query type: {self.query_type}")
    
    def _build_select_query(self) -> str:
        query_parts = [f"SELECT {', '.join(self.fields) if self.fields else '*'}"]
        query_parts.append(f"FROM {self.table}")
        
        if self.joins:
            query_parts.extend(self.joins)
        
        if self.conditions:
            query_parts.append(f"WHERE {' AND '.join(self.conditions)}")
        
        if self.group_by:
            query_parts.append(f"GROUP BY {', '.join(self.group_by)}")
        
        if self.having:
            query_parts.append(f"HAVING {' AND '.join(self.having)}")
        
        if self.order_by:
            query_parts.append(f"ORDER BY {', '.join(self.order_by)}")
        
        if self.limit is not None:
            query_parts.append(f"LIMIT {self.limit}")
        
        if self.offset is not None:
            query_parts.append(f"OFFSET {self.offset}")
        
        return " ".join(query_parts)
    
    def _build_insert_query(self) -> str:
        if not self.fields:
            raise ValueError("Fields are required for INSERT query")
        return f"INSERT INTO {self.table} ({', '.join(self.fields)}) VALUES ({', '.join(['?' for _ in self.fields])})"
    
    def _build_update_query(self) -> str:
        if not self.fields:
            raise ValueError("Fields are required for UPDATE query")
        set_clause = ', '.join([f"{field} = ?" for field in self.fields])
        query = f"UPDATE {self.table} SET {set_clause}"
        if self.conditions:
            query += f" WHERE {' AND '.join(self.conditions)}"
        return query
    
    def _build_delete_query(self) -> str:
        query = f"DELETE FROM {self.table}"
        if self.conditions:
            query += f" WHERE {' AND '.join(self.conditions)}"
        return query

# Builder interfaces
class Builder(ABC):
    """Abstract builder interface."""
    
    @abstractmethod
    def reset(self):
        pass

class ComputerBuilder(Builder):
    """Builder for creating computers."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._computer = Computer()
        return self
    
    def set_cpu(self, cpu: str):
        self._computer.cpu = cpu
        return self
    
    def set_memory(self, memory: str):
        self._computer.memory = memory
        return self
    
    def set_storage(self, storage: str):
        self._computer.storage = storage
        return self
    
    def set_graphics(self, graphics: str):
        self._computer.graphics = graphics
        return self
    
    def set_motherboard(self, motherboard: str):
        self._computer.motherboard = motherboard
        return self
    
    def set_power_supply(self, power_supply: str):
        self._computer.power_supply = power_supply
        return self
    
    def set_case(self, case: str):
        self._computer.case = case
        return self
    
    def set_cooling(self, cooling: str):
        self._computer.cooling = cooling
        return self
    
    def set_network(self, network: str):
        self._computer.network = network
        return self
    
    def set_operating_system(self, os: str):
        self._computer.operating_system = os
        return self
    
    def add_software(self, software: str):
        self._computer.software.append(software)
        return self
    
    def add_peripheral(self, peripheral: str):
        self._computer.peripherals.append(peripheral)
        return self
    
    def set_warranty(self, warranty: str):
        self._computer.warranty = warranty
        return self
    
    def set_price(self, price: float):
        self._computer.price = price
        return self
    
    def build(self) -> Computer:
        computer = self._computer
        self.reset()  # Reset for next build
        return computer

class QueryBuilder(Builder):
    """Builder for creating database queries."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._query = DatabaseQuery()
        return self
    
    def select(self, *fields: str):
        self._query.query_type = "SELECT"
        self._query.fields = list(fields)
        return self
    
    def insert(self, table: str):
        self._query.query_type = "INSERT"
        self._query.table = table
        return self
    
    def update(self, table: str):
        self._query.query_type = "UPDATE"
        self._query.table = table
        return self
    
    def delete(self):
        self._query.query_type = "DELETE"
        return self
    
    def from_table(self, table: str):
        self._query.table = table
        return self
    
    def fields(self, *fields: str):
        self._query.fields = list(fields)
        return self
    
    def where(self, condition: str):
        self._query.conditions.append(condition)
        return self
    
    def join(self, join_clause: str):
        self._query.joins.append(join_clause)
        return self
    
    def order_by(self, *fields: str):
        self._query.order_by = list(fields)
        return self
    
    def group_by(self, *fields: str):
        self._query.group_by = list(fields)
        return self
    
    def having(self, condition: str):
        self._query.having.append(condition)
        return self
    
    def limit(self, limit: int):
        self._query.limit = limit
        return self
    
    def offset(self, offset: int):
        self._query.offset = offset
        return self
    
    def build(self) -> DatabaseQuery:
        query = self._query
        self.reset()
        return query

# Director classes
class ComputerDirector:
    """Director for building different types of computers."""
    
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_gaming_pc(self) -> Computer:
        """Build a high-end gaming PC."""
        return (self.builder
                .reset()
                .set_cpu("Intel Core i9-13900K")
                .set_memory("32GB DDR5-5600")
                .set_storage("2TB NVMe SSD")
                .set_graphics("NVIDIA RTX 4080")
                .set_motherboard("ASUS ROG Strix Z790")
                .set_power_supply("850W 80+ Gold")
                .set_case("NZXT H7 Flow")
                .set_cooling("AIO Liquid Cooler 280mm")
                .set_network("WiFi 6E + Gigabit Ethernet")
                .set_operating_system("Windows 11 Pro")
                .add_software("Steam")
                .add_software("Discord")
                .add_software("OBS Studio")
                .add_peripheral("Gaming Keyboard")
                .add_peripheral("Gaming Mouse")
                .add_peripheral("4K Gaming Monitor")
                .set_warranty("3 years")
                .set_price(3500.00)
                .build())
    
    def build_office_pc(self) -> Computer:
        """Build a basic office PC."""
        return (self.builder
                .reset()
                .set_cpu("Intel Core i5-13400")
                .set_memory("16GB DDR4-3200")
                .set_storage("512GB NVMe SSD")
                .set_graphics("Integrated Graphics")
                .set_motherboard("MSI PRO B660M")
                .set_power_supply("500W 80+ Bronze")
                .set_case("Fractal Design Core 1000")
                .set_cooling("Stock CPU Cooler")
                .set_network("Gigabit Ethernet")
                .set_operating_system("Windows 11 Pro")
                .add_software("Microsoft Office")
                .add_software("Web Browser")
                .add_peripheral("Standard Keyboard")
                .add_peripheral("Standard Mouse")
                .add_peripheral("24-inch Monitor")
                .set_warranty("2 years")
                .set_price(800.00)
                .build())
    
    def build_workstation(self) -> Computer:
        """Build a professional workstation."""
        return (self.builder
                .reset()
                .set_cpu("AMD Threadripper PRO 5965WX")
                .set_memory("64GB DDR4 ECC")
                .set_storage("4TB NVMe SSD + 8TB HDD")
                .set_graphics("NVIDIA RTX A5000")
                .set_motherboard("ASUS Pro WS WRX80E-SAGE")
                .set_power_supply("1000W 80+ Platinum")
                .set_case("Fractal Design Define 7 XL")
                .set_cooling("Custom Liquid Cooling")
                .set_network("10 Gigabit Ethernet")
                .set_operating_system("Windows 11 Pro for Workstations")
                .add_software("AutoCAD")
                .add_software("SolidWorks")
                .add_software("Adobe Creative Suite")
                .add_peripheral("Professional Keyboard")
                .add_peripheral("Precision Mouse")
                .add_peripheral("32-inch 4K Monitor")
                .add_peripheral("Graphics Tablet")
                .set_warranty("5 years")
                .set_price(8000.00)
                .build())

# Fluent interface example
class FluentQueryBuilder:
    """Fluent interface for building queries."""
    
    def __init__(self):
        self._parts = []
        self._params = {}
    
    def SELECT(self, *fields):
        self._parts.append(f"SELECT {', '.join(fields) if fields else '*'}")
        return self
    
    def FROM(self, table):
        self._parts.append(f"FROM {table}")
        return self
    
    def WHERE(self, condition):
        if "WHERE" not in " ".join(self._parts):
            self._parts.append(f"WHERE {condition}")
        else:
            self._parts.append(f"AND {condition}")
        return self
    
    def ORDER_BY(self, *fields):
        self._parts.append(f"ORDER BY {', '.join(fields)}")
        return self
    
    def LIMIT(self, limit):
        self._parts.append(f"LIMIT {limit}")
        return self
    
    def build(self) -> str:
        return " ".join(self._parts)

# Usage examples
if __name__ == "__main__":
    print("=== Computer Builder Example ===")
    
    # Using builder directly
    builder = ComputerBuilder()
    custom_pc = (builder
                 .set_cpu("AMD Ryzen 7 5800X")
                 .set_memory("32GB DDR4-3600")
                 .set_storage("1TB NVMe SSD")
                 .set_graphics("NVIDIA RTX 3070")
                 .set_operating_system("Ubuntu 22.04")
                 .add_software("Visual Studio Code")
                 .add_software("Docker")
                 .set_price(2000.00)
                 .build())
    
    print(custom_pc)
    print()
    
    # Using director
    director = ComputerDirector(builder)
    
    gaming_pc = director.build_gaming_pc()
    print("Gaming PC:")
    print(gaming_pc)
    print()
    
    office_pc = director.build_office_pc()
    print("Office PC:")
    print(office_pc)
    print()
    
    print("=== Database Query Builder Example ===")
    
    # Query builder example
    query_builder = QueryBuilder()
    
    # Complex SELECT query
    select_query = (query_builder
                    .select("u.name", "u.email", "p.title")
                    .from_table("users u")
                    .join("LEFT JOIN posts p ON u.id = p.user_id")
                    .where("u.active = 1")
                    .where("u.created_at > '2023-01-01'")
                    .order_by("u.name", "p.created_at DESC")
                    .limit(10)
                    .build())
    
    print("Complex SELECT Query:")
    print(select_query.build_query())
    print()
    
    # INSERT query
    insert_query = (query_builder
                    .insert("users")
                    .fields("name", "email", "password")
                    .build())
    
    print("INSERT Query:")
    print(insert_query.build_query())
    print()
    
    # Fluent interface example
    fluent_builder = FluentQueryBuilder()
    fluent_query = (fluent_builder
                    .SELECT("name", "email")
                    .FROM("users")
                    .WHERE("active = 1")
                    .WHERE("age > 18")
                    .ORDER_BY("name")
                    .LIMIT(5)
                    .build())
    
    print("Fluent Interface Query:")
    print(fluent_query)
```

### Pros and Cons

**Pros:**
- Allows step-by-step construction
- Can create different representations
- Better control over construction process
- Avoids telescoping constructors
- Supports method chaining (fluent interface)

**Cons:**
- Increases code complexity
- Requires creating many builder classes
- May be overkill for simple objects

### Real-world Use Cases

- Database query builders (SQLAlchemy, Django ORM)
- Configuration objects
- HTML/XML document builders
- Test data builders
- HTTP request builders
- UI component builders

---

## Prototype Pattern

### Overview

The Prototype pattern creates objects by cloning existing instances rather than creating new ones from scratch. It's useful when object creation is expensive or complex.

### When to Use

- When object creation is expensive (database queries, network calls)
- When you need to avoid subclasses of object creator
- When you want to reduce the number of classes in your system
- When objects have only a few different combinations of state

### Python Implementation

```python
import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Prototype interface
class Prototype(ABC):
    """Abstract prototype interface."""
    
    @abstractmethod
    def clone(self) -> 'Prototype':
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

# Concrete prototypes
class Document(Prototype):
    """Document prototype with complex structure."""
    
    def __init__(self, title: str = "", content: str = "", metadata: Optional[Dict] = None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.version = 1
        self.sections: List[Dict[str, Any]] = []
        self.attachments: List[str] = []
    
    def add_section(self, title: str, content: str, level: int = 1):
        """Add a section to the document."""
        section = {
            "title": title,
            "content": content,
            "level": level,
            "id": len(self.sections) + 1
        }
        self.sections.append(section)
        self.modified_at = datetime.now()
    
    def add_attachment(self, filename: str):
        """Add an attachment to the document."""
        self.attachments.append(filename)
        self.modified_at = datetime.now()
    
    def clone(self) -> 'Document':
        """Create a deep copy of the document."""
        cloned = Document()
        cloned.title = f"{self.title} (Copy)"
        cloned.content = self.content
        cloned.metadata = copy.deepcopy(self.metadata)
        cloned.created_at = datetime.now()  # New creation time
        cloned.modified_at = datetime.now()
        cloned.version = 1  # Reset version for clone
        cloned.sections = copy.deepcopy(self.sections)
        cloned.attachments = copy.deepcopy(self.attachments)
        return cloned
    
    def shallow_clone(self) -> 'Document':
        """Create a shallow copy of the document."""
        return copy.copy(self)
    
    def __str__(self) -> str:
        return (f"Document: {self.title}\n"
                f"Version: {self.version}\n"
                f"Sections: {len(self.sections)}\n"
                f"Attachments: {len(self.attachments)}\n"
                f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

class DatabaseConnection(Prototype):
    """Database connection prototype."""
    
    def __init__(self, host: str = "", port: int = 5432, database: str = "", 
                 username: str = "", connection_pool_size: int = 10):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.connection_pool_size = connection_pool_size
        self.connection_string = self._build_connection_string()
        self.is_connected = False
        self.query_cache: Dict[str, Any] = {}
        self.connection_id = id(self)
    
    def _build_connection_string(self) -> str:
        return f"postgresql://{self.username}@{self.host}:{self.port}/{self.database}"
    
    def connect(self):
        """Simulate database connection."""
        self.is_connected = True
        print(f"Connected to {self.connection_string}")
    
    def disconnect(self):
        """Simulate database disconnection."""
        self.is_connected = False
        print(f"Disconnected from {self.connection_string}")
    
    def clone(self) -> 'DatabaseConnection':
        """Clone the database connection with new connection ID."""
        cloned = DatabaseConnection(
            host=self.host,
            port=self.port,
            database=self.database,
            username=self.username,
            connection_pool_size=self.connection_pool_size
        )
        # Don't copy connection state and cache
        cloned.query_cache = {}
        cloned.is_connected = False
        return cloned
    
    def __str__(self) -> str:
        return (f"Database Connection:\n"
                f"  Host: {self.host}:{self.port}\n"
                f"  Database: {self.database}\n"
                f"  Username: {self.username}\n"
                f"  Connected: {self.is_connected}\n"
                f"  Connection ID: {self.connection_id}")

class APIRequest(Prototype):
    """API request prototype with complex configuration."""
    
    def __init__(self, base_url: str = "", endpoint: str = "", method: str = "GET"):
        self.base_url = base_url
        self.endpoint = endpoint
        self.method = method.upper()
        self.headers: Dict[str, str] = {}
        self.parameters: Dict[str, Any] = {}
        self.body: Optional[Dict[str, Any]] = None
        self.timeout = 30
        self.retry_count = 3
        self.auth_token: Optional[str] = None
        
    def set_header(self, key: str, value: str):
        """Set request header."""
        self.headers[key] = value
        return self
    
    def set_parameter(self, key: str, value: Any):
        """Set request parameter."""
        self.parameters[key] = value
        return self
    
    def set_body(self, body: Dict[str, Any]):
        """Set request body."""
        self.body = body
        return self
    
    def set_auth_token(self, token: str):
        """Set authentication token."""
        self.auth_token = token
        self.headers["Authorization"] = f"Bearer {token}"
        return self
    
    def clone(self) -> 'APIRequest':
        """Clone the API request."""
        cloned = APIRequest(self.base_url, self.endpoint, self.method)
        cloned.headers = copy.deepcopy(self.headers)
        cloned.parameters = copy.deepcopy(self.parameters)
        cloned.body = copy.deepcopy(self.body)
        cloned.timeout = self.timeout
        cloned.retry_count = self.retry_count
        cloned.auth_token = self.auth_token
        return cloned
    
    def execute(self) -> str:
        """Simulate API request execution."""
        url = f"{self.base_url}{self.endpoint}"
        return (f"Executing {self.method} request to {url}\n"
                f"Headers: {self.headers}\n"
                f"Parameters: {self.parameters}\n"
                f"Body: {self.body}")
    
    def __str__(self) -> str:
        return (f"API Request:\n"
                f"  URL: {self.base_url}{self.endpoint}\n"
                f"  Method: {self.method}\n"
                f"  Headers: {len(self.headers)}\n"
                f"  Parameters: {len(self.parameters)}\n"
                f"  Timeout: {self.timeout}s")

# Prototype registry
class PrototypeRegistry:
    """Registry for managing prototypes."""
    
    def __init__(self):
        self._prototypes: Dict[str, Prototype] = {}
    
    def register_prototype(self, name: str, prototype: Prototype):
        """Register a prototype with a name."""
        self._prototypes[name] = prototype
    
    def unregister_prototype(self, name: str):
        """Unregister a prototype."""
        if name in self._prototypes:
            del self._prototypes[name]
    
    def get_prototype(self, name: str) -> Optional[Prototype]:
        """Get a prototype by name."""
        prototype = self._prototypes.get(name)
        if prototype:
            return prototype.clone()
        return None
    
    def list_prototypes(self) -> List[str]:
        """List all registered prototype names."""
        return list(self._prototypes.keys())

# Prototype factory
class PrototypeFactory:
    """Factory that uses prototypes to create objects."""
    
    def __init__(self):
        self.registry = PrototypeRegistry()
        self._setup_default_prototypes()
    
    def _setup_default_prototypes(self):
        """Setup default prototypes."""
        # Document templates
        blog_post = Document("Blog Post Template", "Write your blog content here...")
        blog_post.metadata = {"type": "blog", "category": "general", "tags": []}
        blog_post.add_section("Introduction", "Introduce your topic here")
        blog_post.add_section("Main Content", "Main content goes here")
        blog_post.add_section("Conclusion", "Conclude your post here")
        self.registry.register_prototype("blog_post", blog_post)
        
        technical_doc = Document("Technical Documentation", "Technical documentation content...")
        technical_doc.metadata = {"type": "technical", "version": "1.0", "audience": "developers"}
        technical_doc.add_section("Overview", "System overview", 1)
        technical_doc.add_section("Architecture", "System architecture", 1)
        technical_doc.add_section("API Reference", "API documentation", 1)
        technical_doc.add_section("Examples", "Code examples", 2)
        self.registry.register_prototype("technical_doc", technical_doc)
        
        # Database connections
        local_db = DatabaseConnection("localhost", 5432, "testdb", "testuser", 5)
        self.registry.register_prototype("local_db", local_db)
        
        prod_db = DatabaseConnection("prod-server.example.com", 5432, "proddb", "produser", 20)
        self.registry.register_prototype("prod_db", prod_db)
        
        # API requests
        rest_api = APIRequest("https://api.example.com", "/v1/users", "GET")
        rest_api.set_header("Content-Type", "application/json")
        rest_api.set_header("Accept", "application/json")
        rest_api.timeout = 60
        self.registry.register_prototype("rest_api", rest_api)
        
        graphql_api = APIRequest("https://api.example.com", "/graphql", "POST")
        graphql_api.set_header("Content-Type", "application/json")
        graphql_api.set_body({"query": "{ users { id name email } }"})
        self.registry.register_prototype("graphql_api", graphql_api)
    
    def create_document(self, template_name: str) -> Optional[Document]:
        """Create a document from a template."""
        return self.registry.get_prototype(template_name)
    
    def create_db_connection(self, config_name: str) -> Optional[DatabaseConnection]:
        """Create a database connection from a configuration."""
        return self.registry.get_prototype(config_name)
    
    def create_api_request(self, template_name: str) -> Optional[APIRequest]:
        """Create an API request from a template."""
        return self.registry.get_prototype(template_name)

# Configuration prototype with deep cloning
class Configuration(Prototype):
    """Configuration prototype with nested settings."""
    
    def __init__(self, name: str = "Default Config"):
        self.name = name
        self.database_config = {
            "host": "localhost",
            "port": 5432,
            "database": "myapp",
            "pool_size": 10
        }
        self.cache_config = {
            "type": "redis",
            "host": "localhost",
            "port": 6379,
            "ttl": 3600
        }
        self.logging_config = {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "handlers": ["console", "file"]
        }
        self.feature_flags = {
            "new_ui": False,
            "advanced_analytics": False,
            "beta_features": False
        }
    
    def clone(self) -> 'Configuration':
        """Deep clone the configuration."""
        cloned = Configuration(f"{self.name} (Copy)")
        cloned.database_config = copy.deepcopy(self.database_config)
        cloned.cache_config = copy.deepcopy(self.cache_config)
        cloned.logging_config = copy.deepcopy(self.logging_config)
        cloned.feature_flags = copy.deepcopy(self.feature_flags)
        return cloned
    
    def to_json(self) -> str:
        """Convert configuration to JSON."""
        config_dict = {
            "name": self.name,
            "database": self.database_config,
            "cache": self.cache_config,
            "logging": self.logging_config,
            "features": self.feature_flags
        }
        return json.dumps(config_dict, indent=2)
    
    def __str__(self) -> str:
        return f"Configuration: {self.name}"

# Usage examples
if __name__ == "__main__":
    print("=== Basic Prototype Usage ===")
    
    # Create original document
    original_doc = Document("Original Document", "This is the original content")
    original_doc.add_section("Chapter 1", "First chapter content")
    original_doc.add_section("Chapter 2", "Second chapter content")
    original_doc.add_attachment("image1.png")
    
    print("Original Document:")
    print(original_doc)
    print()
    
    # Clone the document
    cloned_doc = original_doc.clone()
    cloned_doc.add_section("Chapter 3", "Additional chapter in clone")
    
    print("Cloned Document:")
    print(cloned_doc)
    print()
    
    print("=== Prototype Factory Usage ===")
    
    # Use prototype factory
    factory = PrototypeFactory()
    
    # Create documents from templates
    blog = factory.create_document("blog_post")
    if blog:
        blog.title = "My First Blog Post"
        blog.content = "Welcome to my blog!"
        print("Blog Post from Template:")
        print(blog)
        print()
    
    tech_doc = factory.create_document("technical_doc")
    if tech_doc:
        tech_doc.title = "API Documentation v2.0"
        print("Technical Document from Template:")
        print(tech_doc)
        print()
    
    # Create database connections
    local_conn = factory.create_db_connection("local_db")
    if local_conn:
        local_conn.connect()
        print("Local Database Connection:")
        print(local_conn)
        print()
    
    prod_conn = factory.create_db_connection("prod_db")
    if prod_conn:
        print("Production Database Connection:")
        print(prod_conn)
        print()
    
    # Create API requests
    api_request = factory.create_api_request("rest_api")
    if api_request:
        api_request.endpoint = "/v1/posts"
        api_request.set_parameter("limit", 10)
        api_request.set_parameter("offset", 0)
        print("REST API Request:")
        print(api_request)
        print()
        print("Executing request:")
        print(api_request.execute())
        print()
    
    print("=== Configuration Prototype ===")
    
    # Configuration prototype
    base_config = Configuration("Base Configuration")
    
    # Development configuration
    dev_config = base_config.clone()
    dev_config.name = "Development Configuration"
    dev_config.database_config["database"] = "myapp_dev"
    dev_config.logging_config["level"] = "DEBUG"
    dev_config.feature_flags["beta_features"] = True
    
    # Production configuration
    prod_config = base_config.clone()
    prod_config.name = "Production Configuration"
    prod_config.database_config["host"] = "prod-db.example.com"
    prod_config.database_config["pool_size"] = 50
    prod_config.cache_config["host"] = "prod-cache.example.com"
    prod_config.logging_config["level"] = "WARNING"
    
    print("Development Configuration:")
    print(dev_config.to_json())
    print()
    
    print("Production Configuration:")
    print(prod_config.to_json())
    print()
    
    print("=== Registry Usage ===")
    
    registry = PrototypeRegistry()
    
    # Register configurations
    registry.register_prototype("dev_config", dev_config)
    registry.register_prototype("prod_config", prod_config)
    
    print(f"Registered prototypes: {registry.list_prototypes()}")
    
    # Get a clone from registry
    test_config = registry.get_prototype("dev_config")
    if test_config:
        test_config.name = "Test Configuration"
        print(f"\nCloned configuration: {test_config}")
```

### Pros and Cons

**Pros:**
- Reduces object creation overhead
- Avoids complex initialization
- Runtime configuration of objects
- Reduces subclassing
- Hide complexity of object creation

**Cons:**
- Can be complex to implement deep cloning
- May require handling circular references
- Cloning objects with external dependencies can be tricky

### Real-world Use Cases

- Document templates and forms
- Game object prototypes (characters, weapons, items)
- Database connection configurations
- GUI widget templates
- Email templates
- Configuration objects for different environments
- Caching frequently created objects

---

## Summary

Creational design patterns provide flexible and reusable solutions for object creation:

1. **Singleton**: Ensures single instance - use for shared resources
2. **Factory Method**: Creates objects via inheritance - use for product families
3. **Abstract Factory**: Creates families of related objects - use for platform-specific code
4. **Builder**: Constructs complex objects step-by-step - use for objects with many parameters
5. **Prototype**: Creates objects by copying existing instances - use when creation is expensive

Choose the appropriate pattern based on your specific requirements:
- Use **Singleton** for global access to shared resources
- Use **Factory Method** when you need to delegate object creation to subclasses
- Use **Abstract Factory** when working with families of related objects
- Use **Builder** for complex objects with many optional parameters
- Use **Prototype** when object creation is expensive or you need runtime configuration

Each pattern solves specific object creation challenges and can be combined with other design patterns to create robust, maintainable software architectures.