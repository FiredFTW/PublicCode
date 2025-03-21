package application;

/**
 * A stack implementation for floats only.
 * 
 * @author ZLAC211
 */
public class NumStack {
  private Stack stack = new Stack();

  public void push(float num) {
    stack.push(new Entry(num));
  }

  /**
   * Returns the top element of the stack and removes it.
   * 
   * @return top element of the stack.
   * @throws EmptyStackException if stack is empty
   */
  public float pop() throws EmptyStackException {
    try {
      return stack.pop().getValue();
    } catch (BadTypeException e) {
      e.printStackTrace();
    } catch (EmptyStackException e) {
      throw new EmptyStackException();
    }
    return 0;
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
