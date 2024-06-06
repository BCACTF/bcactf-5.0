package flagserver;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.SocketException;
import java.util.List;

public class ChatServerSocketListener implements Runnable {
    private ClientConnectionData client;
    private List<ClientConnectionData> clientList;

    public ChatServerSocketListener(ClientConnectionData client, List<ClientConnectionData> clientList) {
        this.client = client;
        this.clientList = clientList;
    }

    @Override
    public void run() {
        try {
            ObjectInputStream in = client.getInput();

            MessageCtoS_Request reqMsg = (MessageCtoS_Request) in.readObject();
            String flag = "Error: No challenge named " + reqMsg.chall + " found.";
            if (reqMsg.chall.equals("fakechall")) {
                flag = "bcactf{fake_flag}";
            }
            if (reqMsg.chall.equals("flagserver")) {
                flag = "bcactf{thankS_5OCK3ts_and_tHreADInG_clA5s_2f6fb44c998fd8}";
            }
            MessageStoC_Flag out = new MessageStoC_Flag(flag);
            System.out.println(flag);
            client.getOut().writeObject(out);

        } catch (Exception ex) {
            if (ex instanceof SocketException) {
                System.out.println("Caught socket ex for " +
                        client.getName());
            } else {
                System.out.println(ex);
                ex.printStackTrace();
            }
        } finally {
            // Remove client from clientList
            clientList.remove(client);

            try {
                client.getSocket().close();
            } catch (IOException ex) {
            }
        }
    }

}
