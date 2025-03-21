import java.util.*;

public class CardTest{
    public static void main(String args[]){

        Card dev = new Card(123, "dev", Rank.COMMON);
        Card dan = new Card(999, "dan", Rank.UNIQUE);
        Card bobtiv = new Card(567, "bobtiv", Rank.COMMON);
        Card dev2 = new Card(123, "dev", Rank.COMMON);
        dev2.setPrice(99);

        System.out.println(dev.compareTo(dan));
        System.out.println(dan.compareTo(dev));
        System.out.println(dev.compareTo(bobtiv));
        System.out.println(dev.compareTo(dev2));

        System.out.println("HashSet:");
        HashSet<Card> hs= new HashSet<Card>();
        hs.add(dev);
        hs.add(dan);
        hs.add(bobtiv);
        hs.add(dev2);
        System.out.println(hs);

        System.out.println("TreeSet:");
        TreeSet<Card> ts = new TreeSet<Card>();
        ts.add(dev);
        ts.add(dan);
        ts.add(bobtiv);
        ts.add(dev2);
        Iterator i=ts.iterator();  
        while(i.hasNext())  
        {  
            System.out.println(i.next());  
        }  


    }
}