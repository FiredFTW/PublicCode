package application;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TestStack {

  Stack testStack;

  @BeforeEach // create a new stack before each test
  void setUp() {
    testStack = new Stack();

  }

  @Test // Test 1
  void testStack() {
    assertEquals(testStack.size(), 0);
  }
  // added size field initialised at 0 and method to return value


  @Test // Test 2
  void testPush() {
    testStack.push(new Entry(5));
    assertEquals(testStack.size(), 1);
  }
  // added empty method push
  // fake size method to return 1 for now
  // changed after test 4 to include entry argument

  @Test // Test 3
  void testSizeChange() {
    testStack.push(new Entry(5));
    assertEquals(testStack.size(), 1);
    try {
      testStack.pop();
    } catch (EmptyStackException e) {
    }
    assertEquals(testStack.size(), 0);
  }
  // push method increases size by 1
  // pop reduces size by 1
  // changed after test 4 to include entry argument


  @Test // Test 4
  void testPushThenPop() {
    try {
      testStack.push(new Entry(5));
      Entry entry = testStack.pop();
      assertEquals(entry.getValue(), 5);
    } catch (BadTypeException e) {
      e.printStackTrace();
    } catch (EmptyStackException e) {
      e.printStackTrace();
    }
  }
  // implemented an array list to contain entries
  // added functionality to push to append entry to list
  // added pop method returns last element of list
  // changed after test 5 to catch EmptyStackException

  @Test // Test 5
  void testPopWhenEmpty() {
    assertThrows(EmptyStackException.class, () -> {
      testStack.pop();
    });
  }
  // created EmptyStackException class
  // added if statement to check for empty stack, throw exception if so

  @Test // Test 6
  void testTop() {
    testStack.push(new Entry("hi"));
    try {
      assertEquals(testStack.top().getString(), "hi");
    } catch (EmptyStackException e) {
      e.printStackTrace();
    } catch (BadTypeException e) {
      e.printStackTrace();
    }
    assertEquals(testStack.size(), 1);
  }
  // added top method which is the same as pop but does not remove element or change size

  @Test // Test 7
  void testTopWhenEmpty() {
    assertThrows(EmptyStackException.class, () -> {
      testStack.top();
    });
  }
  // added if statement to check for empty stack, throw exception if so


  @Test // Test 8
  // pushes many entries then pops to see if they are returned in correct order
  void testMultiPush() {
    for (int i = 0; i < 1000; i++) {
      testStack.push(new Entry(i));
    }
    assertEquals(testStack.size(), 1000);
    for (int i = 999; i > 0; i--) {
      try {
        Entry entry = testStack.pop();
        assertEquals(entry.getValue(), (float) i);
      } catch (BadTypeException e) {
        e.printStackTrace();
      } catch (EmptyStackException e) {
        e.printStackTrace();
      }
    }
  }
  // no changes required, stack can handle lots of entries

}


