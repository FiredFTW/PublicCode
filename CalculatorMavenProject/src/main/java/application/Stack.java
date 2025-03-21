package application;

import java.util.ArrayList;


/**
 * Maintains a stack of Entry objects.
 * 
 * @author ZLAC211
 */

public class Stack {
  private ArrayList<Entry> elements = new ArrayList<Entry>();
  private int size = 0;

  /**
   * Pushes an entry onto the stack.
   * 
   * @param entry - the entry to be pushed
   */
  public void push(Entry entry) {
    elements.add(entry);
    size++;
  }

  /**
   * Removes the last entry added to the stack and returns it.
   * 
   * @return the entry 'on top of' the stack
   * @throws EmptyStackException if the stack is empty
   */
  public Entry pop() throws EmptyStackException {
    if (size == 0) {
      throw new EmptyStackException(); // if stack is empty, throw exception
    }

    // return last added element, remove it, decrease size
    Entry returnEntry = elements.get(size() - 1);
    elements.remove(size() - 1);
    size--;
    return returnEntry;
  }

  /**
   * Returns the last entry added to the stack without removing it.
   * 
   * @return the entry 'on top of' the stack
   * @throws EmptyStackException if the stack is empty
   */
  public Entry top() throws EmptyStackException {
    if (size == 0) {
      throw new EmptyStackException(); // if stack is empty, throw exception
    }
    // return last entry but do NOT remove
    return elements.get(size() - 1);
  }

  /**
   * Returns the size of the stack.
   * 
   * @return number of elements on the stack as an int
   */
  public int size() {
    return size;
  }


}
