package application;

/**
 * Stack data structure for storing operator symbols.
 * 
 * @author ZLAC211
 */
public class OpStack {
  private Stack stack = new Stack();

  public void push(String operator) {
    stack.push(new Entry(operator));
  }



  /**
   * Returns the top element of the stack and removes it.
   * 
   * @return top element of the stack.
   * @throws EmptyStackException if stack is empty
   */
  public String pop() throws EmptyStackException {
    try {
      return stack.pop().getString();
    } catch (BadTypeException e) {
      e.printStackTrace();
    } catch (EmptyStackException e) {
      throw new EmptyStackException();
    }
    return "";
  }

  /**
   * Returns the top element of the stack without removing it.
   * 
   * @return top element of the stack.
   * @throws EmptyStackException if stack is empty
   */
  public String top() throws EmptyStackException {
    try {
      return stack.top().getString();
    } catch (BadTypeException e) {
      e.printStackTrace();
    } catch (EmptyStackException e) {
      throw new EmptyStackException();
    }
    return "";
  }

  /**
   * Provides the size of the stack.
   * 
   * @return the number of float elements stored in the stack
   */
  public int size() {
    return stack.size();
  }
}
