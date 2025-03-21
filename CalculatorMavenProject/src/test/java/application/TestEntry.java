package application;

import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class TestEntry {
  static Entry numberEntry;
  static Entry symbolEntry;
  static Entry stringEntry;
  static Entry invalidEntry;

  @BeforeAll
  static void testNumberEntry() {
    numberEntry = new Entry(5);
    symbolEntry = new Entry(Symbol.PLUS);
    stringEntry = new Entry("hello");
    invalidEntry = new Entry(Symbol.INVALID);
  }
  // create entry objects

  @Test // test 1
  void testGetType() {
    assertEquals(numberEntry.getType(), Type.NUMBER);
    assertEquals(symbolEntry.getType(), Type.SYMBOL);
    assertEquals(stringEntry.getType(), Type.STRING);
    assertEquals(invalidEntry.getType(), Type.INVALID);
  }
  // test passed by adding getType method to Entry

  @Test // test 2
  void testGetters() {
    try {
      assertEquals(numberEntry.getValue(), 5);
      assertEquals(symbolEntry.getSymbol(), Symbol.PLUS);
      assertEquals(stringEntry.getString(), "hello");
    } catch (BadTypeException e) {
      e.printStackTrace();
    }
  }
  // test passed by adding getters for the 3 possible types
  // (later surrounded by try catch due to implementation of BadTypeException for test 3)

  @Test // test 3
  void testBadTypeException() {
    assertThrows(BadTypeException.class, () -> {
      numberEntry.getString();
    });
    assertThrows(BadTypeException.class, () -> {
      symbolEntry.getString();
    });
    assertThrows(BadTypeException.class, () -> {
      stringEntry.getValue();
    });
    assertThrows(BadTypeException.class, () -> {
      stringEntry.getSymbol();
    });
  }
  /*
   * created custom exception and added throw conditions if a getter is called on an entry that does
   * not contain that type
   */

  @Test // test 4
  void testHashCode() {
    Entry numberEntry2 = new Entry(5);
    assertEquals(numberEntry.hashCode(), numberEntry2.hashCode());
    Entry symbolEntry2 = new Entry(Symbol.PLUS);
    assertEquals(symbolEntry.hashCode(), symbolEntry2.hashCode());
    Entry stringEntry2 = new Entry("hello");
    assertEquals(stringEntry.hashCode(), stringEntry2.hashCode());
  }
  // implemented hashCode method

  @Test // test 5
  // checking entries with the same type and value are considered the same
  void testEquals() {
    assertEquals(numberEntry, numberEntry);
    Entry numberEntry2 = new Entry(5);
    Entry symbolEntry2 = new Entry(Symbol.PLUS);
    Entry stringEntry2 = new Entry("hello");
    assertEquals(numberEntry, numberEntry2);
    assertEquals(symbolEntry, symbolEntry2);
    assertEquals(stringEntry, stringEntry2);
  }
  // implemented equals method

  @Test // test 6
  // checking entries with the same type but different values are considered different
  void testNotEquals() {
    assertNotEquals(numberEntry, symbolEntry);
    assertNotEquals(numberEntry, invalidEntry);
    assertNotEquals(numberEntry, null);
    Entry numberEntry3 = new Entry(6);
    assertNotEquals(numberEntry3, numberEntry);
    Entry stringEntry3 = new Entry("hi");
    assertNotEquals(stringEntry3, stringEntry);
    Entry symbolEntry3 = new Entry(Symbol.DIVIDE);
    assertNotEquals(symbolEntry3, symbolEntry);
  }
  // expanded equals method with checks for more cases

  @Test // test 7
  void testToString() {
    assertEquals(numberEntry.toString(), "5.0");
    assertEquals(stringEntry.toString(), "hello");
    assertEquals(symbolEntry.toString(), "+");
    assertEquals(invalidEntry.toString(), "Invalid Entry");
  }

  // implemented an overridden toString method in the entry class


}
