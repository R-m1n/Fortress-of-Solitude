package messaround;

import java.util.Stack;

public class Validity {
    public static boolean isValid(String input) {
        // Check validity of an expression.
        Stack<String> chr_stack = new Stack<>();
        String obrackets = "({<[";
        String cbrackets = ")}>]";
        int balance = 0;
        String bracket = "";

        for (char chr : input.toCharArray()) {
            chr_stack.push(String.valueOf(chr));
        }

        while (!chr_stack.empty()) {
            boolean cond1 = obrackets.contains(chr_stack.peek());
            boolean cond2 = cbrackets.contains(chr_stack.peek());

            if (cond1 | cond2) {
                bracket = chr_stack.peek();

                if (obrackets.contains(bracket))
                    // add 1 to avoid index 0 for the first element.
                    balance += obrackets.indexOf(bracket) + 1;

                if (cbrackets.contains(bracket))
                    // add 1 to avoid index 0 for the first element.
                    balance -= cbrackets.indexOf(bracket) + 1;

            }

            chr_stack.pop();
        }

        if (balance == 0 & !cbrackets.contains(bracket))
            /*
             * if the expression is valid the balance should be 0.
             * and the first bracket in the expression shouldn't be a closing one.
             */

            return true;

        return false;
    }

    public static boolean valid(String input) {
        // Check validity of an expression.

        Stack<String> chr_stack = new Stack<>();
        String obrackets = "({<[";
        String cbrackets = ")}>]";

        for (char chr : input.toCharArray()) {
            String str = String.valueOf(chr);
            boolean cond1 = obrackets.contains(str);
            boolean cond2 = cbrackets.contains(str);

            if (cond1)
                chr_stack.push(str);

            // if the first encountered bracket is a closing one.
            if (cond2 & chr_stack.empty())
                return false;

            if (cond2 & !chr_stack.empty())
                // make sure brackets are of the same type.
                if (obrackets.indexOf(chr_stack.peek()) == cbrackets.indexOf(str))
                    chr_stack.pop();

                else
                    return false;
        }

        return true;
    }
}