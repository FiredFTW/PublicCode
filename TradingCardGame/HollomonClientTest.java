import java.util.*;

public class HollomonClientTest {
    public static void main(String args[]){
        HollomonClient client = new HollomonClient("netsrv.cim.rhul.ac.uk", 1812);
        List<Card> list = client.login(args[0], args[1]);
        System.out.println(client.getCredits());
        System.out.println("CARDS:");
        System.out.println(client.getCards());
        client.close();
    }
}